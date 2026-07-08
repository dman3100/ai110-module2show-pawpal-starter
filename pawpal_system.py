"""
pawpal_system.py
Logic layer for PawPal+. Phase 4 -- adds sorting, filtering, conflict
detection, and recurring-task automation on top of the Phase 2 scheduler.

Scheduling convention: priority is an int where HIGHER = more urgent (5 beats 1).
Confirmed against the official README's Sample Output (Rex/Luna example),
where priority 5 tasks are scheduled ahead of priority 2/3/4 tasks.
"""

from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import Optional

DAY_START = "08:00"


@dataclass
class Task:
    """A single pet-care activity (walk, feeding, meds, grooming, enrichment)."""

    description: str
    task_type: str
    priority: int
    duration_min: int
    due_date: Optional[str] = None   # "YYYY-MM-DD" -- which day this task is due
    due_time: Optional[str] = None   # "HH:MM" -- time of day, used for sorting/conflicts
    frequency: Optional[str] = None  # None, "daily", or "weekly"
    completed: bool = False

    def mark_complete(self):
        """Flip this task's completed status to True."""
        self.completed = True

    def next_occurrence(self) -> Optional["Task"]:
        """
        If this task recurs ("daily" or "weekly") and has a due_date to
        advance from, return a new, incomplete Task for the next occurrence.
        Returns None for non-recurring tasks or tasks with no due_date.
        """
        if self.frequency not in ("daily", "weekly") or self.due_date is None:
            return None

        current = datetime.strptime(self.due_date, "%Y-%m-%d")
        delta = timedelta(days=1) if self.frequency == "daily" else timedelta(weeks=1)
        next_date = current + delta

        return Task(
            description=self.description,
            task_type=self.task_type,
            priority=self.priority,
            duration_min=self.duration_min,
            due_date=next_date.strftime("%Y-%m-%d"),
            due_time=self.due_time,
            frequency=self.frequency,
            completed=False,
        )


@dataclass
class Pet:
    """Stores a pet's identity and the list of care tasks it needs."""

    name: str
    species: str
    breed: Optional[str] = None
    tasks: list[Task] = field(default_factory=list)

    def add_task(self, task: Task):
        """Attach a new Task to this pet's task list."""
        self.tasks.append(task)


@dataclass
class Owner:
    """Manages an owner's pets, available time, and scheduling preferences."""

    name: str
    time_available: int
    preferences: dict = field(default_factory=dict)
    pets: list[Pet] = field(default_factory=list)

    def add_pet(self, pet: Pet):
        """Register a new Pet under this owner."""
        self.pets.append(pet)


class Scheduler:
    """The 'brain': builds per-pet plans and provides cross-pet algorithms."""

    def generate_plan(self, pet: Pet, time_budget: int) -> list[dict]:
        """
        Build a single pet's daily plan within time_budget minutes.

        Returns a list of dicts, one per scheduled task, each containing:
        {"task": Task, "start_time": "HH:MM", "reason": str}

        Tasks are chosen greedily: highest priority first, and among equal
        priorities, shorter tasks first (fits more into a tight budget).
        A task is skipped if it would overflow the remaining budget.
        """
        if time_budget <= 0 or not pet.tasks:
            return []

        ordered = sorted(
            pet.tasks,
            key=lambda t: (-t.priority, t.duration_min),
        )

        plan: list[dict] = []
        remaining = time_budget
        clock = datetime.strptime(DAY_START, "%H:%M")

        for task in ordered:
            if task.duration_min > remaining:
                continue

            reason = (
                f"Priority {task.priority} {task.task_type} task "
                f"({task.duration_min} min) fits in the {remaining} min "
                f"remaining for {pet.name}."
            )

            plan.append(
                {
                    "task": task,
                    "start_time": clock.strftime("%H:%M"),
                    "reason": reason,
                }
            )

            clock += timedelta(minutes=task.duration_min)
            remaining -= task.duration_min

        return plan

    def generate_all_plans(self, owner: Owner) -> dict[str, list[dict]]:
        """
        Build a plan for every pet the owner has, splitting time_available
        evenly across pets (see reflection.md 1b for why even-split over
        proportional-to-task-load).

        Returns {pet_name: plan} where plan is generate_plan()'s output.
        """
        if not owner.pets:
            return {}

        per_pet_budget = owner.time_available // len(owner.pets)

        return {
            pet.name: self.generate_plan(pet, per_pet_budget)
            for pet in owner.pets
        }

    def sort_by_time(self, tasks: list[Task]) -> list[Task]:
        """
        Sort tasks by due_time ("HH:MM"), earliest first. Tasks with no
        due_time are placed at the end -- they have no explicit time
        constraint, so they shouldn't be treated as "earliest."
        """
        return sorted(
            tasks,
            key=lambda t: (t.due_time is None, t.due_time or ""),
        )

    def filter_tasks(
        self,
        owner: Owner,
        pet_name: Optional[str] = None,
        completed: Optional[bool] = None,
    ) -> list[Task]:
        """
        Filter tasks across ALL of an owner's pets by pet name and/or
        completion status. Passing None for either parameter means "don't
        filter on this criterion" -- e.g. filter_tasks(owner, completed=False)
        returns every incomplete task for every pet.
        """
        results = []
        for pet in owner.pets:
            if pet_name is not None and pet.name != pet_name:
                continue
            for task in pet.tasks:
                if completed is not None and task.completed != completed:
                    continue
                results.append(task)
        return results

    def detect_conflicts(self, owner: Owner) -> list[str]:
        """
        Lightweight conflict check: flags any two or more tasks -- across
        the SAME pet or DIFFERENT pets -- that share an identical due_time.
        Returns a list of human-readable warning strings instead of raising,
        so a conflict never crashes the program; it's surfaced to the caller
        to display or ignore.

        Known limitation: this only detects exact due_time matches, not
        overlapping duration windows (e.g. an 08:00-08:30 task and an 08:15
        task wouldn't be flagged as conflicting). See reflection.md 2b.
        """
        by_time: dict[str, list[tuple[str, Task]]] = {}

        for pet in owner.pets:
            for task in pet.tasks:
                if task.due_time is None:
                    continue
                by_time.setdefault(task.due_time, []).append((pet.name, task))

        warnings = []
        for due_time, entries in by_time.items():
            if len(entries) > 1:
                names = ", ".join(
                    f"{pet_name}'s '{task.description}'" for pet_name, task in entries
                )
                warnings.append(f"⚠ Conflict at {due_time}: {names} are all scheduled at the same time.")
        return warnings

    def complete_task(self, pet: Pet, task: Task) -> Optional[Task]:
        """
        Mark a task complete, and if it's recurring ("daily"/"weekly"),
        automatically create and attach the next occurrence to the same
        pet. Returns the newly created Task if one was spawned, else None.
        """
        task.mark_complete()
        next_task = task.next_occurrence()
        if next_task is not None:
            pet.add_task(next_task)
        return next_task
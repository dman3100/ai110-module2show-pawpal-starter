"""
pawpal_system.py
Logic layer for PawPal+. Phase 2 -- classes implemented with working logic.

Scheduling convention: priority is an int where HIGHER = more urgent (5 beats 1).
If your app.py / README examples assume the opposite, flip the sort key in
Scheduler.generate_plan.
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
    completed: bool = False

    def mark_complete(self):
        """Flip this task's completed status to True."""
        self.completed = True


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
    """The 'brain': builds a per-pet daily plan and explains each choice."""

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
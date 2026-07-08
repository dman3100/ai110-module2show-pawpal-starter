"""
main.py
Demo script for PawPal+'s logic layer.

Phase 2: builds an Owner with two Pets and runs Scheduler.generate_all_plans().
Phase 4: adds tasks out of order and demonstrates sort_by_time(), filter_tasks(),
detect_conflicts(), and recurring-task automation via complete_task().
"""

from pawpal_system import Owner, Pet, Task, Scheduler


def print_schedule(owner: Owner, plans: dict[str, list[dict]]):
    print(f"===== Today's Schedule for {owner.name} =====")
    print(f"Time available: {owner.time_available} min "
          f"(split evenly across {len(owner.pets)} pets)\n")

    for pet_name, plan in plans.items():
        print(f"--- {pet_name} ---")
        if not plan:
            print("  No tasks scheduled (no time budget or no tasks).\n")
            continue

        for entry in plan:
            task: Task = entry["task"]
            print(f"  [{entry['start_time']}] {task.description} "
                  f"({task.duration_min} min, priority {task.priority})")
            print(f"      -> {entry['reason']}")
        print()


def print_tasks(label: str, tasks: list[Task]):
    print(f"--- {label} ---")
    if not tasks:
        print("  (none)\n")
        return
    for t in tasks:
        due = t.due_time or "no due_time"
        print(f"  [{due}] {t.description} (priority {t.priority}, "
              f"completed={t.completed})")
    print()


def main():
    owner = Owner(name="Dawit", time_available=90)

    rex = Pet(name="Rex", species="dog", breed="Labrador")
    # Added deliberately OUT OF ORDER by due_time, to prove sort_by_time works.
    rex.add_task(Task("Breakfast", "feeding", priority=4, duration_min=10,
                       due_date="2026-07-07", due_time="08:30"))
    rex.add_task(Task("Morning walk", "walk", priority=5, duration_min=30,
                       due_date="2026-07-07", due_time="08:00"))
    rex.add_task(Task("Brushing", "grooming", priority=2, duration_min=20,
                       due_date="2026-07-07", due_time="09:00"))
    rex.add_task(Task("Evening meds", "meds", priority=5, duration_min=5,
                       due_date="2026-07-07", due_time="20:00", frequency="daily"))

    luna = Pet(name="Luna", species="cat")
    # Luna's feeding is intentionally set to the SAME due_time as Rex's walk,
    # to trigger a cross-pet conflict warning below.
    luna.add_task(Task("Wet food feeding", "feeding", priority=5, duration_min=10,
                        due_date="2026-07-07", due_time="08:00"))
    luna.add_task(Task("Laser pointer playtime", "enrichment", priority=3, duration_min=15,
                        due_date="2026-07-07", due_time="08:10"))

    owner.add_pet(rex)
    owner.add_pet(luna)

    scheduler = Scheduler()

    # ---- Phase 2: per-pet plan generation ----
    plans = scheduler.generate_all_plans(owner)
    print_schedule(owner, plans)

    # ---- Phase 4, Step 2: sorting ----
    print("===== Sorting: Rex's tasks by due_time (added out of order) =====\n")
    print_tasks("Rex's tasks, unsorted (insertion order)", rex.tasks)
    print_tasks("Rex's tasks, sorted by due_time", scheduler.sort_by_time(rex.tasks))

    # ---- Phase 4, Step 2: filtering ----
    print("===== Filtering =====\n")
    print_tasks("All incomplete tasks, across every pet",
                scheduler.filter_tasks(owner, completed=False))
    print_tasks("All of Luna's tasks",
                scheduler.filter_tasks(owner, pet_name="Luna"))

    # ---- Phase 4, Step 4: conflict detection ----
    print("===== Conflict Detection =====\n")
    conflicts = scheduler.detect_conflicts(owner)
    if conflicts:
        for warning in conflicts:
            print(f"  {warning}")
    else:
        print("  No conflicts detected.")
    print()

    # ---- Phase 4, Step 3: recurring tasks ----
    print("===== Recurring Tasks =====\n")
    evening_meds = rex.tasks[-1]  # "Evening meds", frequency="daily"
    print(f"Completing '{evening_meds.description}' "
          f"(due {evening_meds.due_date}, frequency={evening_meds.frequency})...")
    next_task = scheduler.complete_task(rex, evening_meds)
    if next_task:
        print(f"  -> New occurrence auto-created: due {next_task.due_date} "
              f"at {next_task.due_time}, completed={next_task.completed}")
    else:
        print("  -> No new occurrence created (task doesn't recur).")
    print(f"Rex now has {len(rex.tasks)} tasks (was 4 before completion).\n")


if __name__ == "__main__":
    main()
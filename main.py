"""
main.py
Temporary testing ground for PawPal+'s logic layer.
Creates an Owner with two Pets and several Tasks, runs the Scheduler,
and prints a readable "Today's Schedule" to the terminal.
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


def main():
    owner = Owner(name="Dawit", time_available=90)

    rex = Pet(name="Rex", species="dog", breed="Labrador")
    rex.add_task(Task("Morning walk", "walk", priority=5, duration_min=30))
    rex.add_task(Task("Breakfast", "feeding", priority=4, duration_min=10))
    rex.add_task(Task("Brushing", "grooming", priority=2, duration_min=20))

    luna = Pet(name="Luna", species="cat")
    luna.add_task(Task("Wet food feeding", "feeding", priority=5, duration_min=10))
    luna.add_task(Task("Laser pointer playtime", "enrichment", priority=3, duration_min=15))

    owner.add_pet(rex)
    owner.add_pet(luna)

    scheduler = Scheduler()
    plans = scheduler.generate_all_plans(owner)

    print_schedule(owner, plans)


if __name__ == "__main__":
    main()

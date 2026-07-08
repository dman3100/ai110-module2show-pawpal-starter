"""
tests/test_pawpal.py
Test suite for PawPal+'s logic layer.

Phase 2: core Task/Pet behavior.
Phase 5: sorting, recurrence, conflict detection, filtering, and edge cases.
"""

from pawpal_system import Owner, Pet, Task, Scheduler


# ---------- Phase 2: core class behavior ----------

def test_mark_complete_changes_status():
    """mark_complete() should flip a Task's completed flag from False to True."""
    task = Task("Morning walk", "walk", priority=5, duration_min=30)
    assert task.completed is False

    task.mark_complete()

    assert task.completed is True


def test_add_task_increases_pet_task_count():
    """add_task() should increase the pet's task count by one."""
    pet = Pet(name="Rex", species="dog")
    assert len(pet.tasks) == 0

    pet.add_task(Task("Breakfast", "feeding", priority=4, duration_min=10))

    assert len(pet.tasks) == 1


# ---------- Phase 5: sorting ----------

def test_sort_by_time_orders_chronologically():
    """sort_by_time() should return tasks earliest-due_time first."""
    scheduler = Scheduler()
    tasks = [
        Task("Brushing", "grooming", priority=2, duration_min=20, due_time="09:00"),
        Task("Morning walk", "walk", priority=5, duration_min=30, due_time="08:00"),
        Task("Breakfast", "feeding", priority=4, duration_min=10, due_time="08:30"),
    ]

    sorted_tasks = scheduler.sort_by_time(tasks)

    assert [t.description for t in sorted_tasks] == [
        "Morning walk", "Breakfast", "Brushing"
    ]


def test_sort_by_time_places_tasks_without_due_time_last():
    """A task with due_time=None shouldn't crash the sort or be treated as earliest."""
    scheduler = Scheduler()
    tasks = [
        Task("No time set", "walk", priority=3, duration_min=10, due_time=None),
        Task("Morning walk", "walk", priority=5, duration_min=30, due_time="08:00"),
    ]

    sorted_tasks = scheduler.sort_by_time(tasks)

    assert sorted_tasks[0].description == "Morning walk"
    assert sorted_tasks[1].description == "No time set"


# ---------- Phase 5: recurrence ----------

def test_completing_daily_task_creates_next_day_occurrence():
    """complete_task() on a 'daily' task should mark it done AND spawn a new
    incomplete task due exactly one day later."""
    scheduler = Scheduler()
    pet = Pet(name="Rex", species="dog")
    meds = Task("Evening meds", "meds", priority=5, duration_min=5,
                due_date="2026-07-07", due_time="20:00", frequency="daily")
    pet.add_task(meds)

    next_task = scheduler.complete_task(pet, meds)

    assert meds.completed is True
    assert next_task is not None
    assert next_task.due_date == "2026-07-08"
    assert next_task.completed is False
    assert len(pet.tasks) == 2


def test_completing_non_recurring_task_creates_no_new_task():
    """complete_task() on a task with frequency=None should mark it done
    but must NOT spawn a new occurrence."""
    scheduler = Scheduler()
    pet = Pet(name="Rex", species="dog")
    walk = Task("Morning walk", "walk", priority=5, duration_min=30,
                due_date="2026-07-07", due_time="08:00")  # frequency defaults to None
    pet.add_task(walk)

    next_task = scheduler.complete_task(pet, walk)

    assert walk.completed is True
    assert next_task is None
    assert len(pet.tasks) == 1


# ---------- Phase 5: conflict detection ----------

def test_detect_conflicts_flags_duplicate_times_across_pets():
    """Two tasks belonging to different pets at the same due_time should
    produce exactly one warning naming both."""
    scheduler = Scheduler()
    owner = Owner(name="Dawit", time_available=90)

    rex = Pet(name="Rex", species="dog")
    rex.add_task(Task("Morning walk", "walk", priority=5, duration_min=30, due_time="08:00"))

    luna = Pet(name="Luna", species="cat")
    luna.add_task(Task("Wet food feeding", "feeding", priority=5, duration_min=10, due_time="08:00"))

    owner.add_pet(rex)
    owner.add_pet(luna)

    warnings = scheduler.detect_conflicts(owner)

    assert len(warnings) == 1
    assert "Morning walk" in warnings[0]
    assert "Wet food feeding" in warnings[0]


def test_detect_conflicts_returns_empty_when_no_overlap():
    """No shared due_times should produce zero warnings, not a false positive."""
    scheduler = Scheduler()
    owner = Owner(name="Dawit", time_available=90)

    rex = Pet(name="Rex", species="dog")
    rex.add_task(Task("Morning walk", "walk", priority=5, duration_min=30, due_time="08:00"))
    rex.add_task(Task("Brushing", "grooming", priority=2, duration_min=20, due_time="09:00"))

    owner.add_pet(rex)

    warnings = scheduler.detect_conflicts(owner)

    assert warnings == []


# ---------- Phase 5: filtering ----------

def test_filter_tasks_by_pet_name():
    """filter_tasks(pet_name=...) should return only that pet's tasks."""
    scheduler = Scheduler()
    owner = Owner(name="Dawit", time_available=90)

    rex = Pet(name="Rex", species="dog")
    rex.add_task(Task("Morning walk", "walk", priority=5, duration_min=30))

    luna = Pet(name="Luna", species="cat")
    luna.add_task(Task("Wet food feeding", "feeding", priority=5, duration_min=10))

    owner.add_pet(rex)
    owner.add_pet(luna)

    results = scheduler.filter_tasks(owner, pet_name="Luna")

    assert len(results) == 1
    assert results[0].description == "Wet food feeding"


def test_filter_tasks_by_completion_status():
    """filter_tasks(completed=False) should exclude already-completed tasks."""
    scheduler = Scheduler()
    owner = Owner(name="Dawit", time_available=90)

    rex = Pet(name="Rex", species="dog")
    done_task = Task("Breakfast", "feeding", priority=4, duration_min=10)
    done_task.mark_complete()
    pending_task = Task("Morning walk", "walk", priority=5, duration_min=30)
    rex.add_task(done_task)
    rex.add_task(pending_task)
    owner.add_pet(rex)

    results = scheduler.filter_tasks(owner, completed=False)

    assert len(results) == 1
    assert results[0].description == "Morning walk"


# ---------- Phase 5: edge cases ----------

def test_generate_plan_with_no_tasks_returns_empty_list():
    """A pet with zero tasks should produce an empty plan, not an error."""
    scheduler = Scheduler()
    pet = Pet(name="Ghost", species="dog")

    plan = scheduler.generate_plan(pet, time_budget=90)

    assert plan == []

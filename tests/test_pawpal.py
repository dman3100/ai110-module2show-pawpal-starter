"""
tests/test_pawpal.py
Quick tests for PawPal+'s logic layer, per Phase 2 Step 3.
"""

from pawpal_system import Pet, Task


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

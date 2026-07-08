# PawPal+ (Module 2 Project)

You are building **PawPal+**, a Streamlit app that helps a pet owner plan care tasks for their pet.

## Scenario

A busy pet owner needs help staying consistent with pet care. They want an assistant that can:

- Track pet care tasks (walks, feeding, meds, enrichment, grooming, etc.)
- Consider constraints (time available, priority, owner preferences)
- Produce a daily plan and explain why it chose that plan

Your job is to design the system first (UML), then implement the logic in Python, then connect it to the Streamlit UI.

## What you will build

Your final app should:

- Let a user enter basic owner + pet info
- Let a user add/edit tasks (duration + priority at minimum)
- Generate a daily schedule/plan based on constraints and priorities
- Display the plan clearly (and ideally explain the reasoning)
- Include tests for the most important scheduling behaviors

## Features

- Per-pet daily scheduling: Scheduler.generate_plan() greedily selects tasks by priority (higher = more urgent), breaking ties by shorter duration first, and skips any task that would overflow the remaining time budget.
- Sorting by time: Scheduler.sort_by_time() orders tasks chronologically by due_time; tasks with no due_time sort last rather than crashing the sort.
- Filtering: Scheduler.filter_tasks() filters across every pet an owner has, by pet name and/or completion status.
- Conflict warnings: Scheduler.detect_conflicts() flags two or more tasks (same pet or different pets) sharing an identical due_time, surfaced live in the UI. Exact-match only, not overlap-aware (see reflection.md 2b).
- Daily/weekly recurrence: Task.next_occurrence() + Scheduler.complete_task() automatically spawn the next occurrence of a recurring task when marked complete, advancing due_date via timedelta.

## Getting started

### Setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Suggested workflow

1. Read the scenario carefully and identify requirements and edge cases.
2. Draft a UML diagram (classes, attributes, methods, relationships).
3. Convert UML into Python class stubs (no logic yet).
4. Implement scheduling logic in small increments.
5. Add tests to verify key behaviors.
6. Connect your logic to the Streamlit UI in `app.py`.
7. Refine UML so it matches what you actually built.

## 🖥️ Sample Output

Output from running `python3 main.py`, which builds an Owner with two Pets (Rex the dog, Luna the cat) and five Tasks, then generates a per-pet schedule via `Scheduler.generate_all_plans()`:

```
(base) dman3100@Dawits-MacBook-Pro ai110-module2show-pawpal-starter % python3 main.py
===== Today's Schedule for Dawit =====
Time available: 90 min (split evenly across 2 pets)

--- Rex ---
  [08:00] Morning walk (30 min, priority 5)
      -> Priority 5 walk task (30 min) fits in the 45 min remaining for Rex.
  [08:30] Breakfast (10 min, priority 4)
      -> Priority 4 feeding task (10 min) fits in the 15 min remaining for Rex.

--- Luna ---
  [08:00] Wet food feeding (10 min, priority 5)
      -> Priority 5 feeding task (10 min) fits in the 45 min remaining for Luna.
  [08:10] Laser pointer playtime (15 min, priority 3)
      -> Priority 3 enrichment task (15 min) fits in the 35 min remaining for Luna.
```

Note: Rex's third task ("Brushing," 20 min, priority 2) is intentionally not scheduled — after the walk and breakfast, only 5 of his 45-minute budget remain, which isn't enough for a 20-minute task. This demonstrates the scheduler's priority-based tradeoff: lower-priority tasks are dropped when time runs out rather than force-fit or overlapping with higher-priority ones.

## 📐 Smarter Scheduling

| Feature | Method(s) | Notes |
|---------|-----------|-------|
| Task sorting | `Scheduler.sort_by_time()` | Sorts tasks by `due_time` ("HH:MM"), earliest first; tasks with no due_time sort last. |
| Filtering | `Scheduler.filter_tasks()` | Filters across all of an owner's pets by pet name and/or completion status. |
| Conflict handling | `Scheduler.detect_conflicts()` | Flags tasks (same pet or different pets) sharing an identical due_time; returns warning strings instead of crashing. Exact-match only, not overlap-aware (see reflection.md 2b). |
| Recurring tasks | `Task.next_occurrence()` + `Scheduler.complete_task()` | On completing a "daily"/"weekly" task, automatically creates and attaches the next occurrence with `due_date` advanced via `timedelta`. |

## Demo Walkthrough

Main UI features: enter owner name and daily time budget; enter a pet's name and species; add tasks with a title, type, duration, priority, and due time; view the current task list sorted chronologically; see live conflict warnings if two tasks share a due time; generate a daily schedule that shows what's scheduled (with start time and reasoning) and what got excluded for lack of time.

Example workflow:
1. Enter owner name ("Dawit") and time available (90 min).
2. Add a pet ("Rocky", species "dog").
3. Add several tasks with different priorities, durations, and due times, e.g. a high-priority feeding, a medium-priority walk, a low-priority vet visit.
4. If two tasks share a due time, a warning appears immediately above the task table.
5. Click "Generate schedule" to see the ordered plan, each entry's start time and reasoning, and a separate list of any tasks that didn't fit the time budget.

Key Scheduler behaviors demonstrated: priority-based ordering with tie-breaking by duration, time-budget-aware exclusion (with excluded tasks explicitly surfaced instead of silently dropped), and live conflict detection across a pet's own tasks.

Sample CLI output from python3 main.py, showing scheduling, sorting, filtering, conflict detection, and recurring-task automation:

```
===== Today's Schedule for Dawit =====
Time available: 90 min (split evenly across 2 pets)

--- Rex ---
  [08:00] Evening meds (5 min, priority 5)
      -> Priority 5 meds task (5 min) fits in the 45 min remaining for Rex.
  [08:05] Morning walk (30 min, priority 5)
      -> Priority 5 walk task (30 min) fits in the 40 min remaining for Rex.
  [08:35] Breakfast (10 min, priority 4)
      -> Priority 4 feeding task (10 min) fits in the 10 min remaining for Rex.

--- Luna ---
  [08:00] Wet food feeding (10 min, priority 5)
      -> Priority 5 feeding task (10 min) fits in the 45 min remaining for Luna.
  [08:10] Laser pointer playtime (15 min, priority 3)
      -> Priority 3 enrichment task (15 min) fits in the 35 min remaining for Luna.

===== Sorting: Rex's tasks by due_time (added out of order) =====

--- Rex's tasks, sorted by due_time ---
  [08:00] Morning walk (priority 5, completed=False)
  [08:30] Breakfast (priority 4, completed=False)
  [09:00] Brushing (priority 2, completed=False)
  [20:00] Evening meds (priority 5, completed=False)

===== Conflict Detection =====

  ⚠ Conflict at 08:00: Rex's 'Morning walk', Luna's 'Wet food feeding' are all scheduled at the same time.

===== Recurring Tasks =====

Completing 'Evening meds' (due 2026-07-07, frequency=daily)...
  -> New occurrence auto-created: due 2026-07-08 at 20:00, completed=False
Rex now has 5 tasks (was 4 before completion).
```

## Testing PawPal+

**Coverage:**
- Core class behavior: task completion, pet task-count tracking
- Sorting: chronological ordering by `due_time`, including tasks with no `due_time` set
- Recurrence: completing a "daily" task correctly spawns a next-day occurrence; completing a non-recurring task correctly does *not*
- Conflict detection: duplicate `due_time` across different pets is flagged; non-overlapping times produce no false positives
- Filtering: by pet name and by completion status, independently
- Edge case: a pet with zero tasks produces an empty plan instead of erroring

Output:
(base) dman3100@Dawits-MacBook-Pro ai110-module2show-pawpal-starter % grep -c "^def test_" tests/test_pawpal.py

11
(base) dman3100@Dawits-MacBook-Pro ai110-module2show-pawpal-starter % python -m pytest -v
============================= test session starts ==============================
platform darwin -- Python 3.13.5, pytest-8.3.4, pluggy-1.5.0 -- /opt/anaconda3/bin/python
cachedir: .pytest_cache
rootdir: /Users/dman3100/ai110-module2show-pawpal-starter
plugins: anyio-4.7.0
collected 11 items                                                             

tests/test_pawpal.py::test_mark_complete_changes_status PASSED           [  9%]
tests/test_pawpal.py::test_add_task_increases_pet_task_count PASSED      [ 18%]
tests/test_pawpal.py::test_sort_by_time_orders_chronologically PASSED    [ 27%]
tests/test_pawpal.py::test_sort_by_time_places_tasks_without_due_time_last PASSED [ 36%]
tests/test_pawpal.py::test_completing_daily_task_creates_next_day_occurrence PASSED [ 45%]
tests/test_pawpal.py::test_completing_non_recurring_task_creates_no_new_task PASSED [ 54%]
tests/test_pawpal.py::test_detect_conflicts_flags_duplicate_times_across_pets PASSED [ 63%]
tests/test_pawpal.py::test_detect_conflicts_returns_empty_when_no_overlap PASSED [ 72%]
tests/test_pawpal.py::test_filter_tasks_by_pet_name PASSED               [ 81%]
tests/test_pawpal.py::test_filter_tasks_by_completion_status PASSED      [ 90%]
tests/test_pawpal.py::test_generate_plan_with_no_tasks_returns_empty_list PASSED [100%]

============================== 11 passed in 0.02s ==============================

**Confidence Level:** ⭐⭐⭐☆☆ (3/5)
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

## 🧪 Testing PawPal+

```bash
# Run the full test suite:
pytest

# Run with coverage:
pytest --cov
```

Sample test output:

```
============================= test session starts ==============================
platform darwin -- Python 3.13.5, pytest-8.3.4, pluggy-1.5.0 -- /opt/anaconda3/bin/python3
cachedir: .pytest_cache
rootdir: /Users/dman3100/ai110-module2show-pawpal-starter
plugins: anyio-4.7.0
collected 2 items

tests/test_pawpal.py::test_mark_complete_changes_status PASSED           [ 50%]
tests/test_pawpal.py::test_add_task_increases_pet_task_count PASSED      [100%]

============================== 2 passed in 0.03s ===============================
```

## 📐 Smarter Scheduling

> Fill in once you've implemented scheduling logic.

| Feature | Method(s) | Notes |
|---------|-----------|-------|
| Task sorting | | e.g., by priority, duration |
| Filtering | | e.g., skip tasks if time runs out |
| Conflict handling | | e.g., overlapping time slots |
| Recurring tasks | | e.g., daily vs. weekly |

## 📸 Demo Walkthrough

Describe your app in numbered steps so a reader can follow along without watching a video:

1. <!-- Describe this step -->
2. <!-- Describe this step -->
3. <!-- Describe this step -->
4. <!-- Describe this step -->
5. <!-- Add more steps as needed -->

**Screenshot or video** *(optional)*: <!-- Insert a screenshot or link to a demo video here -->

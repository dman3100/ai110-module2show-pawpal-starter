# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**

- Briefly describe your initial UML design.
- What classes did you include, and what responsibilities did you assign to each?

My initial design had four classes: Owner, Pet, Task, and Scheduler. Owner holds the user's name, their pets, available time, and preferences, with an add_pet() method. Pet holds a name, species, and its list of tasks, with add_task() to attach new ones. Task represents a single care activity — description, type, priority, duration, and completion status — with mark_complete() to update it. Scheduler was originally designed to take an Owner and generate one combined daily plan across all their pets, along with a separate method to explain why it made the choices it did.

**b. Design changes**

- Did your design change during implementation?
- If yes, describe at least one change and why you made it.

My design did change in the fact that upon implementing Scheduler.generate_plan() to return a combined single plan for the owner and all their pets, I realized that could be revised better to have different plans for each unique pet, since care needs are different among different breeds and pets. So I decided to split the plan for the owner into smaller pieces with an equal amount of time set for each pet they own. I changed Scheduler to build one plan per pet instead. generate_plan(pet, time_budget) for a single pet, plus generate_all_plans(owner) as a wrapper that loops through all of the owner's pets. I also added a breed field to Pet, since breed differences are the actual reason per-pet plans matter. I made breed optional because not every species in the app has a meaningful breed, so it just defaults to None instead of having to be required.

When I reviewed the skeleton with AI there were two gaps. Task had no field for when a task happens, even though the required sample output format shows timestamps, and generate_plan() / explain_plan() were separate methods with no shared state that connects them. So I collapsed both into generate_plan() returning a list of dicts (task, start_time, and reason together) instead of a bare list of Task objects, since that keeps the plan and its explanation from  getting out of sync.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?

When a task's duration goes over the remaining time budget, the scheduler correctly excludes it (I tested it with an 80-minute grooming task against a 70-minute remaining window) but the UI only displays the tasks that made the cut, with no explanation shown for why an excluded task didn't appear. I've taken this into account, and full compliance with the "explain the plan" requirement should include explaining exclusions, not just inclusions.

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

For brainstorming, I had a few ideas as to how to structure the UML and code design, and the AI helped me get to the bottom of them to see which I should implement and its suggestions for what to drop. Whenever there was a concept I didn't understand it assisted me in answering questions I had about the code itself and why certain errors and bugs in my code occured.

Prompts that ask to explain code structure helped a lot because it helped me to gain perspective on how pieces of code are interconnected.

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

In terms of compatability, the coding assistant I used was out of sync for files and information and it assumed things that weren't true. Updating it every now and then was quite tedious. I verified by checking its suggestions against the code I had and decided from there.

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

I tested 11 different things:

test_mark_complete_changes_status/test_add_task_increases_pet_task_count — baseline object behavior from Phase 2.

test_sort_by_time_orders_chronologically — confirms sort_by_time() actually reorders tasks by due_time, not just returns them unchanged.

test_sort_by_time_places_tasks_without_due_time_last — confirms a task with due_time=None doesn't crash the sort or get treated as "earliest."

test_completing_daily_task_creates_next_day_occurrence — confirms complete_task() on a recurring task both marks it done and spawns a correct date of the next occurrence.

test_completing_non_recurring_task_creates_no_new_task — the negative case: confirms a one-off task does not spawn a duplicate when completed.

test_detect_conflicts_flags_duplicate_times_across_pets — It confirms that two different pets' tasks at the same time get flagged.

test_detect_conflicts_returns_empty_when_no_overlap — the negative case: confirms no false positives when nothing actually conflicts.

test_filter_tasks_by_pet_name / test_filter_tasks_by_completion_status — Confirms whether filtering works on each axis independently.

test_generate_plan_with_no_tasks_returns_empty_list — Confirms a pet with no tasks returns [] instead of going into an error.

Each algorithmic feature (sort, recurrence, conflicts, filter) received two tests that examine whether it works and also whether it does nothing when it shouldn't.

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

I'm decently confident that it works, I tested it myself and went through some bugs. But I don't feel fully sure since there are edge cases that would still need to be looked at. 

Some edge cases to test would be: Testing for duration overlap conflicts(ex. an 08:00–08:30 task and an 08:15 task wouldn't be flagged), checking for weekly recurrences, and recurring task chains that complete the newly spawned occurence again to confirm the app iterates correctly across multiple cycles.

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

I'm most satisfied with the pace at which the AI went through to keep up. 

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

If I had more time I would attempt to make the app more pleasing in terms of looks. It looks basic for now. Also there isn't a feature to edit or delete tasks before you generate a schedule which I'd implement as a crucial feature.

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?

THe biggest thing I learned is that up to date information is very important, or it can delay efficient production. The best system design doesn't come from the basics necessarily(though it's the backbone), but rather the innovation of the mind. Beyond the AI's scope there were things I wanted to implement. Had I given myself the time better it would've worked for the better.

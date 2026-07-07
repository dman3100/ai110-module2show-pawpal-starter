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

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?

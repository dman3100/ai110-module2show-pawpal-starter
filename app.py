import streamlit as st
from datetime import time
from pawpal_system import Owner, Pet, Task, Scheduler

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

st.title("🐾 PawPal+")

st.markdown(
    """
Welcome to the PawPal+ starter app.

Use this app as your interactive demo once your backend classes/functions exist.
"""
)

with st.expander("Scenario", expanded=True):
    st.markdown(
        """
**PawPal+** is a pet care planning assistant. It helps a pet owner plan care tasks
for their pet(s) based on constraints like time, priority, and preferences.

You will design and implement the scheduling logic and connect it to this Streamlit UI.
"""
    )

with st.expander("What you need to build", expanded=True):
    st.markdown(
        """
At minimum, your system should:
- Represent pet care tasks (what needs to happen, how long it takes, priority)
- Represent the pet and the owner (basic info and preferences)
- Build a plan/schedule for a day that chooses and orders tasks based on constraints
- Explain the plan (why each task was chosen and when it happens)
"""
    )

st.divider()

st.subheader("Quick Demo Inputs")
owner_name = st.text_input("Owner name", value="Jordan")
time_available = st.number_input(
    "Time available today (minutes)", min_value=1, max_value=600, value=90
)
pet_name = st.text_input("Pet name", value="Mochi")
species = st.selectbox("Species", ["dog", "cat", "other"])

if "owner" not in st.session_state:
    new_owner = Owner(name=owner_name, time_available=time_available)
    new_pet = Pet(name=pet_name, species=species)
    new_owner.add_pet(new_pet)
    st.session_state.owner = new_owner
    st.session_state.pet = new_pet
    st.session_state.scheduler = Scheduler()

owner = st.session_state.owner
pet = st.session_state.pet
scheduler = st.session_state.scheduler

owner.name = owner_name
owner.time_available = time_available
pet.name = pet_name
pet.species = species

st.markdown("### Tasks")
st.caption(f"Add tasks for {pet.name}. These feed directly into the scheduler.")

col1, col2, col3, col4, col5 = st.columns(5)
with col1:
    task_title = st.text_input("Task title", value="Morning walk")
with col2:
    task_type = st.selectbox(
        "Task type", ["walk", "feeding", "meds", "enrichment", "grooming"]
    )
with col3:
    duration = st.number_input("Duration (minutes)", min_value=1, max_value=240, value=20)
with col4:
    priority_label = st.selectbox("Priority", ["low", "medium", "high"], index=2)
with col5:
    due_time_input = st.time_input("Due time", value=time(8, 0))

# NOTE: mapping assumes existing "higher int = more urgent" convention,
# confirmed against the official README's Rex/Luna sample output.
PRIORITY_MAP = {"low": 1, "medium": 2, "high": 3}

if st.button("Add task"):
    pet.add_task(
        Task(
            description=task_title,
            task_type=task_type,
            priority=PRIORITY_MAP[priority_label],
            duration_min=int(duration),
            due_time=due_time_input.strftime("%H:%M"),
        )
    )

if pet.tasks:
    sorted_tasks = scheduler.sort_by_time(pet.tasks)
    st.write("Current tasks (sorted by due time):")
    st.table(
        [
            {
                "due_time": t.due_time,
                "title": t.description,
                "type": t.task_type,
                "duration_min": t.duration_min,
                "priority": t.priority,
            }
            for t in sorted_tasks
        ]
    )
else:
    st.info("No tasks yet. Add one above.")

# Conflict warnings -- shown immediately as tasks are added, not just at
# schedule-generation time, since a pet owner benefits from knowing about a
# scheduling collision as soon as it exists, not after building a full plan.
conflicts = scheduler.detect_conflicts(owner)
for warning in conflicts:
    st.warning(warning)

st.divider()

st.subheader("Build Schedule")

if st.button("Generate schedule"):
    plan = scheduler.generate_plan(pet, owner.time_available)
    scheduled_ids = {id(entry["task"]) for entry in plan}
    skipped = [t for t in pet.tasks if id(t) not in scheduled_ids]

    if not plan:
        st.warning("No tasks could be scheduled within the time budget.")
    else:
        st.success(f"Schedule generated for {pet.name}!")
        for entry in plan:
            task: Task = entry["task"]
            st.markdown(
                f"**[{entry['start_time']}]** {task.description} "
                f"({task.duration_min} min, priority {task.priority})"
            )
            st.caption(entry["reason"])

    if skipped:
        st.markdown("**Not scheduled today:**")
        for task in skipped:
            st.caption(
                f"⏭️ {task.description} ({task.duration_min} min, priority "
                f"{task.priority}) didn't fit in the remaining time budget."
            )
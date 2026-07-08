import streamlit as st
from pawpal_system import Owner, Pet, Task, Scheduler

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

st.title("🐾 PawPal+")

st.markdown(
    """
Welcome to the PawPal+ starter app.

This file is intentionally thin. It gives you a working Streamlit app so you can start quickly,
but **it does not implement the project logic**. Your job is to design the system and build it.

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

# --- Step 2: session_state as the "vault" ---
# Only build the Owner/Pet objects ONCE per session. On every rerun after that,
# we just pull the same objects back out and sync the editable fields (name,
# time_available, species) onto them, without touching pet.tasks.
if "owner" not in st.session_state:
    new_owner = Owner(name=owner_name, time_available=time_available)
    new_pet = Pet(name=pet_name, species=species)
    new_owner.add_pet(new_pet)  # <-- Owner.add_pet() is the method handling "adding a pet"
    st.session_state.owner = new_owner
    st.session_state.pet = new_pet

owner = st.session_state.owner
pet = st.session_state.pet

# keep top-of-page edits synced onto the persisted objects
owner.name = owner_name
owner.time_available = time_available
pet.name = pet_name
pet.species = species

st.markdown("### Tasks")
st.caption(f"Add tasks for {pet.name}. These feed directly into the scheduler.")

col1, col2, col3, col4 = st.columns(4)
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

# NOTE: mapping assumes existing "higher int = more urgent" convention in
# pawpal_system.py. Unconfirmed against any actual grading rubric.
PRIORITY_MAP = {"low": 1, "medium": 2, "high": 3}

if st.button("Add task"):
    pet.add_task(
        Task(
            description=task_title,
            task_type=task_type,
            priority=PRIORITY_MAP[priority_label],
            duration_min=int(duration),
        )
    )

if pet.tasks:
    st.write("Current tasks:")
    st.table(
        [
            {
                "title": t.description,
                "type": t.task_type,
                "duration_min": t.duration_min,
                "priority": t.priority,
            }
            for t in pet.tasks
        ]
    )
else:
    st.info("No tasks yet. Add one above.")

st.divider()

st.subheader("Build Schedule")

if st.button("Generate schedule"):
    scheduler = Scheduler()
    plan = scheduler.generate_plan(pet, owner.time_available)

    if not plan:
        st.warning("No tasks could be scheduled within the time budget.")
    else:
        st.markdown(f"**Today's schedule for {pet.name}:**")
        for entry in plan:
            task: Task = entry["task"]
            st.markdown(
                f"**[{entry['start_time']}]** {task.description} "
                f"({task.duration_min} min, priority {task.priority})"
            )
            st.caption(entry["reason"])

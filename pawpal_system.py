"""
pawpal_system.py
Logic layer for PawPal+. Phase 1 skeleton -- attributes and method stubs only.
"""

from dataclasses import dataclass, field
from typing import Optional


@dataclass
class Task:
    description: str
    task_type: str
    priority: int
    duration_min: int
    completed: bool = False

    def mark_complete(self):
        pass


@dataclass
class Pet:
    name: str
    species: str
    breed: Optional[str] = None
    tasks: list[Task] = field(default_factory=list)

    def add_task(self, task: Task):
        pass


@dataclass
class Owner:
    name: str
    time_available: int
    preferences: dict = field(default_factory=dict)
    pets: list[Pet] = field(default_factory=list)

    def add_pet(self, pet: Pet):
        pass


class Scheduler:
    def generate_plan(self, pet: Pet, time_budget: int) -> list[dict]:
        # returns [{"task": Task, "start_time": "08:00", "reason": "..."}]
        pass

    def generate_all_plans(self, owner: Owner) -> dict[str, list[dict]]:
        pass

from sqlalchemy.orm import Mapped, mapped_column, relationship
from ..db import db
from datetime import datetime
from sqlalchemy import ForeignKey
from typing import Optional


class Task(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str]
    description: Mapped[str]
    completed_at:Mapped[datetime] = mapped_column(nullable=True)
    goal_id: Mapped[Optional[int]] = mapped_column(ForeignKey("goal.id"), nullable=True)
    goal: Mapped[Optional["Goal"]] = relationship(back_populates="tasks")

    def to_dict(self):
        '''
        return Task instance with a dictionary
        '''
        task = {
            "id":self.id,
            "title":self.title,
            "description":self.description,
            "is_complete":self.completed_at is not None
        }

        if self.goal_id is not None:
            task["goal_id"] = self.goal_id

        return task

    @classmethod
    def from_dict(cls, task_data: dict):
        '''
        Create a Task instance from a dictionary
        '''
        completed_at_value = None
        if task_data.get("is_complete") is True:
            completed_at_value = datetime.now()

        new_task = cls(
            title=task_data["title"],
            description=task_data["description"],
            completed_at=completed_at_value,
            goal_id=task_data.get("goal_id")
        )

        return new_task

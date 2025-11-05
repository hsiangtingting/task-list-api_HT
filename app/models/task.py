from sqlalchemy.orm import Mapped, mapped_column, relationship
from ..db import db
from datetime import datetime
import json

class Task(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str]
    description: Mapped[str]
    completed_at:Mapped[datetime] = mapped_column(nullable=True)
    goals:Mapped[list["Goal"]] = relationship(back_populates="task")

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

        if self.goals:
            task["goals"] = self.goals

        return task

    @classmethod
    def from_dict(cls, task_data: dict):
        '''
        Create a Task instance from a dictionary
        '''
        # title = task_data["title"]
        # description = task_data["description"]
        completed_at_value = None
        if task_data.get("is_complete") is True:
            completed_at_value = datetime.now()

        # Build the Task using the mapped attribute name `completed_at`.
        # If `is_complete` is True we set a timestamp, otherwise None.
        new_task = cls(
            title=task_data["title"],
            description=task_data["description"],
            completed_at=completed_at_value
        )

        return new_task

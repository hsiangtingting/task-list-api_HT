from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import Optional
from ..db import db

class Goal(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str]
    tasks:Mapped[Optional[list["Task"]]] = relationship(back_populates="goal")

    def to_dict(self, include_tasks=False):
        model_dict = {
            "id": self.id,
            "title": self.title,
        }

        if include_tasks :
            model_dict["tasks"] = [task.to_dict() for task in self.tasks]

        return model_dict

    @classmethod
    def from_dict(cls, data_dict):
        return cls(
            title = data_dict["title"],
            tasks = [Task.from_dict(task) for task in data_dict.get("tasks", [])]
            )
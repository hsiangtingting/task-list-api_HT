from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey
from typing import Optional
from ..db import db

class Goal(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str]
    task_id: Mapped[Optional[int]] = mapped_column(ForeignKey("task.id"))
    task: Mapped[Optional["Task"]] = relationship(back_populates="goals")

    def to_dict(self):
        model_dict = {
            "id": self.id,
            "title": self.title,
            "task": self.task.title if self.task_id else None
        }

        return model_dict

    @classmethod
    def from_dict(cls, data_dict):
        return cls(
            title = data_dict["title"],
            task_id = data_dict.get("task_id")
            )
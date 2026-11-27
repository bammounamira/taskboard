from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator


TaskStatus = Literal["todo", "in_progress", "done"]


class TaskBase(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
        str_strip_whitespace=True,
    )


class TaskCreate(TaskBase):
    title: str = Field(min_length=1, max_length=200)
    description: str | None = Field(default=None, max_length=2000)
    status: TaskStatus = "todo"


class TaskUpdate(TaskBase):
    title: str | None = Field(default=None, min_length=1, max_length=200)
    description: str | None = Field(default=None, max_length=2000)
    status: TaskStatus | None = None

    @field_validator("title", "status")
    @classmethod
    def reject_null(cls, value):
        if value is None:
            raise ValueError("title and status cannot be null")
        return value


class Task(TaskCreate):
    id: int
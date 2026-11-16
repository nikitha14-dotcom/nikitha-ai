import datetime
from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime
from backend.app.database import Base

class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False, index=True)
    description = Column(Text, nullable=True)
    status = Column(String, default="todo", index=True)  # todo, in_progress, completed, cancelled
    priority = Column(String, default="medium", index=True)  # low, medium, high, urgent
    deadline = Column(DateTime, nullable=True)
    is_recurring = Column(Boolean, default=False)
    recurrence_rule = Column(String, nullable=True)  # daily, weekly, monthly
    agent_assigned = Column(String, default="personal_assistant")
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    completed_at = Column(DateTime, nullable=True)

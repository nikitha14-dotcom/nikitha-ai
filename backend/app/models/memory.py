import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime, Float
from backend.app.database import Base

class Memory(Base):
    __tablename__ = "memories"

    id = Column(Integer, primary_key=True, index=True)
    category = Column(String, index=True, default="preference")  # preference, project, goal, skill, fact, instruction
    key = Column(String, index=True, nullable=False)
    value = Column(Text, nullable=False)
    confidence = Column(Float, default=1.0)
    source = Column(String, default="conversation")
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

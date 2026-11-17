// backend/app/models/user_settings.py
"""Simple per‑user settings table.
Stores a JSON blob of arbitrary key/value pairs for each user.
"""

import json
from sqlalchemy import Column, Integer, ForeignKey, JSON
from sqlalchemy.orm import relationship
from backend.app.database import Base

class UserSettings(Base):
    __tablename__ = "user_settings"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True, nullable=False)
    settings = Column(JSON, default=dict)

    user = relationship("User", back_populates="settings")

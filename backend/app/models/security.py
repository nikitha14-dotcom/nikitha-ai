import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime, JSON
from backend.app.database import Base

class ActionApproval(Base):
    __tablename__ = "action_approvals"

    id = Column(Integer, primary_key=True, index=True)
    action_type = Column(String, nullable=False, index=True)  # send_email, apply_job, submit_form, delete_file, financial_action
    title = Column(String, nullable=False)
    description = Column(Text, nullable=False)
    agent_name = Column(String, default="orchestrator")
    payload = Column(JSON, default=dict)
    status = Column(String, default="pending", index=True)  # pending, approved, rejected, executed
    decision_notes = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    resolved_at = Column(DateTime, nullable=True)

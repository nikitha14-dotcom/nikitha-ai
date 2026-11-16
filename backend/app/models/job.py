import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime, JSON, Float
from backend.app.database import Base

class JobListing(Base):
    __tablename__ = "job_listings"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False, index=True)
    company = Column(String, nullable=False, index=True)
    location = Column(String, default="Remote / Hybrid")
    job_type = Column(String, default="Full-time")  # Full-time, Internship, Contract
    category = Column(String, default="AI/ML Engineer")  # AI/ML Engineer, Python Developer, Full Stack, Internship
    salary_range = Column(String, nullable=True)
    experience_level = Column(String, default="0-3 years")
    description = Column(Text, nullable=True)
    skills_required = Column(JSON, default=list)
    application_url = Column(String, nullable=True)
    status = Column(String, default="saved")  # saved, applied, interviewing, offered, rejected
    match_score = Column(Float, default=85.0)
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

class ResumeProfile(Base):
    __tablename__ = "resume_profiles"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, default="Master Resume")
    full_name = Column(String, default="Nikitha")
    email = Column(String, default="nikki123kota@gmail.com")
    phone = Column(String, nullable=True)
    linkedin = Column(String, nullable=True)
    github = Column(String, default="https://github.com/nikitha14-dotcom")
    summary = Column(Text, nullable=True)
    skills = Column(JSON, default=list)
    experience = Column(JSON, default=list)
    education = Column(JSON, default=list)
    projects = Column(JSON, default=list)
    ats_score = Column(Float, default=92.0)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

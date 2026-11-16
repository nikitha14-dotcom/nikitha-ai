from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime

# Auth Schemas
class UserCreate(BaseModel):
    email: str
    username: str
    password: str
    full_name: Optional[str] = "Nikitha"

class UserLogin(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: Dict[str, Any]

# Memory Schemas
class MemoryCreate(BaseModel):
    category: str = "preference"
    key: str
    value: str
    confidence: float = 1.0
    source: str = "user"

class MemoryUpdate(BaseModel):
    category: Optional[str] = None
    key: Optional[str] = None
    value: Optional[str] = None

class MemoryResponse(BaseModel):
    id: int
    category: str
    key: str
    value: str
    confidence: float
    source: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

# Task Schemas
class TaskCreate(BaseModel):
    title: str
    description: Optional[str] = None
    priority: str = "medium"
    deadline: Optional[datetime] = None
    is_recurring: bool = False
    recurrence_rule: Optional[str] = None
    agent_assigned: str = "personal_assistant"

class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = None
    priority: Optional[str] = None
    deadline: Optional[datetime] = None
    is_recurring: Optional[bool] = None

class TaskResponse(BaseModel):
    id: int
    title: str
    description: Optional[str]
    status: str
    priority: str
    deadline: Optional[datetime]
    is_recurring: bool
    recurrence_rule: Optional[str]
    agent_assigned: str
    created_at: datetime
    completed_at: Optional[datetime]

    class Config:
        from_attributes = True

# Chat Schemas
class ChatRequest(BaseModel):
    message: str
    conversation_id: Optional[int] = None
    model: Optional[str] = None
    provider: Optional[str] = "auto"
    stream: bool = False

class ChatResponse(BaseModel):
    conversation_id: int
    reply: str
    agent_name: str
    model: str
    action_required: Optional[Dict[str, Any]] = None
    metadata: Optional[Dict[str, Any]] = None

# Voice Schemas
class VoiceProcessRequest(BaseModel):
    transcript: str
    conversation_id: Optional[int] = None
    auto_speak: bool = True

class VoiceProcessResponse(BaseModel):
    transcript: str
    reply: str
    audio_base64: Optional[str] = None
    agent_name: str

# Job & Resume Schemas
class JobSearchQuery(BaseModel):
    query: str = "AI ML Engineer"
    category: Optional[str] = "AI/ML Engineer"
    location: Optional[str] = "India / Remote"
    experience_level: Optional[str] = "All"
    job_type: Optional[str] = "All"

class JobSaveRequest(BaseModel):
    title: str
    company: str
    location: str
    category: str
    salary_range: Optional[str] = None
    experience_level: Optional[str] = None
    description: Optional[str] = None
    skills_required: List[str] = []
    application_url: Optional[str] = None
    match_score: float = 85.0

class ResumeTailorRequest(BaseModel):
    job_title: str
    job_description: str
    current_resume: Optional[Dict[str, Any]] = None

class CoverLetterRequest(BaseModel):
    job_title: str
    company: str
    job_description: str
    candidate_name: str = "Nikitha"

# Approval Schemas
class ApprovalDecision(BaseModel):
    approved: bool
    notes: Optional[str] = None

# Document Schemas
class DocumentGenerateRequest(BaseModel):
    doc_type: str  # "pdf", "docx", "xlsx", "markdown"
    title: str
    topic: str
    sections: List[Dict[str, Any]] = []
    author: str = "NIKITHA.AI"

# Browser Automation Schemas
class BrowserRunRequest(BaseModel):
    url: str
    action: str  # "scrape", "search", "navigate", "fill_form"
    parameters: Dict[str, Any] = {}
    require_confirmation: bool = False

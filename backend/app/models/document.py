# Document and chunk models for RAG

from __future__ import annotations

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean, Text, JSON
from sqlalchemy.orm import relationship
from datetime import datetime
from backend.app.database import Base

class Document(Base):
    __tablename__ = "documents"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    filename = Column(String, nullable=False)
    filepath = Column(String, nullable=False)  # absolute path on server
    uploaded_at = Column(DateTime, default=datetime.utcnow)
    processed = Column(Boolean, default=False)
    # optional metadata (e.g., page count)
    meta_data = Column('metadata', JSON, nullable=True)

    @property
    def metadata(self) -> dict | None:
        return self.meta_data

    @metadata.setter
    def metadata(self, value):
        self.meta_data = value

    # relationship to owner
    user = relationship("User", back_populates="documents")
    chunks = relationship("DocumentChunk", back_populates="document", cascade="all, delete-orphan")

class DocumentChunk(Base):
    __tablename__ = "document_chunks"

    id = Column(Integer, primary_key=True, index=True)
    document_id = Column(Integer, ForeignKey("documents.id"), nullable=False, index=True)
    page_number = Column(Integer, nullable=True)  # optional page reference
    chunk_index = Column(Integer, nullable=False)  # order in document
    text = Column(Text, nullable=False)
    # store embedding as JSON list of floats for simplicity
    embedding = Column(JSON, nullable=True)

    document = relationship("Document", back_populates="chunks")

# Extend User model with relationship (imported lazily to avoid circular import)
from backend.app.models.user import User  # noqa: E402
User.documents = relationship("Document", back_populates="user", cascade="all, delete-orphan")

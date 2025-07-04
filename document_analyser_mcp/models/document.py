from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class Document(BaseModel):
    """Document model for storing text documents with metadata"""
    document_id: str = Field(..., description="Unique identifier for the document")
    title: str = Field(..., description="Document title")
    author: str = Field(..., description="Document author")
    created_at: str = Field(..., description="Creation date in YYYY-MM-DD format")
    category: str = Field(default="general", description="Document category")
    text: str = Field(..., description="Document content text")

class DocumentCreate(BaseModel):
    """Model for creating new documents"""
    title: str = Field(..., description="Document title")
    author: str = Field(..., description="Document author")
    text: str = Field(..., description="Document content text")
    created_at: Optional[str] = Field(None, description="Creation date (auto-generated if not provided)")
    category: str = Field(default="general", description="Document category")

class DocumentSummary(BaseModel):
    """Simplified document model for search results"""
    document_id: str
    title: str
    author: str
    category: str
    matched: bool = True

from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime
from enum import Enum

class MeetingType(str, Enum):
    ONE_ON_ONE = "1:1"
    TEAM_MEETING = "team"
    ALL_HANDS = "all_hands"
    STANDUP = "standup"
    REVIEW = "review"
    PLANNING = "planning"
    BRAINSTORMING = "brainstorming"
    INTERVIEW = "interview"

class MeetingStatus(str, Enum):
    SCHEDULED = "scheduled"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    CANCELLED = "cancelled"
    RESCHEDULED = "rescheduled"

class Meeting(BaseModel):
    meeting_id: str = Field(..., description="Unique meeting identifier")
    title: str = Field(..., description="Meeting title")
    description: Optional[str] = Field(None, description="Meeting description")
    participants: List[str] = Field(..., description="List of participant user IDs")
    organizer: str = Field(..., description="Meeting organizer user ID")
    start_time: datetime = Field(..., description="Meeting start time (UTC)")
    end_time: datetime = Field(..., description="Meeting end time (UTC)")
    time_zone: str = Field(..., description="Primary time zone for the meeting")
    meeting_type: MeetingType = Field(..., description="Type of meeting")
    status: MeetingStatus = Field(default=MeetingStatus.SCHEDULED, description="Meeting status")
    location: Optional[str] = Field(None, description="Meeting location (physical or virtual)")
    agenda: List[str] = Field(default_factory=list, description="Meeting agenda items")
    recurring: bool = Field(default=False, description="Is this a recurring meeting")
    recurrence_pattern: Optional[str] = Field(None, description="Recurrence pattern if recurring")
    created_at: datetime = Field(default_factory=datetime.utcnow, description="Creation timestamp")
    updated_at: datetime = Field(default_factory=datetime.utcnow, description="Last update timestamp")
    effectiveness_score: Optional[float] = Field(None, description="Meeting effectiveness score (1-10)")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Additional metadata")

class MeetingCreate(BaseModel):
    title: str = Field(..., description="Meeting title")
    description: Optional[str] = Field(None, description="Meeting description")
    participants: List[str] = Field(..., description="List of participant user IDs")
    duration: int = Field(..., description="Meeting duration in minutes")
    preferences: Dict[str, Any] = Field(default_factory=dict, description="Scheduling preferences")
    meeting_type: MeetingType = Field(default=MeetingType.TEAM_MEETING, description="Type of meeting")
    location: Optional[str] = Field(None, description="Meeting location")
    agenda: List[str] = Field(default_factory=list, description="Meeting agenda items")
    recurring: bool = Field(default=False, description="Is this a recurring meeting")
    recurrence_pattern: Optional[str] = Field(None, description="Recurrence pattern")

class MeetingUpdate(BaseModel):
    title: Optional[str] = Field(None, description="Updated meeting title")
    description: Optional[str] = Field(None, description="Updated meeting description")
    participants: Optional[List[str]] = Field(None, description="Updated participant list")
    start_time: Optional[datetime] = Field(None, description="Updated start time")
    end_time: Optional[datetime] = Field(None, description="Updated end time")
    status: Optional[MeetingStatus] = Field(None, description="Updated meeting status")
    location: Optional[str] = Field(None, description="Updated meeting location")
    agenda: Optional[List[str]] = Field(None, description="Updated agenda items")
    effectiveness_score: Optional[float] = Field(None, description="Updated effectiveness score")
    metadata: Optional[Dict[str, Any]] = Field(None, description="Updated metadata")

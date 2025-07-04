from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime
from enum import Enum

class ConflictType(str, Enum):
    OVERLAP = "overlap"
    BACK_TO_BACK = "back_to_back"
    OUTSIDE_HOURS = "outside_hours"
    LUNCH_CONFLICT = "lunch_conflict"
    OVERLOAD = "overload"
    TRAVEL_TIME = "travel_time"

class TimeSlot(BaseModel):
    start_time: datetime = Field(..., description="Slot start time (UTC)")
    end_time: datetime = Field(..., description="Slot end time (UTC)")
    duration_minutes: int = Field(..., description="Duration in minutes")
    available_participants: List[str] = Field(..., description="Available participant IDs")
    unavailable_participants: List[str] = Field(default_factory=list, description="Unavailable participant IDs")

class ConflictDetection(BaseModel):
    user_id: str = Field(..., description="User ID with conflict")
    conflict_type: ConflictType = Field(..., description="Type of conflict")
    conflicting_meeting_id: Optional[str] = Field(None, description="ID of conflicting meeting")
    conflict_time: datetime = Field(..., description="Time of conflict")
    severity: int = Field(..., description="Conflict severity (1-10)")
    description: str = Field(..., description="Human-readable conflict description")
    suggested_resolution: Optional[str] = Field(None, description="Suggested resolution")

class OptimalSlot(BaseModel):
    rank: int = Field(..., description="Ranking of this slot (1 is best)")
    time_slot: TimeSlot = Field(..., description="The time slot details")
    overall_score: float = Field(..., description="Overall optimization score (0-10)")
    productivity_score: float = Field(..., description="Productivity score (0-10)")
    convenience_score: float = Field(..., description="Convenience score (0-10)")
    conflict_risk_score: float = Field(..., description="Conflict risk score (0-10)")
    preference_score: float = Field(..., description="Preference alignment score (0-10)")
    explanation: str = Field(..., description="Human-readable explanation of the score")
    participant_impact: Dict[str, Dict[str, Any]] = Field(..., description="Impact on each participant")
    reasoning: Dict[str, Any] = Field(..., description="Detailed scoring breakdown")

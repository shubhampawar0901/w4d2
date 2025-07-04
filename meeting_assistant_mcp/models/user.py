from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import time
from enum import Enum

class WorkingDays(str, Enum):
    MONDAY = "monday"
    TUESDAY = "tuesday"
    WEDNESDAY = "wednesday"
    THURSDAY = "thursday"
    FRIDAY = "friday"
    SATURDAY = "saturday"
    SUNDAY = "sunday"

class ProductivityPeriod(str, Enum):
    EARLY_MORNING = "early_morning"  # 6-9 AM
    MORNING = "morning"              # 9-12 PM
    AFTERNOON = "afternoon"          # 12-3 PM
    LATE_AFTERNOON = "late_afternoon" # 3-6 PM
    EVENING = "evening"              # 6-9 PM

class UserPreferences(BaseModel):
    time_zone: str = Field(..., description="User's primary time zone")
    working_hours_start: time = Field(..., description="Start of working hours")
    working_hours_end: time = Field(..., description="End of working hours")
    working_days: List[WorkingDays] = Field(..., description="Working days of the week")
    lunch_break_start: Optional[time] = Field(None, description="Lunch break start time")
    lunch_break_end: Optional[time] = Field(None, description="Lunch break end time")
    productive_periods: List[ProductivityPeriod] = Field(..., description="Most productive time periods")
    no_meetings_before: Optional[time] = Field(None, description="No meetings before this time")
    no_meetings_after: Optional[time] = Field(None, description="No meetings after this time")
    meeting_free_blocks: List[str] = Field(default_factory=list, description="Regular meeting-free time blocks")
    max_daily_meetings: int = Field(default=8, description="Maximum meetings per day")
    max_consecutive_meetings: int = Field(default=3, description="Maximum consecutive meetings")
    buffer_time_minutes: int = Field(default=15, description="Buffer time between meetings")
    preferred_meeting_duration: int = Field(default=30, description="Preferred meeting duration in minutes")
    avoid_back_to_back: bool = Field(default=True, description="Avoid back-to-back meetings")

class User(BaseModel):
    user_id: str = Field(..., description="Unique user identifier")
    name: str = Field(..., description="User's full name")
    email: str = Field(..., description="User's email address")
    role: str = Field(..., description="User's role/title")
    department: str = Field(..., description="User's department")
    manager_id: Optional[str] = Field(None, description="Manager's user ID")
    preferences: UserPreferences = Field(..., description="User's scheduling preferences")
    is_active: bool = Field(default=True, description="Is user active")
    created_at: str = Field(..., description="User creation date")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Additional user metadata")

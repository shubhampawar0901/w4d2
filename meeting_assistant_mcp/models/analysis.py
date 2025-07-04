from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime, date
from enum import Enum

class MeetingPattern(str, Enum):
    DAILY_STANDUP = "daily_standup"
    WEEKLY_REVIEW = "weekly_review"
    MONTHLY_PLANNING = "monthly_planning"
    QUARTERLY_REVIEW = "quarterly_review"
    AD_HOC = "ad_hoc"

class ProductivityTrend(str, Enum):
    IMPROVING = "improving"
    DECLINING = "declining"
    STABLE = "stable"
    FLUCTUATING = "fluctuating"

class MeetingAnalysis(BaseModel):
    user_id: str = Field(..., description="User ID being analyzed")
    analysis_period_start: date = Field(..., description="Start of analysis period")
    analysis_period_end: date = Field(..., description="End of analysis period")
    total_meetings: int = Field(..., description="Total number of meetings")
    total_meeting_hours: float = Field(..., description="Total hours in meetings")
    average_daily_meetings: float = Field(..., description="Average meetings per day")
    average_meeting_duration: float = Field(..., description="Average meeting duration in minutes")
    meeting_patterns: List[MeetingPattern] = Field(..., description="Identified meeting patterns")
    productivity_trend: ProductivityTrend = Field(..., description="Overall productivity trend")
    peak_meeting_hours: List[int] = Field(..., description="Hours with most meetings (0-23)")
    meeting_type_distribution: Dict[str, int] = Field(..., description="Distribution by meeting type")
    effectiveness_trend: List[float] = Field(..., description="Weekly effectiveness scores")
    recommendations: List[str] = Field(..., description="Optimization recommendations")
    insights: Dict[str, Any] = Field(..., description="Additional insights")

class WorkloadAnalysis(BaseModel):
    team_members: List[str] = Field(..., description="Team member user IDs")
    analysis_period_start: date = Field(..., description="Start of analysis period")
    analysis_period_end: date = Field(..., description="End of analysis period")
    workload_distribution: Dict[str, Dict[str, Any]] = Field(..., description="Workload per team member")
    overloaded_members: List[str] = Field(..., description="Overloaded team members")
    underutilized_members: List[str] = Field(..., description="Underutilized team members")
    balance_score: float = Field(..., description="Overall balance score (0-10)")
    recommendations: List[str] = Field(..., description="Balancing recommendations")
    optimal_distribution: Dict[str, int] = Field(..., description="Suggested meeting distribution")

class EffectivenessScore(BaseModel):
    meeting_id: str = Field(..., description="Meeting ID being scored")
    overall_score: float = Field(..., description="Overall effectiveness score (1-10)")
    duration_efficiency: float = Field(..., description="Duration efficiency score (1-10)")
    agenda_completion: float = Field(..., description="Agenda completion score (1-10)")
    participant_engagement: float = Field(..., description="Participant engagement score (1-10)")
    outcome_clarity: float = Field(..., description="Outcome clarity score (1-10)")
    follow_up_rate: float = Field(..., description="Follow-up action completion rate (0-1)")
    time_to_decision: Optional[float] = Field(None, description="Time to reach decisions (minutes)")
    improvement_suggestions: List[str] = Field(..., description="Specific improvement suggestions")
    strengths: List[str] = Field(..., description="Meeting strengths")
    weaknesses: List[str] = Field(..., description="Areas for improvement")
    calculated_at: datetime = Field(default_factory=datetime.utcnow, description="Score calculation time")

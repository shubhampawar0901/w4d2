"""
Optimal Time Slot Recommendation Service

This service implements the AI-powered optimal time slot recommendation algorithm
that analyzes multiple factors to suggest the best meeting times for all participants.
"""

from typing import List, Dict, Any, Optional, Tuple
from datetime import datetime, timedelta, time
import pytz
from dataclasses import dataclass
import logging

from ...models.scheduling import OptimalSlot, TimeSlot
from ...models.user import User, ProductivityPeriod
from ..core.calendar_service import CalendarService
from ..core.user_service import UserService

logger = logging.getLogger(__name__)

@dataclass
class ScoreComponents:
    """Components of the optimization score"""
    productivity_score: float
    convenience_score: float
    conflict_risk_score: float
    preference_score: float
    
    @property
    def overall_score(self) -> float:
        """Calculate weighted overall score"""
        return (
            self.productivity_score * 0.4 +
            self.convenience_score * 0.3 +
            self.conflict_risk_score * 0.2 +
            self.preference_score * 0.1
        )

class OptimalTimeService:
    """AI-powered optimal time slot recommendation service"""
    
    def __init__(self, calendar_service: CalendarService, user_service: UserService):
        self.calendar_service = calendar_service
        self.user_service = user_service
        
    async def find_optimal_slots(
        self,
        participants: List[str],
        duration: int,
        date_range: Tuple[datetime, datetime],
        preferences: Optional[Dict[str, Any]] = None
    ) -> List[OptimalSlot]:
        """
        Find optimal time slots for a meeting with given participants
        
        Args:
            participants: List of participant user IDs
            duration: Meeting duration in minutes
            date_range: Tuple of (start_date, end_date) for search range
            preferences: Optional meeting preferences
            
        Returns:
            List of OptimalSlot objects ranked by score
        """
        logger.info(f"Finding optimal slots for {len(participants)} participants, {duration}min duration")
        
        # Get participant data
        users = await self._get_participant_data(participants)
        if not users:
            raise ValueError("No valid participants found")
            
        # Find common availability windows
        availability_windows = await self._find_availability_windows(
            users, duration, date_range
        )
        
        if not availability_windows:
            logger.warning("No common availability windows found")
            return []
            
        # Score each potential time slot
        scored_slots = []
        for window in availability_windows:
            score_components = await self._calculate_slot_score(window, users, duration)
            
            optimal_slot = OptimalSlot(
                rank=0,  # Will be set after sorting
                time_slot=window,
                overall_score=score_components.overall_score,
                productivity_score=score_components.productivity_score,
                convenience_score=score_components.convenience_score,
                conflict_risk_score=score_components.conflict_risk_score,
                preference_score=score_components.preference_score,
                explanation=self._generate_explanation(score_components, users),
                participant_impact=await self._calculate_participant_impact(window, users),
                reasoning=self._generate_detailed_reasoning(score_components)
            )
            
            scored_slots.append(optimal_slot)
            
        # Sort by overall score (descending) and assign ranks
        scored_slots.sort(key=lambda x: x.overall_score, reverse=True)
        for i, slot in enumerate(scored_slots):
            slot.rank = i + 1
            
        # Return top 5 recommendations
        return scored_slots[:5]
        
    async def _get_participant_data(self, participant_ids: List[str]) -> List[User]:
        """Get user data for all participants"""
        users = []
        for user_id in participant_ids:
            user = await self.user_service.get_user(user_id)
            if user:
                users.append(user)
            else:
                logger.warning(f"User {user_id} not found")
        return users
        
    async def _find_availability_windows(
        self,
        users: List[User],
        duration: int,
        date_range: Tuple[datetime, datetime]
    ) -> List[TimeSlot]:
        """Find time windows where all participants are available"""
        start_date, end_date = date_range
        current_date = start_date.date()
        end_date_only = end_date.date()
        
        availability_windows = []
        
        while current_date <= end_date_only:
            # Skip weekends for most users (can be customized)
            if current_date.weekday() >= 5:  # Saturday = 5, Sunday = 6
                current_date += timedelta(days=1)
                continue
                
            # Find overlapping working hours for this date
            daily_windows = await self._find_daily_availability(users, current_date, duration)
            availability_windows.extend(daily_windows)
            
            current_date += timedelta(days=1)
            
        return availability_windows
        
    async def _find_daily_availability(
        self,
        users: List[User],
        date: datetime.date,
        duration: int
    ) -> List[TimeSlot]:
        """Find availability windows for a specific date"""
        # Convert date to datetime for each user's timezone
        daily_windows = []
        
        # Find the intersection of all users' working hours
        common_start = None
        common_end = None
        
        for user in users:
            user_tz = pytz.timezone(user.preferences.time_zone)
            
            # Convert working hours to UTC
            user_start = datetime.combine(date, user.preferences.working_hours_start)
            user_end = datetime.combine(date, user.preferences.working_hours_end)
            
            user_start_utc = user_tz.localize(user_start).astimezone(pytz.UTC)
            user_end_utc = user_tz.localize(user_end).astimezone(pytz.UTC)
            
            if common_start is None or user_start_utc > common_start:
                common_start = user_start_utc
            if common_end is None or user_end_utc < common_end:
                common_end = user_end_utc
                
        if not common_start or not common_end or common_end <= common_start:
            return []
            
        # Generate 30-minute time slots within the common window
        current_time = common_start
        slot_duration = timedelta(minutes=duration)
        
        while current_time + slot_duration <= common_end:
            # Check if all participants are actually free at this time
            all_available = await self._check_availability_at_time(users, current_time, duration)
            
            if all_available:
                time_slot = TimeSlot(
                    start_time=current_time,
                    end_time=current_time + slot_duration,
                    duration_minutes=duration,
                    available_participants=[user.user_id for user in users],
                    unavailable_participants=[]
                )
                daily_windows.append(time_slot)
                
            current_time += timedelta(minutes=30)  # 30-minute increments
            
        return daily_windows
        
    async def _check_availability_at_time(
        self,
        users: List[User],
        start_time: datetime,
        duration: int
    ) -> bool:
        """Check if all users are available at the specified time"""
        end_time = start_time + timedelta(minutes=duration)
        
        for user in users:
            # Check for existing meetings
            user_meetings = await self.calendar_service.get_user_meetings(
                user.user_id, start_time, end_time
            )
            
            if user_meetings:
                return False
                
            # Check lunch break conflicts
            if user.preferences.lunch_break_start and user.preferences.lunch_break_end:
                user_tz = pytz.timezone(user.preferences.time_zone)
                user_local_start = start_time.astimezone(user_tz).time()
                user_local_end = end_time.astimezone(user_tz).time()
                
                lunch_start = user.preferences.lunch_break_start
                lunch_end = user.preferences.lunch_break_end
                
                # Check if meeting overlaps with lunch
                if (user_local_start < lunch_end and user_local_end > lunch_start):
                    return False
                    
        return True
        
    async def _calculate_slot_score(
        self,
        time_slot: TimeSlot,
        users: List[User],
        duration: int
    ) -> ScoreComponents:
        """Calculate comprehensive score for a time slot"""
        
        productivity_score = await self._calculate_productivity_score(time_slot, users)
        convenience_score = await self._calculate_convenience_score(time_slot, users)
        conflict_risk_score = await self._calculate_conflict_risk_score(time_slot, users)
        preference_score = await self._calculate_preference_score(time_slot, users)
        
        return ScoreComponents(
            productivity_score=productivity_score,
            convenience_score=convenience_score,
            conflict_risk_score=conflict_risk_score,
            preference_score=preference_score
        )
        
    async def _calculate_productivity_score(self, time_slot: TimeSlot, users: List[User]) -> float:
        """Calculate productivity score based on users' productive periods"""
        total_score = 0.0
        
        for user in users:
            user_tz = pytz.timezone(user.preferences.time_zone)
            local_time = time_slot.start_time.astimezone(user_tz).time()
            hour = local_time.hour
            
            # Score based on productive periods
            user_score = 5.0  # Base score
            
            for period in user.preferences.productive_periods:
                if period == ProductivityPeriod.EARLY_MORNING and 6 <= hour < 9:
                    user_score = 9.0
                elif period == ProductivityPeriod.MORNING and 9 <= hour < 12:
                    user_score = 9.5
                elif period == ProductivityPeriod.AFTERNOON and 12 <= hour < 15:
                    user_score = 8.5
                elif period == ProductivityPeriod.LATE_AFTERNOON and 15 <= hour < 18:
                    user_score = 8.0
                elif period == ProductivityPeriod.EVENING and 18 <= hour < 21:
                    user_score = 7.0
                    
            total_score += user_score
            
        return min(total_score / len(users), 10.0)
        
    async def _calculate_convenience_score(self, time_slot: TimeSlot, users: List[User]) -> float:
        """Calculate convenience score based on time zones and preferences"""
        total_score = 0.0
        
        for user in users:
            user_tz = pytz.timezone(user.preferences.time_zone)
            local_time = time_slot.start_time.astimezone(user_tz).time()
            hour = local_time.hour
            
            user_score = 8.0  # Base score
            
            # Penalize very early or very late times
            if hour < 8:
                user_score -= (8 - hour) * 1.5
            elif hour > 17:
                user_score -= (hour - 17) * 1.0
                
            # Bonus for preferred times
            if user.preferences.no_meetings_before:
                if local_time < user.preferences.no_meetings_before:
                    user_score -= 3.0
                    
            if user.preferences.no_meetings_after:
                if local_time > user.preferences.no_meetings_after:
                    user_score -= 3.0
                    
            total_score += max(user_score, 1.0)
            
        return min(total_score / len(users), 10.0)
        
    async def _calculate_conflict_risk_score(self, time_slot: TimeSlot, users: List[User]) -> float:
        """Calculate conflict risk score"""
        # This is a simplified implementation
        # In a real system, this would analyze meeting density, buffer times, etc.
        base_score = 8.0
        
        # Check for meetings close to this time slot
        for user in users:
            nearby_meetings = await self.calendar_service.get_nearby_meetings(
                user.user_id, time_slot.start_time, buffer_minutes=30
            )
            
            if nearby_meetings:
                base_score -= len(nearby_meetings) * 0.5
                
        return max(base_score, 1.0)
        
    async def _calculate_preference_score(self, time_slot: TimeSlot, users: List[User]) -> float:
        """Calculate preference alignment score"""
        total_score = 0.0
        
        for user in users:
            user_score = 8.0
            
            # Check meeting-free blocks
            for block in user.preferences.meeting_free_blocks:
                # Simplified check - in real implementation, parse time blocks
                if "Friday" in block and time_slot.start_time.weekday() == 4:
                    user_score -= 2.0
                    
            total_score += user_score
            
        return min(total_score / len(users), 10.0)
        
    async def _calculate_participant_impact(
        self,
        time_slot: TimeSlot,
        users: List[User]
    ) -> Dict[str, Dict[str, Any]]:
        """Calculate impact on each participant"""
        impact = {}
        
        for user in users:
            user_tz = pytz.timezone(user.preferences.time_zone)
            local_time = time_slot.start_time.astimezone(user_tz)
            
            # Determine impact level
            hour = local_time.hour
            if 9 <= hour <= 17:
                impact_level = "excellent"
            elif 8 <= hour <= 18:
                impact_level = "good"
            elif 7 <= hour <= 19:
                impact_level = "fair"
            else:
                impact_level = "poor"
                
            impact[user.user_id] = {
                "local_time": local_time.strftime("%I:%M %p %Z"),
                "impact": impact_level,
                "timezone": user.preferences.time_zone
            }
            
        return impact
        
    def _generate_explanation(self, score_components: ScoreComponents, users: List[User]) -> str:
        """Generate human-readable explanation"""
        explanations = []
        
        if score_components.productivity_score >= 8.5:
            explanations.append("Optimal productivity time for most participants")
        elif score_components.productivity_score >= 7.0:
            explanations.append("Good productivity time for participants")
        else:
            explanations.append("Suboptimal productivity time")
            
        if score_components.convenience_score >= 8.0:
            explanations.append("Convenient time across time zones")
        else:
            explanations.append("Some timezone inconvenience")
            
        if score_components.conflict_risk_score >= 8.0:
            explanations.append("Low conflict risk")
        else:
            explanations.append("Potential scheduling conflicts")
            
        return ". ".join(explanations) + "."
        
    def _generate_detailed_reasoning(self, score_components: ScoreComponents) -> Dict[str, Any]:
        """Generate detailed reasoning breakdown"""
        return {
            "productivity_analysis": f"Score: {score_components.productivity_score:.1f}/10",
            "convenience_analysis": f"Score: {score_components.convenience_score:.1f}/10", 
            "conflict_analysis": f"Score: {score_components.conflict_risk_score:.1f}/10",
            "preference_analysis": f"Score: {score_components.preference_score:.1f}/10",
            "weighting": {
                "productivity": "40%",
                "convenience": "30%",
                "conflict_risk": "20%",
                "preferences": "10%"
            }
        }

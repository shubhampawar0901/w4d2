"""
Calendar Service

Core service for managing meeting data and calendar operations.
"""

import json
import os
from typing import List, Optional, Dict, Any
from datetime import datetime, timedelta
import logging

from ...models.meeting import Meeting, MeetingCreate, MeetingUpdate, MeetingStatus

logger = logging.getLogger(__name__)

class CalendarService:
    """Core calendar service for meeting management"""
    
    def __init__(self, data_file: str = "data/meetings.json"):
        self.data_file = data_file
        self._meetings_cache: Optional[List[Meeting]] = None
        
    async def load_meetings(self) -> List[Meeting]:
        """Load meetings from JSON file"""
        if self._meetings_cache is not None:
            return self._meetings_cache
            
        try:
            if os.path.exists(self.data_file):
                with open(self.data_file, 'r', encoding='utf-8') as f:
                    meetings_data = json.load(f)
                    
                self._meetings_cache = [
                    Meeting(**meeting_data) for meeting_data in meetings_data
                ]
            else:
                logger.warning(f"Meetings file {self.data_file} not found")
                self._meetings_cache = []
                
        except Exception as e:
            logger.error(f"Error loading meetings: {e}")
            self._meetings_cache = []
            
        return self._meetings_cache
        
    async def save_meetings(self, meetings: List[Meeting]) -> bool:
        """Save meetings to JSON file"""
        try:
            # Ensure directory exists
            os.makedirs(os.path.dirname(self.data_file), exist_ok=True)
            
            meetings_data = [meeting.model_dump() for meeting in meetings]
            
            with open(self.data_file, 'w', encoding='utf-8') as f:
                json.dump(meetings_data, f, indent=2, default=str)
                
            self._meetings_cache = meetings
            logger.info(f"Saved {len(meetings)} meetings to {self.data_file}")
            return True
            
        except Exception as e:
            logger.error(f"Error saving meetings: {e}")
            return False
            
    async def get_meeting(self, meeting_id: str) -> Optional[Meeting]:
        """Get a specific meeting by ID"""
        meetings = await self.load_meetings()
        
        for meeting in meetings:
            if meeting.meeting_id == meeting_id:
                return meeting
                
        return None
        
    async def get_user_meetings(
        self,
        user_id: str,
        start_time: Optional[datetime] = None,
        end_time: Optional[datetime] = None
    ) -> List[Meeting]:
        """Get meetings for a specific user within a time range"""
        meetings = await self.load_meetings()
        user_meetings = []
        
        for meeting in meetings:
            if user_id in meeting.participants:
                # Filter by time range if provided
                if start_time and meeting.end_time <= start_time:
                    continue
                if end_time and meeting.start_time >= end_time:
                    continue
                    
                user_meetings.append(meeting)
                
        # Sort by start time
        user_meetings.sort(key=lambda m: m.start_time)
        return user_meetings
        
    async def get_nearby_meetings(
        self,
        user_id: str,
        target_time: datetime,
        buffer_minutes: int = 30
    ) -> List[Meeting]:
        """Get meetings near a target time for conflict detection"""
        buffer_delta = timedelta(minutes=buffer_minutes)
        start_range = target_time - buffer_delta
        end_range = target_time + buffer_delta
        
        return await self.get_user_meetings(user_id, start_range, end_range)
        
    async def create_meeting(self, meeting_data: MeetingCreate, organizer_id: str) -> Meeting:
        """Create a new meeting"""
        meetings = await self.load_meetings()
        
        # Generate new meeting ID
        existing_ids = {m.meeting_id for m in meetings}
        counter = 1
        while f"meet_{counter:03d}" in existing_ids:
            counter += 1
        new_id = f"meet_{counter:03d}"
        
        # Create meeting object
        meeting = Meeting(
            meeting_id=new_id,
            title=meeting_data.title,
            description=meeting_data.description,
            participants=meeting_data.participants,
            organizer=organizer_id,
            start_time=datetime.utcnow(),  # Will be set by scheduling logic
            end_time=datetime.utcnow() + timedelta(minutes=meeting_data.duration),
            time_zone=meeting_data.preferences.get("time_zone", "UTC"),
            meeting_type=meeting_data.meeting_type,
            status=MeetingStatus.SCHEDULED,
            location=meeting_data.location,
            agenda=meeting_data.agenda,
            recurring=meeting_data.recurring,
            recurrence_pattern=meeting_data.recurrence_pattern,
            metadata=meeting_data.preferences
        )
        
        meetings.append(meeting)
        await self.save_meetings(meetings)
        
        logger.info(f"Created meeting {new_id}: {meeting.title}")
        return meeting
        
    async def update_meeting(self, meeting_id: str, updates: MeetingUpdate) -> Optional[Meeting]:
        """Update an existing meeting"""
        meetings = await self.load_meetings()
        
        for i, meeting in enumerate(meetings):
            if meeting.meeting_id == meeting_id:
                # Apply updates
                update_data = updates.model_dump(exclude_unset=True)
                for field, value in update_data.items():
                    setattr(meeting, field, value)
                    
                meeting.updated_at = datetime.utcnow()
                
                await self.save_meetings(meetings)
                logger.info(f"Updated meeting {meeting_id}")
                return meeting
                
        logger.warning(f"Meeting {meeting_id} not found for update")
        return None
        
    async def delete_meeting(self, meeting_id: str) -> bool:
        """Delete a meeting"""
        meetings = await self.load_meetings()
        
        for i, meeting in enumerate(meetings):
            if meeting.meeting_id == meeting_id:
                meetings.pop(i)
                await self.save_meetings(meetings)
                logger.info(f"Deleted meeting {meeting_id}")
                return True
                
        logger.warning(f"Meeting {meeting_id} not found for deletion")
        return False
        
    async def search_meetings(
        self,
        query: str,
        user_id: Optional[str] = None,
        limit: int = 10
    ) -> List[Meeting]:
        """Search meetings by title, description, or agenda"""
        meetings = await self.load_meetings()
        results = []
        query_lower = query.lower()
        
        for meeting in meetings:
            # Filter by user if specified
            if user_id and user_id not in meeting.participants:
                continue
                
            # Search in title, description, and agenda
            searchable_text = " ".join([
                meeting.title.lower(),
                meeting.description.lower() if meeting.description else "",
                " ".join(meeting.agenda).lower()
            ])
            
            if query_lower in searchable_text:
                results.append(meeting)
                
            if len(results) >= limit:
                break
                
        return results
        
    async def get_meeting_statistics(self, user_id: Optional[str] = None) -> Dict[str, Any]:
        """Get meeting statistics"""
        meetings = await self.load_meetings()
        
        if user_id:
            meetings = [m for m in meetings if user_id in m.participants]
            
        total_meetings = len(meetings)
        if total_meetings == 0:
            return {"total_meetings": 0}
            
        # Calculate statistics
        total_duration = sum(
            (m.end_time - m.start_time).total_seconds() / 3600 
            for m in meetings
        )
        
        avg_duration = total_duration / total_meetings if total_meetings > 0 else 0
        
        meeting_types = {}
        for meeting in meetings:
            meeting_types[meeting.meeting_type] = meeting_types.get(meeting.meeting_type, 0) + 1
            
        effectiveness_scores = [m.effectiveness_score for m in meetings if m.effectiveness_score]
        avg_effectiveness = sum(effectiveness_scores) / len(effectiveness_scores) if effectiveness_scores else 0
        
        return {
            "total_meetings": total_meetings,
            "total_hours": round(total_duration, 2),
            "average_duration_hours": round(avg_duration, 2),
            "meeting_types": meeting_types,
            "average_effectiveness": round(avg_effectiveness, 2),
            "effectiveness_count": len(effectiveness_scores)
        }
        
    def clear_cache(self):
        """Clear the meetings cache"""
        self._meetings_cache = None

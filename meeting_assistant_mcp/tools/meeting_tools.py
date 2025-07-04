"""
Meeting Assistant MCP Tools

Implementation of all 8 MCP tools for the Smart Meeting Assistant.
"""

from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta
import logging
from fastmcp import FastMCP

from ..services.ai.optimal_time_service import OptimalTimeService
from ..services.core.calendar_service import CalendarService
from ..services.core.user_service import UserService
from ..models.meeting import MeetingCreate
from ..models.scheduling import OptimalSlot

logger = logging.getLogger(__name__)

# Initialize services (will be properly injected in main.py)
calendar_service = CalendarService()
user_service = UserService()
optimal_time_service = OptimalTimeService(calendar_service, user_service)

mcp = FastMCP("Smart Meeting Assistant")

@mcp.tool()
async def find_optimal_slots(
    participants: List[str],
    duration: int,
    date_range: List[str],
    preferences: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """
    Find optimal time slots for a meeting using AI-powered scheduling.

    This tool analyzes participant availability, productivity patterns, time zones,
    and preferences to recommend the best possible meeting times.

    Args:
        participants: List of participant user IDs
        duration: Meeting duration in minutes
        date_range: List with [start_date, end_date] in ISO format
        preferences: Optional meeting preferences and constraints

    Returns:
        Dictionary containing ranked optimal time slots with detailed scoring
    """
    try:
        logger.info(f"Finding optimal slots for {len(participants)} participants")

        # Parse date range
        start_date = datetime.fromisoformat(date_range[0].replace('Z', '+00:00'))
        end_date = datetime.fromisoformat(date_range[1].replace('Z', '+00:00'))

        # Find optimal slots using AI service
        optimal_slots = await optimal_time_service.find_optimal_slots(
            participants=participants,
            duration=duration,
            date_range=(start_date, end_date),
            preferences=preferences or {}
        )

        if not optimal_slots:
            return {
                "success": False,
                "message": "No suitable time slots found for all participants",
                "optimal_slots": [],
                "suggestions": [
                    "Try extending the date range",
                    "Consider reducing meeting duration",
                    "Check if all participants are available during the specified period"
                ]
            }

        # Format response
        formatted_slots = []
        for slot in optimal_slots:
            formatted_slots.append({
                "rank": slot.rank,
                "start_time": slot.time_slot.start_time.isoformat() + "Z",
                "end_time": slot.time_slot.end_time.isoformat() + "Z",
                "duration_minutes": slot.time_slot.duration_minutes,
                "overall_score": round(slot.overall_score, 2),
                "score_breakdown": {
                    "productivity": round(slot.productivity_score, 2),
                    "convenience": round(slot.convenience_score, 2),
                    "conflict_risk": round(slot.conflict_risk_score, 2),
                    "preferences": round(slot.preference_score, 2)
                },
                "explanation": slot.explanation,
                "participant_impact": slot.participant_impact,
                "reasoning": slot.reasoning
            })

        return {
            "success": True,
            "optimal_slots": formatted_slots,
            "analysis_summary": {
                "participants_analyzed": len(participants),
                "duration_requested": duration,
                "date_range": date_range,
                "slots_found": len(optimal_slots),
                "best_score": round(optimal_slots[0].overall_score, 2) if optimal_slots else 0
            },
            "recommendations": [
                f"Best option: {optimal_slots[0].explanation}" if optimal_slots else "No recommendations available",
                "Consider the participant impact when making final decision",
                "Higher scores indicate better overall fit for all participants"
            ]
        }

    except Exception as e:
        logger.error(f"Error finding optimal slots: {e}")
        return {
            "success": False,
            "error": str(e),
            "message": "Failed to find optimal time slots"
        }

@mcp.tool()
async def create_meeting(
    title: str,
    participants: List[str],
    duration: int,
    organizer: str,
    preferences: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """
    Create a new meeting with intelligent scheduling.

    Args:
        title: Meeting title
        participants: List of participant user IDs
        duration: Meeting duration in minutes
        organizer: Organizer user ID
        preferences: Meeting preferences (description, location, etc.)

    Returns:
        Dictionary containing created meeting details
    """
    try:
        # Create meeting data
        meeting_data = MeetingCreate(
            title=title,
            participants=participants,
            duration=duration,
            preferences=preferences or {}
        )

        # Create the meeting
        meeting = await calendar_service.create_meeting(meeting_data, organizer)

        return {
            "success": True,
            "meeting": {
                "meeting_id": meeting.meeting_id,
                "title": meeting.title,
                "participants": meeting.participants,
                "organizer": meeting.organizer,
                "start_time": meeting.start_time.isoformat() + "Z",
                "end_time": meeting.end_time.isoformat() + "Z",
                "status": meeting.status,
                "location": meeting.location
            },
            "message": f"Meeting '{title}' created successfully"
        }

    except Exception as e:
        logger.error(f"Error creating meeting: {e}")
        return {
            "success": False,
            "error": str(e),
            "message": "Failed to create meeting"
        }

@mcp.tool()
async def detect_scheduling_conflicts(
    user_id: str,
    start_time: str,
    end_time: str
) -> Dict[str, Any]:
    """
    Detect scheduling conflicts for a user in a given time range.

    Args:
        user_id: User ID to check conflicts for
        start_time: Start time in ISO format
        end_time: End time in ISO format

    Returns:
        Dictionary containing conflict analysis
    """
    try:
        start_dt = datetime.fromisoformat(start_time.replace('Z', '+00:00'))
        end_dt = datetime.fromisoformat(end_time.replace('Z', '+00:00'))

        # Get user meetings in the time range
        user_meetings = await calendar_service.get_user_meetings(user_id, start_dt, end_dt)

        conflicts = []
        for meeting in user_meetings:
            # Check for overlap
            if (meeting.start_time < end_dt and meeting.end_time > start_dt):
                conflicts.append({
                    "meeting_id": meeting.meeting_id,
                    "title": meeting.title,
                    "start_time": meeting.start_time.isoformat() + "Z",
                    "end_time": meeting.end_time.isoformat() + "Z",
                    "conflict_type": "overlap",
                    "severity": "high"
                })

        return {
            "success": True,
            "user_id": user_id,
            "time_range": {
                "start": start_time,
                "end": end_time
            },
            "conflicts_found": len(conflicts),
            "conflicts": conflicts,
            "is_available": len(conflicts) == 0,
            "recommendations": [
                "No conflicts found - time slot is available" if len(conflicts) == 0
                else f"Found {len(conflicts)} conflicts - consider alternative times"
            ]
        }

    except Exception as e:
        logger.error(f"Error detecting conflicts: {e}")
        return {
            "success": False,
            "error": str(e),
            "message": "Failed to detect scheduling conflicts"
        }
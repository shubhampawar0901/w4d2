"""
Time Zone Service

Service for handling time zone conversions and calculations.
"""

import pytz
from datetime import datetime, time
from typing import List, Dict, Any, Optional
import logging

logger = logging.getLogger(__name__)

class TimeZoneService:
    """Service for time zone operations"""
    
    def __init__(self):
        self.common_timezones = {
            "America/New_York": "Eastern Time",
            "America/Los_Angeles": "Pacific Time", 
            "America/Chicago": "Central Time",
            "America/Denver": "Mountain Time",
            "Europe/London": "GMT/BST",
            "Europe/Paris": "CET/CEST",
            "Europe/Berlin": "CET/CEST",
            "Asia/Tokyo": "JST",
            "Asia/Shanghai": "CST",
            "Asia/Kolkata": "IST",
            "Asia/Seoul": "KST",
            "Australia/Sydney": "AEST/AEDT"
        }
        
    def get_timezone_info(self, timezone_name: str) -> Dict[str, Any]:
        """Get information about a timezone"""
        try:
            tz = pytz.timezone(timezone_name)
            now = datetime.now(tz)
            
            return {
                "timezone": timezone_name,
                "display_name": self.common_timezones.get(timezone_name, timezone_name),
                "current_time": now.isoformat(),
                "utc_offset": now.strftime("%z"),
                "is_dst": bool(now.dst()),
                "abbreviation": now.strftime("%Z")
            }
        except Exception as e:
            logger.error(f"Error getting timezone info for {timezone_name}: {e}")
            return {}
            
    def convert_time(
        self,
        dt: datetime,
        from_tz: str,
        to_tz: str
    ) -> datetime:
        """Convert datetime from one timezone to another"""
        try:
            from_timezone = pytz.timezone(from_tz)
            to_timezone = pytz.timezone(to_tz)
            
            # Localize the datetime if it's naive
            if dt.tzinfo is None:
                dt = from_timezone.localize(dt)
            
            # Convert to target timezone
            return dt.astimezone(to_timezone)
            
        except Exception as e:
            logger.error(f"Error converting time from {from_tz} to {to_tz}: {e}")
            return dt
            
    def find_common_working_hours(
        self,
        timezones: List[str],
        working_start: time = time(9, 0),
        working_end: time = time(17, 0)
    ) -> Dict[str, Any]:
        """Find overlapping working hours across multiple timezones"""
        try:
            # Use today as reference date
            today = datetime.now().date()
            
            # Convert working hours to UTC for each timezone
            utc_windows = []
            
            for tz_name in timezones:
                tz = pytz.timezone(tz_name)
                
                # Create datetime objects for working hours
                start_dt = tz.localize(datetime.combine(today, working_start))
                end_dt = tz.localize(datetime.combine(today, working_end))
                
                # Convert to UTC
                start_utc = start_dt.astimezone(pytz.UTC)
                end_utc = end_dt.astimezone(pytz.UTC)
                
                utc_windows.append({
                    "timezone": tz_name,
                    "start_utc": start_utc,
                    "end_utc": end_utc
                })
            
            # Find intersection of all windows
            if not utc_windows:
                return {"overlap_found": False}
                
            # Start with first window
            common_start = utc_windows[0]["start_utc"]
            common_end = utc_windows[0]["end_utc"]
            
            # Find intersection with all other windows
            for window in utc_windows[1:]:
                common_start = max(common_start, window["start_utc"])
                common_end = min(common_end, window["end_utc"])
                
            # Check if there's any overlap
            if common_start >= common_end:
                return {
                    "overlap_found": False,
                    "message": "No common working hours found across all timezones"
                }
            
            # Convert back to each timezone for display
            local_times = {}
            for tz_name in timezones:
                tz = pytz.timezone(tz_name)
                local_start = common_start.astimezone(tz)
                local_end = common_end.astimezone(tz)
                
                local_times[tz_name] = {
                    "start": local_start.strftime("%H:%M"),
                    "end": local_end.strftime("%H:%M"),
                    "duration_hours": (common_end - common_start).total_seconds() / 3600
                }
            
            return {
                "overlap_found": True,
                "common_window_utc": {
                    "start": common_start.isoformat(),
                    "end": common_end.isoformat(),
                    "duration_hours": (common_end - common_start).total_seconds() / 3600
                },
                "local_times": local_times,
                "timezones_analyzed": timezones
            }
            
        except Exception as e:
            logger.error(f"Error finding common working hours: {e}")
            return {"overlap_found": False, "error": str(e)}
            
    def get_timezone_fairness_score(
        self,
        meeting_time: datetime,
        participant_timezones: List[str]
    ) -> Dict[str, Any]:
        """Calculate fairness score for a meeting time across timezones"""
        try:
            timezone_impacts = {}
            total_score = 0
            
            for tz_name in participant_timezones:
                tz = pytz.timezone(tz_name)
                local_time = meeting_time.astimezone(tz)
                hour = local_time.hour
                
                # Score based on local time (0-10 scale)
                if 9 <= hour <= 17:
                    score = 10  # Perfect business hours
                elif 8 <= hour <= 18:
                    score = 8   # Acceptable
                elif 7 <= hour <= 19:
                    score = 6   # Early/late but manageable
                elif 6 <= hour <= 20:
                    score = 4   # Very early/late
                else:
                    score = 1   # Unreasonable hours
                
                timezone_impacts[tz_name] = {
                    "local_time": local_time.strftime("%H:%M %Z"),
                    "hour": hour,
                    "score": score,
                    "impact": (
                        "excellent" if score >= 9 else
                        "good" if score >= 7 else
                        "fair" if score >= 5 else
                        "poor"
                    )
                }
                
                total_score += score
            
            avg_score = total_score / len(participant_timezones) if participant_timezones else 0
            
            return {
                "fairness_score": round(avg_score, 2),
                "timezone_impacts": timezone_impacts,
                "meeting_time_utc": meeting_time.isoformat(),
                "analysis": {
                    "excellent_timezones": len([t for t in timezone_impacts.values() if t["score"] >= 9]),
                    "good_timezones": len([t for t in timezone_impacts.values() if t["score"] >= 7]),
                    "poor_timezones": len([t for t in timezone_impacts.values() if t["score"] < 5])
                },
                "recommendation": (
                    "Excellent time for all participants" if avg_score >= 9 else
                    "Good time for most participants" if avg_score >= 7 else
                    "Fair time with some inconvenience" if avg_score >= 5 else
                    "Poor time - consider alternatives"
                )
            }
            
        except Exception as e:
            logger.error(f"Error calculating timezone fairness: {e}")
            return {"fairness_score": 0, "error": str(e)}
            
    def suggest_meeting_times(
        self,
        participant_timezones: List[str],
        duration_minutes: int = 60,
        days_ahead: int = 7
    ) -> List[Dict[str, Any]]:
        """Suggest optimal meeting times considering all timezones"""
        try:
            suggestions = []
            
            # Find common working hours
            common_hours = self.find_common_working_hours(participant_timezones)
            
            if not common_hours.get("overlap_found"):
                return []
            
            # Generate suggestions for the next week
            base_date = datetime.now().date()
            
            for day_offset in range(1, days_ahead + 1):
                # Skip weekends
                target_date = base_date + timedelta(days=day_offset)
                if target_date.weekday() >= 5:  # Saturday = 5, Sunday = 6
                    continue
                
                # Use the common window start time
                common_start = datetime.fromisoformat(
                    common_hours["common_window_utc"]["start"]
                ).replace(
                    year=target_date.year,
                    month=target_date.month,
                    day=target_date.day
                )
                
                # Calculate fairness score
                fairness = self.get_timezone_fairness_score(common_start, participant_timezones)
                
                suggestions.append({
                    "date": target_date.isoformat(),
                    "start_time_utc": common_start.isoformat(),
                    "end_time_utc": (common_start + timedelta(minutes=duration_minutes)).isoformat(),
                    "fairness_score": fairness["fairness_score"],
                    "timezone_impacts": fairness["timezone_impacts"],
                    "recommendation": fairness["recommendation"]
                })
            
            # Sort by fairness score (descending)
            suggestions.sort(key=lambda x: x["fairness_score"], reverse=True)
            
            return suggestions[:5]  # Return top 5 suggestions
            
        except Exception as e:
            logger.error(f"Error suggesting meeting times: {e}")
            return []
            
    def get_supported_timezones(self) -> List[Dict[str, str]]:
        """Get list of supported timezones"""
        return [
            {"timezone": tz, "display_name": name}
            for tz, name in self.common_timezones.items()
        ]

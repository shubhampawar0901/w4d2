#!/usr/bin/env python3
"""
Script to generate additional meetings to reach 60+ total meetings
"""

import json
from datetime import datetime, timedelta
import random

# Meeting templates for generating realistic meetings
meeting_templates = [
    {
        "title": "Code Review Session",
        "description": "Weekly code review for quality assurance",
        "meeting_type": "review",
        "duration": 60,
        "participants": ["user_001", "user_002", "user_008"],
        "agenda": ["Pull request reviews", "Code quality discussion", "Best practices", "Action items"]
    },
    {
        "title": "Database Migration Planning",
        "description": "Planning database schema migration",
        "meeting_type": "planning", 
        "duration": 90,
        "participants": ["user_002", "user_005", "user_006"],
        "agenda": ["Migration strategy", "Rollback plan", "Testing approach", "Timeline"]
    },
    {
        "title": "User Testing Results Review",
        "description": "Review of latest user testing session results",
        "meeting_type": "review",
        "duration": 75,
        "participants": ["user_004", "user_003", "user_009"],
        "agenda": ["Test findings", "User feedback", "Design implications", "Next steps"]
    },
    {
        "title": "Incident Post-Mortem",
        "description": "Post-mortem analysis of recent production incident",
        "meeting_type": "review",
        "duration": 60,
        "participants": ["user_006", "user_001", "user_002", "user_010"],
        "agenda": ["Incident timeline", "Root cause analysis", "Prevention measures", "Action items"]
    },
    {
        "title": "Feature Kickoff Meeting",
        "description": "Kickoff meeting for new feature development",
        "meeting_type": "planning",
        "duration": 120,
        "participants": ["user_003", "user_001", "user_004", "user_008"],
        "agenda": ["Requirements review", "Technical approach", "Timeline planning", "Resource allocation"]
    }
]

def generate_meeting(template, meeting_id, start_date):
    """Generate a meeting based on template"""
    # Random time between 9 AM and 5 PM
    hour = random.randint(9, 16)
    minute = random.choice([0, 30])
    
    start_time = start_date.replace(hour=hour, minute=minute, second=0, microsecond=0)
    end_time = start_time + timedelta(minutes=template["duration"])
    
    # Random effectiveness score between 7.0 and 9.5
    effectiveness = round(random.uniform(7.0, 9.5), 1)
    
    # Random organizer from participants
    organizer = random.choice(template["participants"])
    
    meeting = {
        "meeting_id": meeting_id,
        "title": template["title"],
        "description": template["description"],
        "participants": template["participants"],
        "organizer": organizer,
        "start_time": start_time.isoformat() + "Z",
        "end_time": end_time.isoformat() + "Z",
        "time_zone": "America/New_York",
        "meeting_type": template["meeting_type"],
        "status": "scheduled",
        "location": random.choice(["Virtual - Zoom", "Virtual - Teams", "Conference Room A", "Conference Room B"]),
        "agenda": template["agenda"],
        "recurring": random.choice([True, False]),
        "recurrence_pattern": random.choice([None, "weekly", "bi_weekly", "monthly"]) if random.choice([True, False]) else None,
        "created_at": (start_date - timedelta(days=random.randint(1, 14))).isoformat() + "Z",
        "updated_at": (start_date - timedelta(days=random.randint(0, 7))).isoformat() + "Z",
        "effectiveness_score": effectiveness,
        "metadata": {
            "generated": True,
            "template": template["title"].lower().replace(" ", "_")
        }
    }
    
    return meeting

def main():
    # Generate meetings for the next 2 weeks
    base_date = datetime(2024, 12, 25)
    meetings = []
    
    for i in range(45):  # Generate 45 more meetings to reach 65 total
        template = random.choice(meeting_templates)
        meeting_id = f"meet_{21 + i:03d}"
        
        # Spread meetings across 2 weeks
        days_offset = random.randint(0, 13)
        meeting_date = base_date + timedelta(days=days_offset)
        
        meeting = generate_meeting(template, meeting_id, meeting_date)
        meetings.append(meeting)
    
    # Sort by start time
    meetings.sort(key=lambda x: x["start_time"])
    
    # Print JSON for the additional meetings
    print(json.dumps(meetings, indent=2))

if __name__ == "__main__":
    main()

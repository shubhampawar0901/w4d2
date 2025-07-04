#!/usr/bin/env python3
"""
Script to merge additional meetings and reach 60+ total
"""

import json
from datetime import datetime, timedelta
import random

def create_additional_meetings():
    """Create additional meetings to reach 60+ total"""
    
    # Meeting templates
    templates = [
        {
            "title": "Weekly Team Standup",
            "description": "Daily standup for team coordination",
            "meeting_type": "standup",
            "duration": 30,
            "participants": ["user_001", "user_002", "user_005", "user_008"],
            "agenda": ["Progress updates", "Blockers", "Today's goals"]
        },
        {
            "title": "One-on-One Meeting",
            "description": "Manager and direct report 1:1",
            "meeting_type": "1:1",
            "duration": 30,
            "participants": ["user_001", "user_002"],
            "agenda": ["Career development", "Feedback", "Support needed"]
        },
        {
            "title": "Sprint Planning",
            "description": "Planning next sprint iteration",
            "meeting_type": "planning",
            "duration": 120,
            "participants": ["user_001", "user_002", "user_005", "user_006", "user_008"],
            "agenda": ["Backlog review", "Story estimation", "Sprint commitment"]
        },
        {
            "title": "Design Review",
            "description": "Review of design proposals and mockups",
            "meeting_type": "review",
            "duration": 90,
            "participants": ["user_004", "user_003", "user_008", "user_001"],
            "agenda": ["Design presentation", "Feedback collection", "Next iterations"]
        },
        {
            "title": "Architecture Discussion",
            "description": "Technical architecture planning session",
            "meeting_type": "brainstorming",
            "duration": 120,
            "participants": ["user_001", "user_002", "user_006", "user_010"],
            "agenda": ["System design", "Technology choices", "Scalability planning"]
        }
    ]
    
    # Generate 40 more meetings
    meetings = []
    start_date = datetime(2024, 12, 26)  # Start after existing meetings

    for i in range(40):
        template = random.choice(templates)
        meeting_id = f"meet_{26 + i:03d}"
        
        # Spread across 3 weeks
        days_offset = random.randint(0, 20)
        meeting_date = start_date + timedelta(days=days_offset)
        
        # Random time during business hours
        hour = random.randint(9, 16)
        minute = random.choice([0, 30])
        
        start_time = meeting_date.replace(hour=hour, minute=minute, second=0, microsecond=0)
        end_time = start_time + timedelta(minutes=template["duration"])
        
        # Random effectiveness score
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
            "created_at": (start_time - timedelta(days=random.randint(1, 14))).isoformat() + "Z",
            "updated_at": (start_time - timedelta(days=random.randint(0, 7))).isoformat() + "Z",
            "effectiveness_score": effectiveness,
            "metadata": {
                "generated": True,
                "template": template["title"].lower().replace(" ", "_"),
                "batch": "additional_40"
            }
        }
        
        meetings.append(meeting)
    
    return meetings

def main():
    # Load existing meetings
    try:
        with open('data/meetings.json', 'r') as f:
            existing_meetings = json.load(f)
    except FileNotFoundError:
        existing_meetings = []
    
    # Generate additional meetings
    additional_meetings = create_additional_meetings()
    
    # Combine all meetings
    all_meetings = existing_meetings + additional_meetings
    
    # Sort by start time
    all_meetings.sort(key=lambda x: x["start_time"])
    
    # Save combined meetings
    with open('data/meetings.json', 'w') as f:
        json.dump(all_meetings, f, indent=2)
    
    print(f"Total meetings: {len(all_meetings)}")
    print(f"Added {len(additional_meetings)} new meetings")

if __name__ == "__main__":
    main()

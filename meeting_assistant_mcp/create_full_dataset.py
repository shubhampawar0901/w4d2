#!/usr/bin/env python3
"""
Script to create a comprehensive meeting dataset with 60+ meetings
"""

import json
from datetime import datetime, timedelta
import random

def create_comprehensive_meetings():
    """Create 60+ meetings with realistic data"""
    
    # Base meetings (we already have 25)
    base_meetings = []
    
    # Meeting templates for variety
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
        },
        {
            "title": "Customer Feedback Session",
            "description": "Review customer feedback and feature requests",
            "meeting_type": "review",
            "duration": 60,
            "participants": ["user_003", "user_009", "user_004"],
            "agenda": ["Customer insights", "Feature prioritization", "User experience"]
        },
        {
            "title": "Security Review",
            "description": "Security assessment and vulnerability review",
            "meeting_type": "review",
            "duration": 90,
            "participants": ["user_006", "user_001", "user_010"],
            "agenda": ["Security audit", "Vulnerability assessment", "Compliance check"]
        },
        {
            "title": "Performance Optimization",
            "description": "Application performance analysis and optimization",
            "meeting_type": "brainstorming",
            "duration": 90,
            "participants": ["user_002", "user_005", "user_006"],
            "agenda": ["Performance metrics", "Bottleneck analysis", "Optimization strategies"]
        }
    ]
    
    # Generate meetings for 3 weeks
    start_date = datetime(2024, 12, 16)
    meetings = []
    
    for i in range(40):  # Generate 40 more meetings
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
            "location": random.choice(["Virtual - Zoom", "Virtual - Teams", "Conference Room A", "Conference Room B", "Meeting Room 1", "Meeting Room 2"]),
            "agenda": template["agenda"],
            "recurring": random.choice([True, False]),
            "recurrence_pattern": random.choice([None, "weekly", "bi_weekly", "monthly"]) if random.choice([True, False]) else None,
            "created_at": (start_time - timedelta(days=random.randint(1, 14))).isoformat() + "Z",
            "updated_at": (start_time - timedelta(days=random.randint(0, 7))).isoformat() + "Z",
            "effectiveness_score": effectiveness,
            "metadata": {
                "generated": True,
                "template": template["title"].lower().replace(" ", "_"),
                "week": f"week_{(days_offset // 7) + 1}"
            }
        }
        
        meetings.append(meeting)
    
    # Sort by start time
    meetings.sort(key=lambda x: x["start_time"])
    
    return meetings

if __name__ == "__main__":
    meetings = create_comprehensive_meetings()
    print(json.dumps(meetings, indent=2))
    print(f"\n# Generated {len(meetings)} additional meetings")

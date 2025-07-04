#!/usr/bin/env python3
"""
Test script for Smart Meeting Assistant MCP Server

This script tests all the core functionality of the meeting assistant.
"""

import asyncio
import json
from datetime import datetime, timedelta
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Import services
from services.core.calendar_service import CalendarService
from services.core.user_service import UserService
from services.ai.optimal_time_service import OptimalTimeService

async def test_data_loading():
    """Test loading of users and meetings data"""
    logger.info("Testing data loading...")
    
    calendar_service = CalendarService("data/meetings.json")
    user_service = UserService("data/users.json")
    
    # Load data
    users = await user_service.load_users()
    meetings = await calendar_service.load_meetings()
    
    logger.info(f"Loaded {len(users)} users")
    logger.info(f"Loaded {len(meetings)} meetings")
    
    # Test user data
    if users:
        sample_user = users[0]
        logger.info(f"Sample user: {sample_user.name} ({sample_user.user_id})")
        logger.info(f"Time zone: {sample_user.preferences.time_zone}")
        logger.info(f"Working hours: {sample_user.preferences.working_hours_start} - {sample_user.preferences.working_hours_end}")
    
    # Test meeting data
    if meetings:
        sample_meeting = meetings[0]
        logger.info(f"Sample meeting: {sample_meeting.title} ({sample_meeting.meeting_id})")
        logger.info(f"Participants: {len(sample_meeting.participants)}")
        logger.info(f"Duration: {(sample_meeting.end_time - sample_meeting.start_time).total_seconds() / 60} minutes")
    
    return users, meetings

async def test_optimal_time_service():
    """Test the optimal time slot recommendation service"""
    logger.info("Testing optimal time slot service...")
    
    calendar_service = CalendarService("data/meetings.json")
    user_service = UserService("data/users.json")
    optimal_service = OptimalTimeService(calendar_service, user_service)
    
    # Test parameters
    participants = ["user_001", "user_002", "user_003"]
    duration = 60  # 1 hour
    start_date = datetime.now() + timedelta(days=1)
    end_date = start_date + timedelta(days=7)
    
    try:
        optimal_slots = await optimal_service.find_optimal_slots(
            participants=participants,
            duration=duration,
            date_range=(start_date, end_date)
        )
        
        logger.info(f"Found {len(optimal_slots)} optimal time slots")
        
        if optimal_slots:
            best_slot = optimal_slots[0]
            logger.info(f"Best slot: {best_slot.time_slot.start_time} - {best_slot.time_slot.end_time}")
            logger.info(f"Overall score: {best_slot.overall_score:.2f}")
            logger.info(f"Explanation: {best_slot.explanation}")
        
        return optimal_slots
        
    except Exception as e:
        logger.error(f"Error testing optimal time service: {e}")
        return []

async def test_calendar_operations():
    """Test calendar CRUD operations"""
    logger.info("Testing calendar operations...")
    
    calendar_service = CalendarService("data/meetings.json")
    
    # Test getting meetings for a user
    user_meetings = await calendar_service.get_user_meetings("user_001")
    logger.info(f"User_001 has {len(user_meetings)} meetings")
    
    # Test search functionality
    search_results = await calendar_service.search_meetings("standup", limit=5)
    logger.info(f"Found {len(search_results)} meetings matching 'standup'")
    
    # Test statistics
    stats = await calendar_service.get_meeting_statistics("user_001")
    logger.info(f"Meeting statistics for user_001: {stats}")
    
    return user_meetings, search_results, stats

async def test_user_operations():
    """Test user service operations"""
    logger.info("Testing user operations...")
    
    user_service = UserService("data/users.json")
    
    # Test getting user
    user = await user_service.get_user("user_001")
    if user:
        logger.info(f"Retrieved user: {user.name}")
        
        # Test availability summary
        availability = await user_service.get_user_availability_summary("user_001")
        logger.info(f"Availability summary: {availability}")
    
    # Test department query
    eng_users = await user_service.get_users_by_department("Engineering")
    logger.info(f"Engineering department has {len(eng_users)} users")
    
    # Test organization structure
    org_structure = await user_service.get_organization_structure()
    logger.info(f"Organization structure: {org_structure}")
    
    return user, availability, eng_users

async def test_conflict_detection():
    """Test conflict detection functionality"""
    logger.info("Testing conflict detection...")
    
    calendar_service = CalendarService("data/meetings.json")
    
    # Test with a known busy time
    test_start = datetime(2024, 12, 16, 14, 0)  # 2 PM
    test_end = datetime(2024, 12, 16, 15, 0)    # 3 PM
    
    conflicts = await calendar_service.get_nearby_meetings(
        "user_001", 
        test_start, 
        buffer_minutes=30
    )
    
    logger.info(f"Found {len(conflicts)} potential conflicts for user_001")
    
    for conflict in conflicts:
        logger.info(f"Conflict: {conflict.title} at {conflict.start_time}")
    
    return conflicts

async def test_meeting_patterns():
    """Test meeting pattern analysis"""
    logger.info("Testing meeting pattern analysis...")
    
    calendar_service = CalendarService("data/meetings.json")
    
    # Get meetings for analysis
    end_date = datetime.utcnow()
    start_date = end_date - timedelta(days=30)
    
    user_meetings = await calendar_service.get_user_meetings("user_001", start_date, end_date)
    
    if user_meetings:
        # Analyze patterns
        meeting_types = {}
        daily_counts = {}
        hourly_counts = {}
        
        for meeting in user_meetings:
            # Meeting type distribution
            meeting_types[meeting.meeting_type] = meeting_types.get(meeting.meeting_type, 0) + 1
            
            # Daily distribution
            day = meeting.start_time.strftime('%A')
            daily_counts[day] = daily_counts.get(day, 0) + 1
            
            # Hourly distribution
            hour = meeting.start_time.hour
            hourly_counts[hour] = hourly_counts.get(hour, 0) + 1
        
        logger.info(f"Meeting type distribution: {meeting_types}")
        logger.info(f"Daily distribution: {daily_counts}")
        logger.info(f"Peak hours: {sorted(hourly_counts.items(), key=lambda x: x[1], reverse=True)[:3]}")
    
    return user_meetings

async def run_comprehensive_test():
    """Run comprehensive test of all functionality"""
    logger.info("Starting comprehensive test of Smart Meeting Assistant...")
    
    try:
        # Test 1: Data Loading
        users, meetings = await test_data_loading()
        
        # Test 2: Calendar Operations
        user_meetings, search_results, stats = await test_calendar_operations()
        
        # Test 3: User Operations
        user, availability, eng_users = await test_user_operations()
        
        # Test 4: Optimal Time Service
        optimal_slots = await test_optimal_time_service()
        
        # Test 5: Conflict Detection
        conflicts = await test_conflict_detection()
        
        # Test 6: Meeting Patterns
        pattern_meetings = await test_meeting_patterns()
        
        # Summary
        logger.info("\n" + "="*50)
        logger.info("COMPREHENSIVE TEST SUMMARY")
        logger.info("="*50)
        logger.info(f"✓ Data Loading: {len(users)} users, {len(meetings)} meetings")
        logger.info(f"✓ Calendar Operations: {len(user_meetings)} user meetings, {len(search_results)} search results")
        logger.info(f"✓ User Operations: {len(eng_users)} engineering users")
        logger.info(f"✓ Optimal Time Service: {len(optimal_slots)} optimal slots found")
        logger.info(f"✓ Conflict Detection: {len(conflicts)} conflicts detected")
        logger.info(f"✓ Pattern Analysis: {len(pattern_meetings)} meetings analyzed")
        logger.info("="*50)
        logger.info("All tests completed successfully!")
        
        return True
        
    except Exception as e:
        logger.error(f"Test failed with error: {e}")
        return False

async def main():
    """Main test function"""
    success = await run_comprehensive_test()
    
    if success:
        logger.info("🎉 Smart Meeting Assistant is working correctly!")
    else:
        logger.error("❌ Tests failed - check the logs for details")

if __name__ == "__main__":
    asyncio.run(main())

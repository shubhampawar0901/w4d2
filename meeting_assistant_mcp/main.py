#!/usr/bin/env python3
"""
Smart Meeting Assistant MCP Server

An AI-powered meeting scheduling and management system with intelligent optimization.
"""

import asyncio
import logging
import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('meeting_assistant.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

# Import services and tools
from services.core.calendar_service import CalendarService
from services.core.user_service import UserService
from services.ai.optimal_time_service import OptimalTimeService

# Import all MCP tools
from tools.meeting_tools import (
    find_optimal_slots,
    create_meeting,
    detect_scheduling_conflicts,
    analyze_meeting_patterns,
    generate_agenda_suggestions,
    calculate_workload_balance,
    score_meeting_effectiveness,
    optimize_meeting_schedule,
    mcp
)

class MeetingAssistantServer:
    """Smart Meeting Assistant MCP Server"""
    
    def __init__(self):
        self.calendar_service = CalendarService("data/meetings.json")
        self.user_service = UserService("data/users.json")
        self.optimal_time_service = OptimalTimeService(
            self.calendar_service, 
            self.user_service
        )
        
    async def initialize(self):
        """Initialize the server and load data"""
        logger.info("Initializing Smart Meeting Assistant MCP Server...")
        
        # Load initial data
        users = await self.user_service.load_users()
        meetings = await self.calendar_service.load_meetings()
        
        logger.info(f"Loaded {len(users)} users and {len(meetings)} meetings")
        
        # Verify data integrity
        await self._verify_data_integrity()
        
        logger.info("Server initialization complete")
        
    async def _verify_data_integrity(self):
        """Verify data integrity and relationships"""
        users = await self.user_service.load_users()
        meetings = await self.calendar_service.load_meetings()
        
        user_ids = {user.user_id for user in users}
        
        # Check for invalid participant references in meetings
        invalid_participants = 0
        for meeting in meetings:
            for participant in meeting.participants:
                if participant not in user_ids:
                    invalid_participants += 1
                    logger.warning(f"Meeting {meeting.meeting_id} references unknown user {participant}")
        
        if invalid_participants > 0:
            logger.warning(f"Found {invalid_participants} invalid participant references")
        else:
            logger.info("Data integrity check passed")
            
    async def get_server_info(self):
        """Get server information and statistics"""
        users = await self.user_service.load_users()
        meetings = await self.calendar_service.load_meetings()
        
        # Calculate statistics
        total_users = len(users)
        total_meetings = len(meetings)
        
        # Department distribution
        departments = {}
        for user in users:
            departments[user.department] = departments.get(user.department, 0) + 1
            
        # Meeting type distribution
        meeting_types = {}
        for meeting in meetings:
            meeting_types[meeting.meeting_type] = meeting_types.get(meeting.meeting_type, 0) + 1
            
        return {
            "server_name": "Smart Meeting Assistant",
            "version": "1.0.0",
            "status": "running",
            "statistics": {
                "total_users": total_users,
                "total_meetings": total_meetings,
                "departments": departments,
                "meeting_types": meeting_types
            },
            "capabilities": [
                "AI-powered optimal time slot recommendations",
                "Intelligent conflict detection and resolution", 
                "Meeting pattern analysis and insights",
                "Workload balancing across team members",
                "Smart agenda generation",
                "Meeting effectiveness scoring",
                "Schedule optimization recommendations",
                "Multi-timezone support"
            ],
            "tools": [
                "find_optimal_slots",
                "create_meeting", 
                "detect_scheduling_conflicts",
                "analyze_meeting_patterns",
                "generate_agenda_suggestions",
                "calculate_workload_balance",
                "score_meeting_effectiveness",
                "optimize_meeting_schedule"
            ]
        }

async def main():
    """Main server entry point"""
    try:
        # Initialize server
        server = MeetingAssistantServer()
        await server.initialize()
        
        # Get server info
        info = await server.get_server_info()
        logger.info(f"Server Info: {info}")
        
        # Start the MCP server
        logger.info("Starting Smart Meeting Assistant MCP Server...")
        logger.info("Available tools:")
        for tool in info["tools"]:
            logger.info(f"  - {tool}")
            
        # Run the FastMCP server
        await mcp.run()
        
    except KeyboardInterrupt:
        logger.info("Server shutdown requested")
    except Exception as e:
        logger.error(f"Server error: {e}")
        raise
    finally:
        logger.info("Smart Meeting Assistant MCP Server stopped")

if __name__ == "__main__":
    asyncio.run(main())

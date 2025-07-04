"""
User Service

Core service for managing user data and preferences.
"""

import json
import os
from typing import List, Optional, Dict, Any
import logging

from ...models.user import User, UserPreferences

logger = logging.getLogger(__name__)

class UserService:
    """Core user service for user management"""
    
    def __init__(self, data_file: str = "data/users.json"):
        self.data_file = data_file
        self._users_cache: Optional[List[User]] = None
        
    async def load_users(self) -> List[User]:
        """Load users from JSON file"""
        if self._users_cache is not None:
            return self._users_cache
            
        try:
            if os.path.exists(self.data_file):
                with open(self.data_file, 'r', encoding='utf-8') as f:
                    users_data = json.load(f)
                    
                self._users_cache = [
                    User(**user_data) for user_data in users_data
                ]
            else:
                logger.warning(f"Users file {self.data_file} not found")
                self._users_cache = []
                
        except Exception as e:
            logger.error(f"Error loading users: {e}")
            self._users_cache = []
            
        return self._users_cache
        
    async def save_users(self, users: List[User]) -> bool:
        """Save users to JSON file"""
        try:
            # Ensure directory exists
            os.makedirs(os.path.dirname(self.data_file), exist_ok=True)
            
            users_data = [user.model_dump() for user in users]
            
            with open(self.data_file, 'w', encoding='utf-8') as f:
                json.dump(users_data, f, indent=2, default=str)
                
            self._users_cache = users
            logger.info(f"Saved {len(users)} users to {self.data_file}")
            return True
            
        except Exception as e:
            logger.error(f"Error saving users: {e}")
            return False
            
    async def get_user(self, user_id: str) -> Optional[User]:
        """Get a specific user by ID"""
        users = await self.load_users()
        
        for user in users:
            if user.user_id == user_id:
                return user
                
        return None
        
    async def get_users_by_ids(self, user_ids: List[str]) -> List[User]:
        """Get multiple users by their IDs"""
        users = await self.load_users()
        result = []
        
        for user in users:
            if user.user_id in user_ids:
                result.append(user)
                
        return result
        
    async def get_team_members(self, manager_id: str) -> List[User]:
        """Get all team members for a manager"""
        users = await self.load_users()
        team_members = []
        
        for user in users:
            if user.manager_id == manager_id:
                team_members.append(user)
                
        return team_members
        
    async def get_users_by_department(self, department: str) -> List[User]:
        """Get all users in a department"""
        users = await self.load_users()
        dept_users = []
        
        for user in users:
            if user.department.lower() == department.lower():
                dept_users.append(user)
                
        return dept_users
        
    async def create_user(self, user_data: Dict[str, Any]) -> User:
        """Create a new user"""
        users = await self.load_users()
        
        # Generate new user ID if not provided
        if "user_id" not in user_data:
            existing_ids = {u.user_id for u in users}
            counter = 1
            while f"user_{counter:03d}" in existing_ids:
                counter += 1
            user_data["user_id"] = f"user_{counter:03d}"
            
        user = User(**user_data)
        users.append(user)
        await self.save_users(users)
        
        logger.info(f"Created user {user.user_id}: {user.name}")
        return user
        
    async def update_user(self, user_id: str, updates: Dict[str, Any]) -> Optional[User]:
        """Update an existing user"""
        users = await self.load_users()
        
        for i, user in enumerate(users):
            if user.user_id == user_id:
                # Apply updates
                for field, value in updates.items():
                    if hasattr(user, field):
                        setattr(user, field, value)
                        
                await self.save_users(users)
                logger.info(f"Updated user {user_id}")
                return user
                
        logger.warning(f"User {user_id} not found for update")
        return None
        
    async def update_user_preferences(
        self,
        user_id: str,
        preferences: UserPreferences
    ) -> Optional[User]:
        """Update user preferences"""
        return await self.update_user(user_id, {"preferences": preferences})
        
    async def get_user_availability_summary(self, user_id: str) -> Dict[str, Any]:
        """Get a summary of user's availability preferences"""
        user = await self.get_user(user_id)
        if not user:
            return {}
            
        prefs = user.preferences
        
        return {
            "user_id": user_id,
            "name": user.name,
            "time_zone": prefs.time_zone,
            "working_hours": {
                "start": prefs.working_hours_start.strftime("%H:%M"),
                "end": prefs.working_hours_end.strftime("%H:%M")
            },
            "working_days": prefs.working_days,
            "lunch_break": {
                "start": prefs.lunch_break_start.strftime("%H:%M") if prefs.lunch_break_start else None,
                "end": prefs.lunch_break_end.strftime("%H:%M") if prefs.lunch_break_end else None
            },
            "productive_periods": prefs.productive_periods,
            "meeting_constraints": {
                "max_daily": prefs.max_daily_meetings,
                "max_consecutive": prefs.max_consecutive_meetings,
                "buffer_minutes": prefs.buffer_time_minutes,
                "avoid_back_to_back": prefs.avoid_back_to_back
            },
            "meeting_free_blocks": prefs.meeting_free_blocks
        }
        
    async def find_users_by_criteria(self, criteria: Dict[str, Any]) -> List[User]:
        """Find users matching specific criteria"""
        users = await self.load_users()
        results = []
        
        for user in users:
            match = True
            
            # Check each criteria
            for field, value in criteria.items():
                if field == "department" and user.department.lower() != value.lower():
                    match = False
                    break
                elif field == "role" and user.role.lower() != value.lower():
                    match = False
                    break
                elif field == "time_zone" and user.preferences.time_zone != value:
                    match = False
                    break
                elif field == "is_active" and user.is_active != value:
                    match = False
                    break
                    
            if match:
                results.append(user)
                
        return results
        
    async def get_organization_structure(self) -> Dict[str, Any]:
        """Get the organization structure"""
        users = await self.load_users()
        
        # Build hierarchy
        managers = {}
        departments = {}
        
        for user in users:
            # Group by department
            if user.department not in departments:
                departments[user.department] = []
            departments[user.department].append({
                "user_id": user.user_id,
                "name": user.name,
                "role": user.role,
                "manager_id": user.manager_id
            })
            
            # Track managers
            if user.manager_id:
                if user.manager_id not in managers:
                    managers[user.manager_id] = []
                managers[user.manager_id].append(user.user_id)
                
        return {
            "departments": departments,
            "reporting_structure": managers,
            "total_users": len(users)
        }
        
    def clear_cache(self):
        """Clear the users cache"""
        self._users_cache = None

"""
User service for authentication and authorization.
"""

from typing import Optional, Dict, Any
from datetime import datetime

from database.database_manager import DatabaseManager
from models.user import User, UserRole


class UserService:
    """Service for user authentication and authorization."""
    
    def __init__(self, db_manager: DatabaseManager):
        """Initialize service with database manager."""
        self.db_manager = db_manager
        self.current_user: Optional[User] = None
    
    def authenticate(self, username: str, password: str) -> Optional[User]:
        """Authenticate user with username and password."""
        try:
            # Ensure database is connected
            self.db_manager.ensure_connected()
            
            user = self.db_manager.get_user_by_username(username)
            if not user:
                return None
            
            # Check if account is locked
            if user.is_locked():
                return None
            
            # Check password
            if user.check_password(password):
                # Reset login attempts on successful login
                user.reset_login_attempts()
                user.last_login = datetime.now()
                if user.id:
                    self.db_manager.update_user_login(user.id, user.last_login)
                self.current_user = user
                return user
            else:
                # Increment failed login attempts
                user.increment_login_attempts()
                if user.id:
                    self.db_manager.update_user(user)
                return None
                
        except Exception as e:
            print(f"Authentication error: {e}")
            return None
    
    def logout(self):
        """Logout current user."""
        self.current_user = None
    
    def get_current_user(self) -> Optional[User]:
        """Get current logged in user."""
        return self.current_user
    
    def has_permission(self, permission: str) -> bool:
        """Check if current user has specific permission."""
        if not self.current_user:
            return False
        return self.current_user.has_permission(permission)
    
    def is_admin(self) -> bool:
        """Check if current user is admin."""
        if not self.current_user:
            return False
        return self.current_user.role == UserRole.ADMIN
    
    def is_manager(self) -> bool:
        """Check if current user is manager."""
        if not self.current_user:
            return False
        return self.current_user.role in [UserRole.ADMIN, UserRole.MANAGER]
    
    def create_user(self, user_data: Dict[str, Any]) -> User:
        """Create new user."""
        # Validate required fields
        required_fields = ['username', 'full_name', 'role']
        for field in required_fields:
            if field not in user_data or not user_data[field]:
                raise ValueError(f"Field '{field}' is required")
        
        # Check if username already exists
        existing_user = self.db_manager.get_user_by_username(user_data['username'])
        if existing_user:
            raise ValueError("Username already exists")
        
        # Create user object
        user = User(**user_data)
        
        # Set default password if not provided
        if 'password' in user_data:
            user.set_password(user_data['password'])
        else:
            user.set_password("password123")  # Default password
        
        # Save to database
        user_id = self.db_manager.create_user(user)
        user.id = user_id
        
        return user
    
    def update_user(self, user_id: int, user_data: Dict[str, Any]) -> bool:
        """Update user."""
        # Get existing user
        user = self.db_manager.get_user_by_username(user_data.get('username', ''))
        if user and user.id != user_id:
            raise ValueError("Username already exists")
        
        # Update password if provided
        if 'password' in user_data and user_data['password']:
            user.set_password(user_data['password'])
        
        # Update other fields
        for key, value in user_data.items():
            if hasattr(user, key) and key != 'password':
                setattr(user, key, value)
        
        # Update in database
        return self.db_manager.update_user(user)
    
    def change_password(self, user_id: int, old_password: str, 
                       new_password: str) -> bool:
        """Change user password."""
        # Get user by ID (this would need a new method in DatabaseManager)
        # For now, we'll use a placeholder
        return False
    
    def get_user_permissions(self) -> Dict[str, bool]:
        """Get current user permissions."""
        if not self.current_user:
            return {}
        
        permissions = [
            'read', 'write', 'delete', 'export', 'reports', 'admin'
        ]
        
        return {
            permission: self.current_user.has_permission(permission)
            for permission in permissions
        } 
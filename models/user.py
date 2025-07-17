"""
User model for authentication and authorization.
"""

from datetime import datetime
from typing import Optional
from dataclasses import dataclass
from enum import Enum
import hashlib
import secrets


class UserRole(Enum):
    """User role enumeration."""
    ADMIN = "admin"
    MANAGER = "manager"
    OFFICER = "officer"
    VIEWER = "viewer"


class UserStatus(Enum):
    """User status enumeration."""
    ACTIVE = "active"
    INACTIVE = "inactive"
    LOCKED = "locked"


@dataclass
class User:
    """User data model."""
    
    id: Optional[int] = None
    username: str = ""
    email: str = ""
    full_name: str = ""
    role: UserRole = UserRole.OFFICER
    status: UserStatus = UserStatus.ACTIVE
    
    # Password fields (hashed)
    password_hash: str = ""
    salt: str = ""
    
    # Metadata
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    last_login: Optional[datetime] = None
    login_attempts: int = 0
    locked_until: Optional[datetime] = None
    
    def __post_init__(self):
        """Initialize default values."""
        if self.created_at is None:
            self.created_at = datetime.now()
        if self.updated_at is None:
            self.updated_at = datetime.now()
        if not self.salt:
            self.salt = secrets.token_hex(16)
    
    def set_password(self, password: str):
        """Set password with salt and hash."""
        self.salt = secrets.token_hex(16)
        self.password_hash = self._hash_password(password, self.salt)
    
    def check_password(self, password: str) -> bool:
        """Check if provided password matches."""
        return self.password_hash == self._hash_password(password, self.salt)
    
    def _hash_password(self, password: str, salt: str) -> str:
        """Hash password with salt."""
        return hashlib.sha256((password + salt).encode()).hexdigest()
    
    def is_locked(self) -> bool:
        """Check if user account is locked."""
        if self.status == UserStatus.LOCKED:
            return True
        if self.locked_until and datetime.now() < self.locked_until:
            return True
        return False
    
    def increment_login_attempts(self):
        """Increment failed login attempts."""
        self.login_attempts += 1
        if self.login_attempts >= 5:
            self.status = UserStatus.LOCKED
            self.locked_until = datetime.now().replace(hour=datetime.now().hour + 1)
    
    def reset_login_attempts(self):
        """Reset failed login attempts."""
        self.login_attempts = 0
        self.locked_until = None
        if self.status == UserStatus.LOCKED:
            self.status = UserStatus.ACTIVE
    
    def has_permission(self, permission: str) -> bool:
        """Check if user has specific permission."""
        permissions = {
            UserRole.ADMIN: ['all'],
            UserRole.MANAGER: ['read', 'write', 'delete', 'export', 'reports'],
            UserRole.OFFICER: ['read', 'write', 'export'],
            UserRole.VIEWER: ['read']
        }
        
        user_permissions = permissions.get(self.role, [])
        return 'all' in user_permissions or permission in user_permissions
    
    def to_dict(self) -> dict:
        """Convert to dictionary for database storage."""
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'full_name': self.full_name,
            'role': self.role.value,
            'status': self.status.value,
            'password_hash': self.password_hash,
            'salt': self.salt,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'last_login': self.last_login.isoformat() if self.last_login else None,
            'login_attempts': self.login_attempts,
            'locked_until': self.locked_until.isoformat() if self.locked_until else None
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'User':
        """Create User instance from dictionary."""
        # Convert string values back to enums
        if 'role' in data and data['role']:
            data['role'] = UserRole(data['role'])
        if 'status' in data and data['status']:
            data['status'] = UserStatus(data['status'])
        
        # Convert datetime strings back to datetime objects
        for datetime_field in ['created_at', 'updated_at', 'last_login', 'locked_until']:
            if datetime_field in data and data[datetime_field]:
                data[datetime_field] = datetime.fromisoformat(data[datetime_field])
        
        return cls(**data) 
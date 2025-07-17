"""
Database manager for SQLite operations.
"""

import sqlite3
from typing import List, Optional
from datetime import datetime
from pathlib import Path

from models.offender import Offender
from models.user import User


class DatabaseManager:
    """Database manager for SQLite operations."""
    
    def __init__(self, db_path: str = "data/database.db"):
        """Initialize database manager."""
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self.connection = None
        self._is_connected = False
    
    def connect(self):
        """Connect to database."""
        if not self._is_connected:
            self.connection = sqlite3.connect(
                str(self.db_path),
                detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES,
                check_same_thread=False
            )
            self.connection.row_factory = sqlite3.Row
            self._is_connected = True
    
    def disconnect(self):
        """Disconnect from database."""
        if self.connection and self._is_connected:
            self.connection.close()
            self.connection = None
            self._is_connected = False
    
    def __enter__(self):
        """Context manager entry."""
        self.connect()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.disconnect()
    
    def ensure_connected(self):
        """Ensure database is connected."""
        if not self._is_connected or not self.connection:
            self.connect()
    
    def execute(self, query: str, params: tuple = ()) -> sqlite3.Cursor:
        """Execute SQL query."""
        self.ensure_connected()
        return self.connection.execute(query, params)
    
    def executemany(self, query: str, params_list: List[tuple]) -> sqlite3.Cursor:
        """Execute SQL query with multiple parameters."""
        self.ensure_connected()
        return self.connection.executemany(query, params_list)
    
    def commit(self):
        """Commit changes."""
        if self.connection and self._is_connected:
            self.connection.commit()
    
    def rollback(self):
        """Rollback changes."""
        if self.connection and self._is_connected:
            self.connection.rollback()
    
    # Offender operations
    def create_offender(self, offender: Offender) -> int:
        """Create new offender record."""
        query = """
        INSERT INTO offenders (
            case_number, full_name, gender, birth_date, address, occupation,
            crime, case_type, sentence_number, decision_number, start_date,
            duration_months, reduced_months, reduction_date, reduction_count,
            completion_date, status, days_remaining, risk_level, risk_percentage,
            created_at, updated_at, created_by, notes
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
        
        params = (
            offender.case_number, offender.full_name, offender.gender.value if hasattr(offender.gender, 'value') else str(offender.gender),
            offender.birth_date, offender.address, offender.occupation,
            offender.crime, offender.case_type.value if hasattr(offender.case_type, 'value') else str(offender.case_type), offender.sentence_number,
            offender.decision_number, offender.start_date, offender.duration_months,
            offender.reduced_months, offender.reduction_date, offender.reduction_count,
            offender.completion_date, offender.status.value if hasattr(offender.status, 'value') else str(offender.status), offender.days_remaining,
            offender.risk_level.value if hasattr(offender.risk_level, 'value') else str(offender.risk_level), offender.risk_percentage,
            offender.created_at, offender.updated_at, offender.created_by,
            offender.notes
        )
        
        cursor = self.execute(query, params)
        self.commit()
        return cursor.lastrowid
    
    def get_offender(self, offender_id: int) -> Optional[Offender]:
        """Get offender by ID."""
        query = "SELECT * FROM offenders WHERE id = ?"
        cursor = self.execute(query, (offender_id,))
        row = cursor.fetchone()
        
        if row:
            return self._row_to_offender(row)
        return None
    
    def get_all_offenders(self) -> List[Offender]:
        """Get all offenders."""
        query = "SELECT * FROM offenders ORDER BY created_at DESC"
        cursor = self.execute(query)
        return [self._row_to_offender(row) for row in cursor.fetchall()]
    
    def update_offender(self, offender: Offender) -> bool:
        """Update offender record."""
        query = """
        UPDATE offenders SET
            case_number = ?, full_name = ?, gender = ?, birth_date = ?,
            address = ?, occupation = ?, crime = ?, case_type = ?,
            sentence_number = ?, decision_number = ?, start_date = ?,
            duration_months = ?, reduced_months = ?, reduction_date = ?,
            reduction_count = ?, completion_date = ?, status = ?,
            days_remaining = ?, risk_level = ?, risk_percentage = ?,
            updated_at = ?, notes = ?
        WHERE id = ?
        """
        
        params = (
            offender.case_number, offender.full_name, offender.gender.value if hasattr(offender.gender, 'value') else str(offender.gender),
            offender.birth_date, offender.address, offender.occupation,
            offender.crime, offender.case_type.value if hasattr(offender.case_type, 'value') else str(offender.case_type), offender.sentence_number,
            offender.decision_number, offender.start_date, offender.duration_months,
            offender.reduced_months, offender.reduction_date, offender.reduction_count,
            offender.completion_date, offender.status.value if hasattr(offender.status, 'value') else str(offender.status), offender.days_remaining,
            offender.risk_level.value if hasattr(offender.risk_level, 'value') else str(offender.risk_level), offender.risk_percentage,
            datetime.now(), offender.notes, offender.id
        )
        
        cursor = self.execute(query, params)
        self.commit()
        return cursor.rowcount > 0
    
    def delete_offender(self, offender_id: int) -> bool:
        """Delete offender record."""
        query = "DELETE FROM offenders WHERE id = ?"
        cursor = self.execute(query, (offender_id,))
        self.commit()
        return cursor.rowcount > 0
    
    def search_offenders(self, search_term: str) -> List[Offender]:
        """Search offenders by name or case number."""
        query = """
        SELECT * FROM offenders 
        WHERE full_name LIKE ? OR case_number LIKE ?
        ORDER BY created_at DESC
        """
        search_pattern = f"%{search_term}%"
        cursor = self.execute(query, (search_pattern, search_pattern))
        return [self._row_to_offender(row) for row in cursor.fetchall()]
    
    def get_offenders_by_status(self, status: str) -> List[Offender]:
        """Get offenders by status."""
        query = "SELECT * FROM offenders WHERE status = ? ORDER BY created_at DESC"
        cursor = self.execute(query, (status,))
        return [self._row_to_offender(row) for row in cursor.fetchall()]
    
    def _row_to_offender(self, row: sqlite3.Row) -> Offender:
        """Convert database row to Offender object."""
        data = dict(row)
        
        # Convert enum values
        from models.offender import Offender
        return Offender.from_dict(data)
    
    # User operations
    def create_user(self, user: User) -> int:
        """Create new user record."""
        query = """
        INSERT INTO users (
            username, email, full_name, role, status, password_hash,
            salt, created_at, updated_at, login_attempts
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
        
        params = (
            user.username, user.email, user.full_name, user.role.value,
            user.status.value, user.password_hash, user.salt,
            user.created_at, user.updated_at, user.login_attempts
        )
        
        cursor = self.execute(query, params)
        self.commit()
        return cursor.lastrowid
    
    def get_user_by_username(self, username: str) -> Optional[User]:
        """Get user by username."""
        query = "SELECT * FROM users WHERE username = ?"
        cursor = self.execute(query, (username,))
        row = cursor.fetchone()
        
        if row:
            return self._row_to_user(row)
        return None
    
    def update_user_login(self, user_id: int, last_login: datetime):
        """Update user last login time."""
        query = "UPDATE users SET last_login = ? WHERE id = ?"
        self.execute(query, (last_login, user_id))
        self.commit()
    
    def update_user(self, user: User) -> bool:
        """Update user record."""
        query = """
        UPDATE users SET
            email = ?, full_name = ?, role = ?, status = ?,
            password_hash = ?, salt = ?, updated_at = ?,
            login_attempts = ?, locked_until = ?
        WHERE id = ?
        """
        
        params = (
            user.email, user.full_name, user.role.value, user.status.value,
            user.password_hash, user.salt, datetime.now(),
            user.login_attempts, user.locked_until, user.id
        )
        
        cursor = self.execute(query, params)
        self.commit()
        return cursor.rowcount > 0
    
    def _row_to_user(self, row: sqlite3.Row) -> User:
        """Convert database row to User object."""
        data = dict(row)
        
        # Convert enum values
        from models.user import UserRole, UserStatus
        
        if data['role']:
            data['role'] = UserRole(data['role'])
        if data['status']:
            data['status'] = UserStatus(data['status'])
        
        return User(**data) 
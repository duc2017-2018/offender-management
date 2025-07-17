"""
Violation model for managing offender violations.
"""

from datetime import datetime, date
from typing import Optional
from dataclasses import dataclass
from enum import Enum


class ViolationType(Enum):
    """Violation type enumeration."""
    MINOR = "Vi phạm nhẹ"
    MODERATE = "Vi phạm vừa"
    SERIOUS = "Vi phạm nghiêm trọng"
    CRITICAL = "Vi phạm rất nghiêm trọng"


class ViolationStatus(Enum):
    """Violation status enumeration."""
    PENDING = "Chờ xử lý"
    PROCESSING = "Đang xử lý"
    RESOLVED = "Đã xử lý"
    DISMISSED = "Đã bỏ qua"


@dataclass
class Violation:
    """Violation data model."""
    
    id: Optional[int] = None
    offender_id: Optional[int] = None
    
    # Violation details
    violation_type: ViolationType = ViolationType.MINOR
    description: str = ""  # Mô tả vi phạm
    location: str = ""  # Địa điểm vi phạm
    violation_date: Optional[date] = None
    report_date: Optional[date] = None
    
    # Consequences
    penalty: str = ""  # Hình phạt
    additional_months: int = 0  # Thêm tháng thử thách
    warning_level: int = 0  # Mức cảnh báo
    
    # Status
    status: ViolationStatus = ViolationStatus.PENDING
    resolution_notes: str = ""  # Ghi chú xử lý
    resolved_by: Optional[int] = None
    resolved_date: Optional[date] = None
    
    # Metadata
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    created_by: Optional[int] = None
    
    def __post_init__(self):
        """Initialize default values."""
        if self.created_at is None:
            self.created_at = datetime.now()
        if self.updated_at is None:
            self.updated_at = datetime.now()
        if self.report_date is None:
            self.report_date = date.today()
    
    def get_severity_score(self) -> int:
        """Calculate severity score based on violation type."""
        severity_scores = {
            ViolationType.MINOR: 1,
            ViolationType.MODERATE: 2,
            ViolationType.SERIOUS: 3,
            ViolationType.CRITICAL: 4
        }
        return severity_scores.get(self.violation_type, 1)
    
    def to_dict(self) -> dict:
        """Convert to dictionary for database storage."""
        return {
            'id': self.id,
            'offender_id': self.offender_id,
            'violation_type': self.violation_type.value,
            'description': self.description,
            'location': self.location,
            'violation_date': self.violation_date.isoformat() if self.violation_date else None,
            'report_date': self.report_date.isoformat() if self.report_date else None,
            'penalty': self.penalty,
            'additional_months': self.additional_months,
            'warning_level': self.warning_level,
            'status': self.status.value,
            'resolution_notes': self.resolution_notes,
            'resolved_by': self.resolved_by,
            'resolved_date': self.resolved_date.isoformat() if self.resolved_date else None,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'created_by': self.created_by
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'Violation':
        """Create Violation instance from dictionary."""
        # Convert string values back to enums
        if 'violation_type' in data and data['violation_type']:
            data['violation_type'] = ViolationType(data['violation_type'])
        if 'status' in data and data['status']:
            data['status'] = ViolationStatus(data['status'])
        
        # Convert date strings back to date objects
        for date_field in ['violation_date', 'report_date', 'resolved_date']:
            if date_field in data and data[date_field]:
                data[date_field] = datetime.fromisoformat(data[date_field]).date()
        
        # Convert datetime strings back to datetime objects
        for datetime_field in ['created_at', 'updated_at']:
            if datetime_field in data and data[datetime_field]:
                data[datetime_field] = datetime.fromisoformat(data[datetime_field])
        
        return cls(**data) 
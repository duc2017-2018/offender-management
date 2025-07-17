"""
Case model for managing case information.
"""

from datetime import datetime, date
from typing import Optional
from dataclasses import dataclass
from enum import Enum


class CaseStatus(Enum):
    """Case status enumeration."""
    ACTIVE = "Đang xử lý"
    COMPLETED = "Đã hoàn thành"
    SUSPENDED = "Tạm đình chỉ"
    CANCELLED = "Đã hủy"


@dataclass
class Case:
    """Case data model."""
    
    id: Optional[int] = None
    case_number: str = ""  # Số vụ án
    case_name: str = ""  # Tên vụ án
    offender_id: Optional[int] = None
    
    # Court information
    court_name: str = ""  # Tên tòa án
    judge_name: str = ""  # Tên thẩm phán
    prosecutor_name: str = ""  # Tên kiểm sát viên
    
    # Case details
    crime_description: str = ""  # Mô tả tội danh
    sentence_details: str = ""  # Chi tiết bản án
    decision_details: str = ""  # Chi tiết quyết định
    
    # Dates
    case_date: Optional[date] = None  # Ngày xử án
    decision_date: Optional[date] = None  # Ngày ra quyết định
    effective_date: Optional[date] = None  # Ngày có hiệu lực
    
    # Status
    status: CaseStatus = CaseStatus.ACTIVE
    
    # Metadata
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    created_by: Optional[int] = None
    notes: str = ""
    
    def __post_init__(self):
        """Initialize default values."""
        if self.created_at is None:
            self.created_at = datetime.now()
        if self.updated_at is None:
            self.updated_at = datetime.now()
    
    def to_dict(self) -> dict:
        """Convert to dictionary for database storage."""
        return {
            'id': self.id,
            'case_number': self.case_number,
            'case_name': self.case_name,
            'offender_id': self.offender_id,
            'court_name': self.court_name,
            'judge_name': self.judge_name,
            'prosecutor_name': self.prosecutor_name,
            'crime_description': self.crime_description,
            'sentence_details': self.sentence_details,
            'decision_details': self.decision_details,
            'case_date': self.case_date.isoformat() if self.case_date else None,
            'decision_date': self.decision_date.isoformat() if self.decision_date else None,
            'effective_date': self.effective_date.isoformat() if self.effective_date else None,
            'status': self.status.value,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'created_by': self.created_by,
            'notes': self.notes
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'Case':
        """Create Case instance from dictionary."""
        # Convert string values back to enums
        if 'status' in data and data['status']:
            data['status'] = CaseStatus(data['status'])
        
        # Convert date strings back to date objects
        for date_field in ['case_date', 'decision_date', 'effective_date']:
            if date_field in data and data[date_field]:
                data[date_field] = datetime.fromisoformat(data[date_field]).date()
        
        # Convert datetime strings back to datetime objects
        for datetime_field in ['created_at', 'updated_at']:
            if datetime_field in data and data[datetime_field]:
                data[datetime_field] = datetime.fromisoformat(data[datetime_field])
        
        return cls(**data) 
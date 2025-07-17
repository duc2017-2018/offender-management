"""
Reduction model for managing sentence reductions.
"""

from datetime import datetime, date
from typing import Optional
from dataclasses import dataclass
from enum import Enum


class ReductionType(Enum):
    """Reduction type enumeration."""
    REGULAR = "Giảm thường xuyên"
    SPECIAL = "Giảm đặc biệt"
    COMPASSIONATE = "Giảm nhân đạo"


class ReductionStatus(Enum):
    """Reduction status enumeration."""
    PENDING = "Chờ xét duyệt"
    APPROVED = "Đã phê duyệt"
    REJECTED = "Đã từ chối"
    CANCELLED = "Đã hủy"


@dataclass
class Reduction:
    """Reduction data model."""
    
    id: Optional[int] = None
    offender_id: Optional[int] = None
    
    # Reduction details
    reduction_type: ReductionType = ReductionType.REGULAR
    months_reduced: int = 0  # Số tháng được giảm
    reason: str = ""  # Lý do giảm
    evidence: str = ""  # Bằng chứng
    
    # Application details
    application_date: Optional[date] = None
    decision_date: Optional[date] = None
    effective_date: Optional[date] = None
    
    # Status
    status: ReductionStatus = ReductionStatus.PENDING
    decision_notes: str = ""  # Ghi chú quyết định
    decided_by: Optional[int] = None
    
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
        if self.application_date is None:
            self.application_date = date.today()
    
    def is_approved(self) -> bool:
        """Check if reduction is approved."""
        return self.status == ReductionStatus.APPROVED
    
    def is_pending(self) -> bool:
        """Check if reduction is pending."""
        return self.status == ReductionStatus.PENDING
    
    def to_dict(self) -> dict:
        """Convert to dictionary for database storage."""
        return {
            'id': self.id,
            'offender_id': self.offender_id,
            'reduction_type': self.reduction_type.value if hasattr(self.reduction_type, 'value') else str(self.reduction_type),
            'months_reduced': self.months_reduced,
            'reason': self.reason,
            'evidence': self.evidence,
            'application_date': self.application_date.isoformat() 
                if self.application_date else None,
            'decision_date': self.decision_date.isoformat() 
                if self.decision_date else None,
            'effective_date': self.effective_date.isoformat() 
                if self.effective_date else None,
            'status': self.status.value if hasattr(self.status, 'value') else str(self.status),
            'decision_notes': self.decision_notes,
            'decided_by': self.decided_by,
            'created_at': self.created_at.isoformat() 
                if self.created_at else None,
            'updated_at': self.updated_at.isoformat() 
                if self.updated_at else None,
            'created_by': self.created_by
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'Reduction':
        """Create Reduction instance from dictionary."""
        # Convert string values back to enums
        if 'reduction_type' in data and data['reduction_type']:
            data['reduction_type'] = ReductionType(data['reduction_type'])
        if 'status' in data and data['status']:
            data['status'] = ReductionStatus(data['status'])
        
        # Convert date strings back to date objects
        for date_field in ['application_date', 'decision_date', 'effective_date']:
            if date_field in data and data[date_field] and isinstance(data[date_field], str):
                data[date_field] = datetime.fromisoformat(data[date_field]).date()
        
        # Convert datetime strings back to datetime objects
        for datetime_field in ['created_at', 'updated_at']:
            if datetime_field in data and data[datetime_field] and isinstance(data[datetime_field], str):
                data[datetime_field] = datetime.fromisoformat(data[datetime_field])
        
        return cls(**data) 
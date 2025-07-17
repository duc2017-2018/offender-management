"""
Offender model for managing offender information.
"""

from datetime import datetime, date
from typing import Optional
from dataclasses import dataclass
from enum import Enum


class Gender(Enum):
    """Gender enumeration."""
    MALE = "Nam"
    FEMALE = "Nữ"


class CaseType(Enum):
    """Case type enumeration."""
    SUSPENDED_SENTENCE = "Án treo"
    PROBATION = "Cải tạo không giam giữ"
    POSTPONEMENT = "Hoãn chấp hành án"
    CONDITIONAL_RELEASE = "Tha tù trước thời hạn có điều kiện"
    OTHER = "Khác"


class Status(Enum):
    """Offender status enumeration."""
    ACTIVE = "Đang chấp hành"
    COMPLETED = "Đã hoàn thành"
    VIOLATION = "Vi phạm"
    EXPIRING_SOON = "Sắp kết thúc"


class RiskLevel(Enum):
    """Risk level enumeration."""
    LOW = "Thấp"
    MEDIUM = "Trung bình"
    HIGH = "Cao"


@dataclass
class Offender:
    """Offender data model."""
    
    # Basic information
    id: Optional[int] = None
    id_number: str = ""
    case_number: str = ""  # Số hồ sơ: 40CE0625/405LF
    full_name: str = ""
    gender: Gender = Gender.MALE
    birth_date: Optional[date] = None
    address: str = ""
    occupation: str = ""
    crime: str = ""  # Tội danh
    case_type: CaseType = CaseType.SUSPENDED_SENTENCE
    phone: str = ""
    ward: str = ""
    sentence: str = ""
    
    # Case information
    sentence_number: str = ""  # Số bản án
    decision_number: str = ""  # Số quyết định THA
    start_date: Optional[date] = None
    duration_months: int = 0  # Thời gian thử thách (tháng)
    reduced_months: int = 0  # Được giảm (tháng)
    reduction_date: Optional[date] = None
    reduction_count: int = 0  # Số lần giảm
    
    # Calculated fields
    completion_date: Optional[date] = None
    status: Status = Status.ACTIVE
    days_remaining: int = 0
    risk_level: RiskLevel = RiskLevel.MEDIUM
    risk_percentage: float = 0.0
    
    # Metadata
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    created_by: Optional[int] = None
    notes: str = ""
    
    def __post_init__(self):
        """Calculate derived fields after initialization and ensure Enum fields are valid."""
        # Convert string fields to Enum if needed
        if isinstance(self.gender, str):
            try:
                self.gender = Gender(self.gender)
            except Exception:
                self.gender = Gender.MALE
        if isinstance(self.case_type, str):
            try:
                self.case_type = CaseType(self.case_type)
            except Exception:
                self.case_type = CaseType.SUSPENDED_SENTENCE
        if isinstance(self.status, str):
            try:
                self.status = Status(self.status)
            except Exception:
                self.status = Status.ACTIVE
        if isinstance(self.risk_level, str):
            try:
                self.risk_level = RiskLevel(self.risk_level)
            except Exception:
                self.risk_level = RiskLevel.MEDIUM
        # Existing logic
        if self.created_at is None:
            self.created_at = datetime.now()
        if self.updated_at is None:
            self.updated_at = datetime.now()
        self._calculate_completion_date()
        self._calculate_status()
        self._calculate_days_remaining()
    
    def _calculate_completion_date(self):
        """Calculate completion date based on start date and duration."""
        if self.start_date and self.duration_months > 0:
            # Calculate base completion date
            from dateutil.relativedelta import relativedelta
            base_completion = self.start_date + \
                relativedelta(months=self.duration_months)
            # Apply reductions
            if self.reduced_months > 0:
                self.completion_date = base_completion - \
                    relativedelta(months=self.reduced_months)
            else:
                self.completion_date = base_completion
        else:
            self.completion_date = None
    
    def _calculate_status(self):
        """Calculate current status based on completion date."""
        if not self.completion_date:
            self.status = Status.ACTIVE
            return
        today = date.today()
        days_until_completion = (
            self.completion_date - today
        ).days
        if days_until_completion <= 0:
            self.status = Status.COMPLETED
        elif days_until_completion <= 5:  # Cảnh báo trước 5 ngày
            self.status = Status.EXPIRING_SOON
        else:
            self.status = Status.ACTIVE
    
    def _calculate_days_remaining(self):
        """Calculate days remaining until completion."""
        if self.completion_date:
            today = date.today()
            days = (
                self.completion_date - today
            ).days
            self.days_remaining = max(0, days)
        else:
            self.days_remaining = 0
    
    def is_eligible_for_reduction(self) -> bool:
        """Check if offender is eligible for sentence reduction."""
        if not self.start_date or not self.completion_date:
            return False
        today = date.today()
        served_months = (
            today - self.start_date
        ).days / 30.44
        # Must serve at least 1/3 of sentence
        required_months = self.duration_months / 3
        return served_months >= required_months
    
    def get_next_reduction_date(self) -> Optional[date]:
        """Calculate next possible reduction date."""
        if not self.is_eligible_for_reduction():
            return None
        # Can apply for reduction every 6 months
        from dateutil.relativedelta import relativedelta
        last_reduction = self.reduction_date or self.start_date
        if last_reduction is None:
            return None
        return last_reduction + relativedelta(months=6)

    def get_days_remaining(self) -> int:
        """Trả về số ngày còn lại cho đến ngày hoàn thành án."""
        if self.completion_date:
            today = date.today()
            days = (self.completion_date - today).days
            return max(0, days)
        return 0
    
    def to_dict(self) -> dict:
        """Convert to dictionary for database storage."""
        return {
            'id': self.id,
            'id_number': self.id_number,
            'case_number': self.case_number,
            'full_name': self.full_name,
            'gender': self.gender.value if hasattr(self.gender, 'value') else str(self.gender),
            'birth_date': self.birth_date.isoformat() if self.birth_date else None,
            'address': self.address,
            'occupation': self.occupation,
            'crime': self.crime,
            'case_type': self.case_type.value if hasattr(self.case_type, 'value') else str(self.case_type),
            'sentence_number': self.sentence_number,
            'decision_number': self.decision_number,
            'start_date': self.start_date.isoformat() if self.start_date else None,
            'duration_months': self.duration_months,
            'reduced_months': self.reduced_months,
            'reduction_date': self.reduction_date.isoformat() if self.reduction_date else None,
            'reduction_count': self.reduction_count,
            'completion_date': self.completion_date.isoformat() if self.completion_date else None,
            'status': self.status.value if hasattr(self.status, 'value') else str(self.status),
            'days_remaining': self.days_remaining,
            'risk_level': self.risk_level.value if hasattr(self.risk_level, 'value') else str(self.risk_level),
            'risk_percentage': self.risk_percentage,
            'phone': self.phone,
            'ward': self.ward,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'created_by': self.created_by,
            'notes': self.notes
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'Offender':
        """Create Offender instance from dictionary, with robust Enum conversion."""
        # Convert string values back to enums, fallback to default if invalid
        if 'gender' in data and data['gender'] and not hasattr(data['gender'], 'value'):
            try:
                data['gender'] = Gender(data['gender'])
            except Exception:
                data['gender'] = Gender.MALE
        if 'case_type' in data and data['case_type'] and not hasattr(data['case_type'], 'value'):
            try:
                data['case_type'] = CaseType(data['case_type'])
            except Exception:
                data['case_type'] = CaseType.SUSPENDED_SENTENCE
        if 'status' in data and data['status'] and not hasattr(data['status'], 'value'):
            try:
                data['status'] = Status(data['status'])
            except Exception:
                data['status'] = Status.ACTIVE
        if 'risk_level' in data and data['risk_level'] and not hasattr(data['risk_level'], 'value'):
            try:
                data['risk_level'] = RiskLevel(data['risk_level'])
            except Exception:
                data['risk_level'] = RiskLevel.MEDIUM
        # Convert date strings back to date objects
        for date_field in ['birth_date', 'start_date', 'reduction_date', 'completion_date']:
            if date_field in data and data[date_field] and isinstance(data[date_field], str):
                data[date_field] = datetime.fromisoformat(data[date_field]).date()
        # Convert datetime strings back to datetime objects
        for datetime_field in ['created_at', 'updated_at']:
            if datetime_field in data and data[datetime_field] and isinstance(data[datetime_field], str):
                data[datetime_field] = datetime.fromisoformat(data[datetime_field])
        return cls(**data) 
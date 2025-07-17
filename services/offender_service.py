"""
Offender service for business logic.
"""

from typing import List, Optional, Dict, Any
from datetime import datetime, date, timedelta
from dateutil.relativedelta import relativedelta

from database.database_manager import DatabaseManager
from models.offender import Offender, Status, RiskLevel
from models.violation import Violation
from models.reduction import Reduction


class OffenderService:
    """Service for offender business logic."""
    
    def __init__(self, db_manager: DatabaseManager):
        """Initialize service with database manager."""
        self.db_manager = db_manager
    
    def create_offender(self, offender_data: Dict[str, Any]) -> Offender:
        """Create new offender with validation and calculations."""
        # Create offender object
        offender = Offender(**offender_data)
        
        # Validate data
        self._validate_offender(offender)
        
        # Calculate derived fields
        self._calculate_offender_fields(offender)
        
        # Save to database
        offender_id = self.db_manager.create_offender(offender)
        offender.id = offender_id
        
        return offender
    
    def update_offender(self, offender_id: int, offender_data: Dict[str, Any]) -> bool:
        """Update offender with validation and recalculations."""
        # Get existing offender
        offender = self.db_manager.get_offender(offender_id)
        if not offender:
            raise ValueError(f"Offender with ID {offender_id} not found")

        # Update fields, convert string to Enum if needed
        from models.offender import Gender, CaseType, Status, RiskLevel
        for key, value in offender_data.items():
            if hasattr(offender, key):
                # Enum conversion
                if key == "gender" and isinstance(value, str):
                    value = Gender(value)
                elif key == "case_type" and isinstance(value, str):
                    value = CaseType(value)
                elif key == "status" and isinstance(value, str):
                    value = Status(value)
                elif key == "risk_level" and isinstance(value, str):
                    value = RiskLevel(value)
                setattr(offender, key, value)

        # Validate data
        self._validate_offender(offender)

        # Recalculate derived fields
        self._calculate_offender_fields(offender)

        # Update in database
        return self.db_manager.update_offender(offender)
    
    def delete_offender(self, offender_id: int) -> bool:
        """Delete offender."""
        return self.db_manager.delete_offender(offender_id)
    
    def get_offender(self, offender_id: int) -> Optional[Offender]:
        """Get offender by ID."""
        return self.db_manager.get_offender(offender_id)
    
    def get_all_offenders(self) -> List[Offender]:
        """Get all offenders."""
        return self.db_manager.get_all_offenders()
    
    def search_offenders(self, search_term: str) -> List[Offender]:
        """Search offenders."""
        return self.db_manager.search_offenders(search_term)
    
    def get_offenders_by_status(self, status: str) -> List[Offender]:
        """Get offenders by status."""
        return self.db_manager.get_offenders_by_status(status)
    
    def get_expiring_offenders(self, days: int = 5) -> List[Offender]:
        """Get offenders expiring within specified days."""
        offenders = self.get_all_offenders()
        today = date.today()
        expiring = []
        
        for offender in offenders:
            if offender.completion_date:
                days_until = (offender.completion_date - today).days
                if 0 <= days_until <= days:
                    expiring.append(offender)
        
        return expiring
    
    def get_completed_offenders(self) -> List[Offender]:
        """Get offenders who have completed their sentence."""
        return self.get_offenders_by_status(Status.COMPLETED.value)
    
    def get_active_offenders(self) -> List[Offender]:
        """Get active offenders."""
        return self.get_offenders_by_status(Status.ACTIVE.value)
    
    def get_violation_offenders(self) -> List[Offender]:
        """Get offenders with violations."""
        return self.get_offenders_by_status(Status.VIOLATION.value)
    
    def calculate_risk_assessment(self, offender: Offender) -> Dict[str, Any]:
        """Calculate risk assessment for offender."""
        risk_factors = []
        risk_score = 0.0
        
        # Age factor
        if offender.birth_date:
            age = (date.today() - offender.birth_date).days / 365.25
            if age < 25:
                risk_factors.append("Tuổi trẻ")
                risk_score += 0.25
            elif age > 50:
                risk_factors.append("Tuổi cao")
                risk_score -= 0.1
        
        # Employment factor
        if not offender.occupation or offender.occupation.lower() in ['thất nghiệp', 'nông dân']:
            risk_factors.append("Thất nghiệp")
            risk_score += 0.2
        
        # Time remaining factor
        if offender.days_remaining < 30:
            risk_factors.append("Sắp hết hạn")
            risk_score += 0.15
        
        # Previous violations factor
        # This would require querying violations table
        # For now, we'll use a placeholder
        
        # Normalize risk score
        risk_score = min(1.0, max(0.0, risk_score))
        
        # Determine risk level
        if risk_score < 0.3:
            risk_level = RiskLevel.LOW
        elif risk_score < 0.7:
            risk_level = RiskLevel.MEDIUM
        else:
            risk_level = RiskLevel.HIGH
        
        return {
            'risk_score': risk_score,
            'risk_level': risk_level,
            'risk_factors': risk_factors,
            'risk_percentage': risk_score * 100
        }
    
    def apply_sentence_reduction(self, offender_id: int, months: int, reason: str) -> bool:
        """Apply sentence reduction to offender."""
        offender = self.get_offender(offender_id)
        if not offender:
            return False
        
        # Check eligibility
        if not offender.is_eligible_for_reduction():
            return False
        
        # Apply reduction
        offender.reduced_months += months
        offender.reduction_count += 1
        offender.reduction_date = date.today()
        
        # Recalculate completion date
        self._calculate_offender_fields(offender)
        
        # Update in database
        return self.db_manager.update_offender(offender)
    
    def _validate_offender(self, offender: Offender):
        """Validate offender data."""
        errors = []
        
        # Required fields
        if not offender.case_number:
            errors.append("Số hồ sơ không được để trống")
        
        if not offender.full_name:
            errors.append("Họ tên không được để trống")
        
        # Date validations
        if offender.birth_date and offender.birth_date > date.today():
            errors.append("Ngày sinh không thể lớn hơn ngày hiện tại")
        
        if offender.start_date and offender.birth_date:
            if offender.start_date < offender.birth_date:
                errors.append("Ngày bắt đầu không thể trước ngày sinh")
        
        # Duration validation
        if offender.duration_months < 1 or offender.duration_months > 60:
            errors.append("Thời gian thử thách phải từ 1-60 tháng")
        
        if errors:
            raise ValueError("; ".join(errors))
    
    def _calculate_offender_fields(self, offender: Offender):
        """Calculate derived fields for offender."""
        # Calculate completion date
        if offender.start_date and offender.duration_months > 0:
            base_completion = offender.start_date + relativedelta(months=offender.duration_months)
            if offender.reduced_months > 0:
                offender.completion_date = base_completion - relativedelta(months=offender.reduced_months)
            else:
                offender.completion_date = base_completion
        
        # Calculate status
        if offender.completion_date:
            today = date.today()
            days_until = (offender.completion_date - today).days
            
            if days_until <= 0:
                offender.status = Status.COMPLETED
            elif days_until <= 30:
                offender.status = Status.EXPIRING_SOON
            else:
                offender.status = Status.ACTIVE
        
        # Calculate days remaining
        if offender.completion_date:
            today = date.today()
            days = (offender.completion_date - today).days
            offender.days_remaining = max(0, days)
        
        # Calculate risk assessment
        risk_data = self.calculate_risk_assessment(offender)
        offender.risk_level = risk_data['risk_level']
        offender.risk_percentage = risk_data['risk_percentage']
        
        # Update timestamp
        offender.updated_at = datetime.now()
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get system statistics."""
        offenders = self.get_all_offenders()
        
        stats = {
            'total_offenders': len(offenders),
            'active_offenders': len([o for o in offenders if o.status == Status.ACTIVE]),
            'completed_offenders': len([o for o in offenders if o.status == Status.COMPLETED]),
            'violation_offenders': len([o for o in offenders if o.status == Status.VIOLATION]),
            'expiring_soon': len([o for o in offenders if o.status == Status.EXPIRING_SOON]),
            'high_risk': len([o for o in offenders if o.risk_level == RiskLevel.HIGH]),
            'medium_risk': len([o for o in offenders if o.risk_level == RiskLevel.MEDIUM]),
            'low_risk': len([o for o in offenders if o.risk_level == RiskLevel.LOW])
        }
        
        return stats 

    def get_total_count(self) -> int:
        """Trả về tổng số đối tượng."""
        return len(self.get_all_offenders())

    def get_count_by_status(self, status: str) -> int:
        """Trả về số đối tượng theo trạng thái (status)."""
        return len(self.get_offenders_by_status(status)) 

    def get_count_by_risk_level(self, risk_level: str) -> int:
        """Trả về số đối tượng theo mức độ nguy cơ (risk_level)."""
        return len([o for o in self.get_all_offenders() if (o.risk_level.value if hasattr(o.risk_level, 'value') else str(o.risk_level)) == risk_level]) 
"""
Report service for generating reports and exports.
"""

from typing import List, Dict, Any, Optional
from datetime import datetime, date
import json
import csv
from pathlib import Path

from models.offender import Offender, Status, RiskLevel


class ReportService:
    """Service for generating reports and exports."""
    
    def __init__(self):
        """Initialize report service."""
        self.report_templates = {
            'monthly': self._generate_monthly_report,
            'quarterly': self._generate_quarterly_report,
            'annual': self._generate_annual_report,
            'status': self._generate_status_report,
            'risk': self._generate_risk_report
        }
    
    def generate_report(self, report_type: str, offenders: List[Offender], 
                       filters: Dict[str, Any] = None) -> Dict[str, Any]:
        """Generate report based on type."""
        if report_type not in self.report_templates:
            raise ValueError(f"Unknown report type: {report_type}")
        
        # Apply filters
        filtered_offenders = self._apply_filters(offenders, filters or {})
        
        # Generate report
        return self.report_templates[report_type](filtered_offenders)
    
    def export_to_excel(self, offenders: List[Offender], filename: str) -> bool:
        """Export offenders to Excel CSV format."""
        try:
            with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
                fieldnames = [
                    'Số hồ sơ', 'Họ tên', 'Giới tính', 'Ngày sinh', 'Địa chỉ',
                    'Nghề nghiệp', 'Tội danh', 'Loại án', 'Số bản án',
                    'Số quyết định', 'Ngày bắt đầu', 'Thời gian (tháng)',
                    'Được giảm (tháng)', 'Ngày giảm', 'Số lần giảm',
                    'Ngày hoàn thành', 'Trạng thái', 'Ngày còn lại',
                    'Mức độ nguy cơ', 'Tỷ lệ nguy cơ (%)', 'Ghi chú'
                ]
                
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
                
                for offender in offenders:
                    writer.writerow({
                        'Số hồ sơ': offender.case_number,
                        'Họ tên': offender.full_name,
                        'Giới tính': offender.gender.value if hasattr(offender.gender, 'value') else str(offender.gender),
                        'Ngày sinh': offender.birth_date.isoformat() if offender.birth_date else '',
                        'Địa chỉ': offender.address,
                        'Nghề nghiệp': offender.occupation,
                        'Tội danh': offender.crime,
                        'Loại án': offender.case_type.value if hasattr(offender.case_type, 'value') else str(offender.case_type),
                        'Số bản án': offender.sentence_number,
                        'Số quyết định': offender.decision_number,
                        'Ngày bắt đầu': offender.start_date.isoformat() if offender.start_date else '',
                        'Thời gian (tháng)': offender.duration_months,
                        'Được giảm (tháng)': offender.reduced_months,
                        'Ngày giảm': offender.reduction_date.isoformat() if offender.reduction_date else '',
                        'Số lần giảm': offender.reduction_count,
                        'Ngày hoàn thành': offender.completion_date.isoformat() if offender.completion_date else '',
                        'Trạng thái': offender.status.value if hasattr(offender.status, 'value') else str(offender.status),
                        'Ngày còn lại': offender.days_remaining,
                        'Mức độ nguy cơ': offender.risk_level.value if hasattr(offender.risk_level, 'value') else str(offender.risk_level),
                        'Tỷ lệ nguy cơ (%)': f"{offender.risk_percentage:.1f}",
                        'Ghi chú': offender.notes
                    })
            
            return True
        except Exception as e:
            print(f"Error exporting to Excel: {e}")
            return False
    
    def export_to_json(self, offenders: List[Offender], filename: str) -> bool:
        """Export offenders to JSON format."""
        try:
            data = []
            for offender in offenders:
                data.append(offender.to_dict())
            
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            
            return True
        except Exception as e:
            print(f"Error exporting to JSON: {e}")
            return False
    
    def _apply_filters(self, offenders: List[Offender], filters: Dict[str, Any]) -> List[Offender]:
        """Apply filters to offenders list."""
        filtered = offenders
        
        # Status filter
        if 'status' in filters and filters['status']:
            filtered = [o for o in filtered if (o.status.value if hasattr(o.status, 'value') else str(o.status)) == filters['status']]
        
        # Risk level filter
        if 'risk_level' in filters and filters['risk_level']:
            filtered = [o for o in filtered if (o.risk_level.value if hasattr(o.risk_level, 'value') else str(o.risk_level)) == filters['risk_level']]
        
        # Date range filter
        if 'start_date' in filters and filters['start_date']:
            filtered = [o for o in filtered if o.start_date and o.start_date >= filters['start_date']]
        
        if 'end_date' in filters and filters['end_date']:
            filtered = [o for o in filtered if o.start_date and o.start_date <= filters['end_date']]
        
        # Search term filter
        if 'search' in filters and filters['search']:
            search_term = filters['search'].lower()
            filtered = [o for o in filtered if 
                       search_term in o.full_name.lower() or 
                       search_term in o.case_number.lower()]
        
        return filtered
    
    def _generate_monthly_report(self, offenders: List[Offender]) -> Dict[str, Any]:
        """Generate monthly report."""
        current_month = datetime.now().month
        current_year = datetime.now().year
        
        monthly_offenders = [o for o in offenders 
                           if o.created_at and o.created_at.month == current_month 
                           and o.created_at.year == current_year]
        
        return {
            'report_type': 'monthly',
            'period': f"{current_month}/{current_year}",
            'total_offenders': len(offenders),
            'new_offenders': len(monthly_offenders),
            'completed_offenders': len([o for o in offenders if o.status == Status.COMPLETED]),
            'active_offenders': len([o for o in offenders if o.status == Status.ACTIVE]),
            'violation_offenders': len([o for o in offenders if o.status == Status.VIOLATION]),
            'expiring_soon': len([o for o in offenders if o.status == Status.EXPIRING_SOON]),
            'high_risk': len([o for o in offenders if o.risk_level == RiskLevel.HIGH]),
            'completion_rate': self._calculate_completion_rate(offenders),
            'violation_rate': self._calculate_violation_rate(offenders)
        }
    
    def _generate_quarterly_report(self, offenders: List[Offender]) -> Dict[str, Any]:
        """Generate quarterly report."""
        current_quarter = (datetime.now().month - 1) // 3 + 1
        current_year = datetime.now().year
        
        quarterly_offenders = [o for o in offenders 
                             if o.created_at and 
                             ((o.created_at.month - 1) // 3 + 1) == current_quarter 
                             and o.created_at.year == current_year]
        
        return {
            'report_type': 'quarterly',
            'period': f"Q{current_quarter}/{current_year}",
            'total_offenders': len(offenders),
            'new_offenders': len(quarterly_offenders),
            'completed_offenders': len([o for o in offenders if o.status == Status.COMPLETED]),
            'active_offenders': len([o for o in offenders if o.status == Status.ACTIVE]),
            'violation_offenders': len([o for o in offenders if o.status == Status.VIOLATION]),
            'expiring_soon': len([o for o in offenders if o.status == Status.EXPIRING_SOON]),
            'high_risk': len([o for o in offenders if o.risk_level == RiskLevel.HIGH]),
            'completion_rate': self._calculate_completion_rate(offenders),
            'violation_rate': self._calculate_violation_rate(offenders)
        }
    
    def _generate_annual_report(self, offenders: List[Offender]) -> Dict[str, Any]:
        """Generate annual report."""
        current_year = datetime.now().year
        
        annual_offenders = [o for o in offenders 
                          if o.created_at and o.created_at.year == current_year]
        
        return {
            'report_type': 'annual',
            'period': str(current_year),
            'total_offenders': len(offenders),
            'new_offenders': len(annual_offenders),
            'completed_offenders': len([o for o in offenders if o.status == Status.COMPLETED]),
            'active_offenders': len([o for o in offenders if o.status == Status.ACTIVE]),
            'violation_offenders': len([o for o in offenders if o.status == Status.VIOLATION]),
            'expiring_soon': len([o for o in offenders if o.status == Status.EXPIRING_SOON]),
            'high_risk': len([o for o in offenders if o.risk_level == RiskLevel.HIGH]),
            'completion_rate': self._calculate_completion_rate(offenders),
            'violation_rate': self._calculate_violation_rate(offenders)
        }
    
    def _generate_status_report(self, offenders: List[Offender]) -> Dict[str, Any]:
        """Generate status report."""
        return {
            'report_type': 'status',
            'total_offenders': len(offenders),
            'status_distribution': {
                'active': len([o for o in offenders if o.status == Status.ACTIVE]),
                'completed': len([o for o in offenders if o.status == Status.COMPLETED]),
                'violation': len([o for o in offenders if o.status == Status.VIOLATION]),
                'expiring_soon': len([o for o in offenders if o.status == Status.EXPIRING_SOON])
            },
            'risk_distribution': {
                'high': len([o for o in offenders if o.risk_level == RiskLevel.HIGH]),
                'medium': len([o for o in offenders if o.risk_level == RiskLevel.MEDIUM]),
                'low': len([o for o in offenders if o.risk_level == RiskLevel.LOW])
            }
        }
    
    def _generate_risk_report(self, offenders: List[Offender]) -> Dict[str, Any]:
        """Generate risk assessment report."""
        high_risk = [o for o in offenders if o.risk_level == RiskLevel.HIGH]
        medium_risk = [o for o in offenders if o.risk_level == RiskLevel.MEDIUM]
        low_risk = [o for o in offenders if o.risk_level == RiskLevel.LOW]
        
        return {
            'report_type': 'risk',
            'total_offenders': len(offenders),
            'high_risk_count': len(high_risk),
            'medium_risk_count': len(medium_risk),
            'low_risk_count': len(low_risk),
            'high_risk_percentage': (len(high_risk) / len(offenders) * 100) if offenders else 0,
            'medium_risk_percentage': (len(medium_risk) / len(offenders) * 100) if offenders else 0,
            'low_risk_percentage': (len(low_risk) / len(offenders) * 100) if offenders else 0,
            'high_risk_offenders': [o.case_number for o in high_risk],
            'medium_risk_offenders': [o.case_number for o in medium_risk],
            'low_risk_offenders': [o.case_number for o in low_risk]
        }
    
    def _calculate_completion_rate(self, offenders: List[Offender]) -> float:
        """Calculate completion rate."""
        if not offenders:
            return 0.0
        completed = len([o for o in offenders if o.status == Status.COMPLETED])
        return (completed / len(offenders)) * 100
    
    def _calculate_violation_rate(self, offenders: List[Offender]) -> float:
        """Calculate violation rate."""
        if not offenders:
            return 0.0
        violations = len([o for o in offenders if o.status == Status.VIOLATION])
        return (violations / len(offenders)) * 100 
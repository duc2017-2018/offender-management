"""
AI service for risk prediction and analysis.
"""

from typing import Dict, Any, List, Optional
from datetime import datetime, date
import random

from models.offender import Offender, RiskLevel


class AIService:
    """Service for AI-powered features."""
    
    def __init__(self):
        """Initialize AI service."""
        self.risk_factors = {
            'age_young': 0.25,
            'age_old': -0.1,
            'unemployed': 0.2,
            'expiring_soon': 0.15,
            'previous_violations': 0.3,
            'rural_area': 0.1,
            'urban_area': -0.05,
            'family_support': -0.2,
            'education_low': 0.15,
            'education_high': -0.1
        }
    
    def predict_risk(self, offender: Offender) -> Dict[str, Any]:
        """Predict risk level for offender."""
        risk_score = 0.0
        factors = []
        
        # Age factor
        if offender.birth_date:
            age = (date.today() - offender.birth_date).days / 365.25
            if age < 25:
                risk_score += self.risk_factors['age_young']
                factors.append("Tuổi trẻ")
            elif age > 50:
                risk_score += self.risk_factors['age_old']
                factors.append("Tuổi cao")
        
        # Employment factor
        if not offender.occupation or offender.occupation.lower() in ['thất nghiệp', 'nông dân']:
            risk_score += self.risk_factors['unemployed']
            factors.append("Thất nghiệp")
        
        # Time remaining factor
        if offender.days_remaining < 30:
            risk_score += self.risk_factors['expiring_soon']
            factors.append("Sắp hết hạn")
        
        # Location factor (simplified)
        if offender.address:
            if 'thành phố' in offender.address.lower():
                risk_score += self.risk_factors['urban_area']
            else:
                risk_score += self.risk_factors['rural_area']
        
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
            'risk_percentage': risk_score * 100,
            'risk_factors': factors,
            'recommendations': self._get_recommendations(risk_level, factors)
        }
    
    def analyze_trends(self, offenders: List[Offender]) -> Dict[str, Any]:
        """Analyze trends in offender data."""
        if not offenders:
            return {}
        
        # Calculate statistics
        total = len(offenders)
        active = len([
            o for o in offenders
            if (o.status.value if hasattr(o.status, 'value') else str(o.status)) == "Đang chấp hành"
        ])
        completed = len([
            o for o in offenders
            if (o.status.value if hasattr(o.status, 'value') else str(o.status)) == "Đã hoàn thành"
        ])
        violations = len([
            o for o in offenders
            if (o.status.value if hasattr(o.status, 'value') else str(o.status)) == "Vi phạm"
        ])
        
        # Risk distribution
        high_risk = len([o for o in offenders if o.risk_level == RiskLevel.HIGH])
        medium_risk = len([o for o in offenders if o.risk_level == RiskLevel.MEDIUM])
        low_risk = len([o for o in offenders if o.risk_level == RiskLevel.LOW])
        
        # Age distribution
        age_groups = {'18-25': 0, '26-35': 0, '36-50': 0, '50+': 0}
        for offender in offenders:
            if offender.birth_date:
                age = (date.today() - offender.birth_date).days / 365.25
                if age <= 25:
                    age_groups['18-25'] += 1
                elif age <= 35:
                    age_groups['26-35'] += 1
                elif age <= 50:
                    age_groups['36-50'] += 1
                else:
                    age_groups['50+'] += 1
        
        return {
            'total_offenders': total,
            'status_distribution': {
                'active': active,
                'completed': completed,
                'violations': violations
            },
            'risk_distribution': {
                'high': high_risk,
                'medium': medium_risk,
                'low': low_risk
            },
            'age_distribution': age_groups,
            'completion_rate': (completed / total * 100) if total > 0 else 0,
            'violation_rate': (violations / total * 100) if total > 0 else 0
        }
    
    def generate_insights(self, offenders: List[Offender]) -> List[str]:
        """Generate insights from offender data."""
        insights = []
        
        if not offenders:
            return ["Không có dữ liệu để phân tích"]
        
        # Expiring soon
        expiring = [o for o in offenders if o.days_remaining <= 30 and o.days_remaining > 0]
        if expiring:
            insights.append(f"{len(expiring)} đối tượng sắp hết hạn trong 30 ngày tới")
        
        # High risk offenders
        high_risk = [o for o in offenders if o.risk_level == RiskLevel.HIGH]
        if high_risk:
            insights.append(f"{len(high_risk)} đối tượng có nguy cơ cao cần giám sát đặc biệt")
        
        # Completion rate
        completed = [o for o in offenders if o.status.value == "Đã hoàn thành"]
        completion_rate = len(completed) / len(offenders) * 100
        insights.append(f"Tỷ lệ hoàn thành: {completion_rate:.1f}%")
        
        # Violation rate
        violations = [o for o in offenders if o.status.value == "Vi phạm"]
        violation_rate = len(violations) / len(offenders) * 100
        insights.append(f"Tỷ lệ vi phạm: {violation_rate:.1f}%")
        
        return insights
    
    def chatbot_response(self, question: str) -> str:
        """Generate chatbot response."""
        responses = {
            'điều kiện giảm án': """
            Điều kiện giảm án theo Điều 35 Bộ luật Hình sự:
            - Đã chấp hành ít nhất 1/3 thời gian thử thách
            - Có nhiều tiến bộ trong cải tạo
            - Không vi phạm kỷ luật
            - Có nơi cư trú ổn định
            """,
            'thời gian thử thách': """
            Thời gian thử thách được tính từ ngày bản án có hiệu lực:
            - Án treo: 1-5 năm
            - Cải tạo không giam giữ: 6 tháng - 3 năm
            - Công ích: 1-5 năm
            """,
            'vi phạm': """
            Các vi phạm có thể dẫn đến:
            - Cảnh cáo
            - Kéo dài thời gian thử thách
            - Chuyển sang hình phạt tù
            """,
            'quyền lợi': """
            Đối tượng có quyền:
            - Được giảm án khi đủ điều kiện
            - Được hỗ trợ tìm việc làm
            - Được tham gia các chương trình cải tạo
            """
        }
        
        question_lower = question.lower()
        for key, response in responses.items():
            if key in question_lower:
                return response.strip()
        
        return "Tôi không hiểu câu hỏi của bạn. Vui lòng hỏi về điều kiện giảm án, thời gian thử thách, vi phạm hoặc quyền lợi."
    
    def _get_recommendations(self, risk_level: RiskLevel, factors: List[str]) -> List[str]:
        """Get recommendations based on risk level and factors."""
        recommendations = []
        
        if risk_level == RiskLevel.HIGH:
            recommendations.extend([
                "Tăng cường giám sát",
                "Báo cáo định kỳ hàng tuần",
                "Kiểm tra nơi cư trú thường xuyên"
            ])
        elif risk_level == RiskLevel.MEDIUM:
            recommendations.extend([
                "Giám sát định kỳ",
                "Báo cáo hàng tháng",
                "Hỗ trợ tìm việc làm"
            ])
        else:
            recommendations.extend([
                "Giám sát thông thường",
                "Báo cáo hàng quý",
                "Khuyến khích tham gia cải tạo"
            ])
        
        # Add specific recommendations based on factors
        if "Thất nghiệp" in factors:
            recommendations.append("Hỗ trợ tìm việc làm")
        if "Tuổi trẻ" in factors:
            recommendations.append("Hướng dẫn kỹ năng sống")
        if "Sắp hết hạn" in factors:
            recommendations.append("Chuẩn bị hồ sơ hoàn thành")
        
        return recommendations 
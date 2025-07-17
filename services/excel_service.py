"""
Excel service for importing/exporting data with automatic calculations.
"""

import pandas as pd
from typing import List, Dict, Any
from datetime import datetime
from models.offender import Offender, Gender, CaseType
from services.offender_service import OffenderService


class ExcelService:
    """Service for Excel import/export with automatic calculations."""
    
    def __init__(self, offender_service: OffenderService):
        """Initialize Excel service."""
        self.offender_service = offender_service
        
    def import_from_excel(self, file_path: str) -> Dict[str, Any]:
        """Import offenders from Excel file with automatic calculations."""
        try:
            # Read Excel file
            df = pd.read_excel(file_path, sheet_name=0)
            
            imported_count = 0
            errors = []
            
            for index, row in df.iterrows():
                try:
                    # Convert row to offender data
                    offender_data = self._convert_row_to_offender_data(row)
                    
                    # Create offender object (will trigger automatic calculations)
                    offender = Offender.from_dict(offender_data)
                    
                    # Save to database
                    offender_id = self.offender_service.db_manager.create_offender(offender)
                    offender.id = offender_id
                    
                    imported_count += 1
                    
                except Exception as e:
                    errors.append(f"Dòng {index + 2}: {str(e)}")
            
            return {
                'success': True,
                'imported_count': imported_count,
                'errors': errors,
                'total_rows': len(df)
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': f"Lỗi đọc file Excel: {str(e)}",
                'imported_count': 0,
                'errors': []
            }
    
    def export_to_excel(self, offenders: List[Offender], file_path: str) -> bool:
        """Export offenders to Excel with calculated fields."""
        try:
            # Convert offenders to DataFrame
            data = []
            for offender in offenders:
                data.append({
                    'Số hồ sơ': offender.case_number,
                    'Họ tên': offender.full_name,
                    'Giới tính': offender.gender.value if hasattr(offender.gender, 'value') else str(offender.gender),
                    'Ngày sinh': offender.birth_date.strftime('%d/%m/%Y') if offender.birth_date else '',
                    'Địa chỉ': offender.address,
                    'Nghề nghiệp': offender.occupation,
                    'Tội danh': offender.crime,
                    'Loại án': offender.case_type.value if hasattr(offender.case_type, 'value') else str(offender.case_type),
                    'Số bản án': offender.sentence_number,
                    'Số quyết định': offender.decision_number,
                    'Ngày bắt đầu': offender.start_date.strftime('%d/%m/%Y') if offender.start_date else '',
                    'Thời gian (tháng)': offender.duration_months,
                    'Được giảm (tháng)': offender.reduced_months,
                    'Ngày được giảm': offender.reduction_date.strftime('%d/%m/%Y') if offender.reduction_date else '',
                    'Số lần giảm': offender.reduction_count,
                    'Ngày chấp hành xong': offender.completion_date.strftime('%d/%m/%Y') if offender.completion_date else '',
                    'Trạng thái': offender.status.value if hasattr(offender.status, 'value') else str(offender.status),
                    'Số ngày còn lại': offender.days_remaining,
                    'Mức độ nguy cơ': offender.risk_level.value if hasattr(offender.risk_level, 'value') else str(offender.risk_level),
                    'Tỷ lệ nguy cơ (%)': f"{offender.risk_percentage:.1f}",
                    'Ghi chú': offender.notes
                })
            
            # Create DataFrame
            df = pd.DataFrame(data)
            
            # Export to Excel
            with pd.ExcelWriter(file_path, engine='openpyxl') as writer:
                df.to_excel(writer, sheet_name='Đối tượng thi hành án', index=False)
                
                # Auto-adjust column widths
                worksheet = writer.sheets['Đối tượng thi hành án']
                for column in worksheet.columns:
                    max_length = 0
                    column_letter = column[0].column_letter
                    for cell in column:
                        try:
                            if len(str(cell.value)) > max_length:
                                max_length = len(str(cell.value))
                        except:
                            pass
                    adjusted_width = min(max_length + 2, 50)
                    worksheet.column_dimensions[column_letter].width = adjusted_width
            
            return True
            
        except Exception as e:
            print(f"Lỗi xuất Excel: {e}")
            return False
    
    def _convert_row_to_offender_data(self, row: pd.Series) -> Dict[str, Any]:
        """Convert Excel row to offender data."""
        # Map Excel columns to offender fields
        data = {}
        
        # Basic information
        data['case_number'] = str(row.get('Số hồ sơ', '')).strip()
        data['full_name'] = str(row.get('Họ tên', '')).strip()
        
        # Gender
        gender_str = str(row.get('Giới tính', '')).strip()
        data['gender'] = Gender.FEMALE if 'nữ' in gender_str.lower() else Gender.MALE
        
        # Birth date
        birth_date = row.get('Ngày sinh')
        if pd.notna(birth_date):
            if isinstance(birth_date, str):
                try:
                    data['birth_date'] = datetime.strptime(birth_date, '%d/%m/%Y').date()
                except:
                    data['birth_date'] = None
            else:
                data['birth_date'] = birth_date.date() if hasattr(birth_date, 'date') else None
        else:
            data['birth_date'] = None
        
        data['address'] = str(row.get('Địa chỉ', '')).strip()
        data['occupation'] = str(row.get('Nghề nghiệp', '')).strip()
        data['crime'] = str(row.get('Tội danh', '')).strip()
        
        # Case type
        case_type_str = str(row.get('Loại án', '')).strip()
        if 'cải tạo' in case_type_str.lower():
            data['case_type'] = CaseType.PROBATION
        elif 'công ích' in case_type_str.lower():
            data['case_type'] = CaseType.COMMUNITY_SERVICE
        else:
            data['case_type'] = CaseType.SUSPENDED_SENTENCE
        
        # Case information
        data['sentence_number'] = str(row.get('Số bản án', '')).strip()
        data['decision_number'] = str(row.get('Số quyết định', '')).strip()
        
        # Start date
        start_date = row.get('Ngày bắt đầu')
        if pd.notna(start_date):
            if isinstance(start_date, str):
                try:
                    data['start_date'] = datetime.strptime(start_date, '%d/%m/%Y').date()
                except:
                    data['start_date'] = None
            else:
                data['start_date'] = start_date.date() if hasattr(start_date, 'date') else None
        else:
            data['start_date'] = None
        
        # Duration and reduction
        data['duration_months'] = int(row.get('Thời gian (tháng)', 0))
        data['reduced_months'] = int(row.get('Được giảm (tháng)', 0))
        
        # Reduction date
        reduction_date = row.get('Ngày được giảm')
        if pd.notna(reduction_date):
            if isinstance(reduction_date, str):
                try:
                    data['reduction_date'] = datetime.strptime(reduction_date, '%d/%m/%Y').date()
                except:
                    data['reduction_date'] = None
            else:
                data['reduction_date'] = reduction_date.date() if hasattr(reduction_date, 'date') else None
        else:
            data['reduction_date'] = None
        
        data['reduction_count'] = int(row.get('Số lần giảm', 0))
        data['notes'] = str(row.get('Ghi chú', '')).strip()
        
        return data
    
    def create_excel_template(self, file_path: str) -> bool:
        """Create Excel template for data import."""
        try:
            # Create sample data
            sample_data = [
                {
                    'Số hồ sơ': '40CE0625/405LF',
                    'Họ tên': 'Nguyễn Văn A',
                    'Giới tính': 'Nam',
                    'Ngày sinh': '15/05/1990',
                    'Địa chỉ': 'TDP 1, P. Bắc Hồng, TX. Hồng Lĩnh, Hà Tĩnh',
                    'Nghề nghiệp': 'Nông dân',
                    'Tội danh': 'Trộm cắp tài sản',
                    'Loại án': 'Án treo',
                    'Số bản án': 'Số 15/2025/HS-ST, ngày 15/5/2025',
                    'Số quyết định': 'Số 15/2025/QĐ-CA, ngày 29/5/2025',
                    'Ngày bắt đầu': '01/06/2025',
                    'Thời gian (tháng)': 6,
                    'Được giảm (tháng)': 1,
                    'Ngày được giảm': '02/09/2025',
                    'Số lần giảm': 1,
                    'Ghi chú': 'Đối tượng có tiến bộ tốt'
                }
            ]
            
            df = pd.DataFrame(sample_data)
            
            # Export template
            with pd.ExcelWriter(file_path, engine='openpyxl') as writer:
                df.to_excel(writer, sheet_name='Mẫu nhập liệu', index=False)
                
                # Add instructions sheet
                instructions = pd.DataFrame({
                    'Hướng dẫn': [
                        '1. Điền thông tin theo mẫu trên',
                        '2. Ngày tháng định dạng: dd/mm/yyyy',
                        '3. Giới tính: Nam hoặc Nữ',
                        '4. Loại án: Án treo, Cải tạo, Công ích',
                        '5. Thời gian tính bằng tháng',
                        '6. Các trường có dấu * là bắt buộc',
                        '7. Sau khi nhập, hệ thống sẽ tự động tính:',
                        '   - Ngày chấp hành xong',
                        '   - Trạng thái thi hành án',
                        '   - Số ngày còn lại',
                        '   - Mức độ nguy cơ'
                    ]
                })
                instructions.to_excel(writer, sheet_name='Hướng dẫn', index=False)
            
            return True
            
        except Exception as e:
            print(f"Lỗi tạo template: {e}")
            return False 
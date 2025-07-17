"""
Document service for generating documents from templates.
"""

from typing import Dict, Any, Optional
from datetime import datetime, date
from pathlib import Path

from docxtpl import DocxTemplate
from models.offender import Offender, Gender, CaseType
from docx2pdf import convert


class DocumentService:
    """Service for generating documents from templates."""
    
    def __init__(self):
        """Initialize document service."""
        self.templates_dir = Path("assets/templates")
        
    def generate_confirmation_letter(self, offender: Offender, template_name: str = "CD44A_template.docx") -> Optional[str]:
        """Generate confirmation letter from template."""
        try:
            template_path = self.templates_dir / template_name
            if not template_path.exists():
                raise FileNotFoundError(f"Template không tồn tại: {template_path}")
            
            # Load template
            doc = DocxTemplate(str(template_path))
            
            # Prepare context data
            context = self._prepare_context(offender)
            
            # Render template
            doc.render(context)
            
            # Generate output filename
            output_filename = f"Giay_xac_nhan_{offender.case_number}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.docx"
            output_path = Path("data/exports") / output_filename
            output_path.parent.mkdir(parents=True, exist_ok=True)
            
            # Save document
            doc.save(str(output_path))
            
            return str(output_path)
            
        except Exception as e:
            print(f"Lỗi tạo giấy xác nhận: {e}")
            return None
    
    def generate_batch_confirmation_letters(self, offenders: list, template_name: str = "CD44A_template.docx") -> Dict[str, Any]:
        """Generate confirmation letters for multiple offenders."""
        results = {
            'success_count': 0,
            'error_count': 0,
            'errors': [],
            'generated_files': []
        }
        
        for offender in offenders:
            try:
                file_path = self.generate_confirmation_letter(offender, template_name)
                if file_path:
                    results['success_count'] += 1
                    results['generated_files'].append(file_path)
                else:
                    results['error_count'] += 1
                    results['errors'].append(f"Không thể tạo giấy xác nhận cho {offender.full_name}")
            except Exception as e:
                results['error_count'] += 1
                results['errors'].append(f"Lỗi tạo giấy xác nhận cho {offender.full_name}: {str(e)}")
        
        return results
    
    def _prepare_context(self, offender: Offender) -> Dict[str, Any]:
        """Prepare context data for template rendering."""
        context = {
            # Basic information
            'ten_ho_so': offender.case_number,
            'ten_doi_tuong': offender.full_name,
            'gioi_tinh': offender.gender.value if hasattr(offender.gender, 'value') else str(offender.gender),
            'ten_khac': '',  # Placeholder
            'ngay_sinh': offender.birth_date.strftime('%d/%m/%Y') if offender.birth_date else '',
            'noi_dktt': offender.address,
            'noi_o_hien_nay': offender.address,
            'toi_danh': offender.crime,
            
            # Case information
            'hinh_phat': offender.case_type.value if hasattr(offender.case_type, 'value') else str(offender.case_type),
            'thoi_han': f"{offender.duration_months} tháng",
            'thoi_han_chap_hanh': f"{offender.duration_months} tháng",
            'ngay_chap_hanh': offender.start_date.strftime('%d/%m/%Y') if offender.start_date else '',
            'ban_an_so': offender.sentence_number,
            'ngay_ban_an': offender.start_date.strftime('%d/%m/%Y') if offender.start_date else '',
            'toa_an': 'TAND huyện Thạch Hà, tỉnh Hà Tĩnh',
            'qd_thi_hanh_so': offender.decision_number,
            'ngay_qd_thi_hanh': offender.start_date.strftime('%d/%m/%Y') if offender.start_date else '',
            'toa_an_qd': 'TAND huyện Thạch Hà, tỉnh Hà Tĩnh',
            'noi_dung_chap_hanh': f"Chấp hành án {offender.case_type.value if hasattr(offender.case_type, 'value') else str(offender.case_type)}",
            'so_ho_so': offender.case_number,
            'ngay_lap_ho_so': datetime.now().strftime('%d/%m/%Y'),
            'so_to': '15',  # Placeholder
            
            # Completion information
            'ngay_hoan_thanh': offender.completion_date.strftime('%d/%m/%Y') if offender.completion_date else '',
            'trang_thai': offender.status.value if hasattr(offender.status, 'value') else str(offender.status),
            'so_ngay_con_lai': offender.days_remaining,
            
            # Reduction information
            'duoc_giam_thoi_gian': f"{offender.reduced_months} tháng" if offender.reduced_months > 0 else "Không",
            'ngay_duoc_giam': offender.reduction_date.strftime('%d/%m/%Y') if offender.reduction_date else '',
            'so_lan_giam': offender.reduction_count,
            
            # Officer information (placeholders)
            'can_bo_giao': 'Nguyễn Văn A',
            'chuc_vu_giao': 'Cán bộ quản lý',
            'don_vi_giao': 'Phòng Thi hành án dân sự',
            'can_bo_nhan': 'Trần Thị B',
            'chuc_vu_nhan': 'Cán bộ tiếp nhận',
            'don_vi_nhan': 'Phòng Thi hành án dân sự',
            
            # Document metadata
            'can_cu_khoan': 'Khoản 1 Điều 1 Nghị định số 62/2015/NĐ-CP',
            'thoi_gian_giao': datetime.now().strftime('%H:%M ngày %d/%m/%Y'),
            'dia_diem_giao': 'Phòng Thi hành án dân sự, TAND huyện Thạch Hà',
            'gio_ket_thuc': datetime.now().strftime('%H:%M'),
            
            # Current date
            'ngay_hien_tai': datetime.now().strftime('%d/%m/%Y'),
            'thang_hien_tai': datetime.now().strftime('%m/%Y'),
            'nam_hien_tai': str(datetime.now().year)
        }
        
        return context
    
    def get_available_templates(self) -> list:
        """Get list of available templates."""
        templates = []
        if self.templates_dir.exists():
            for template_file in self.templates_dir.glob("*.docx"):
                templates.append({
                    'name': template_file.name,
                    'path': str(template_file),
                    'size': template_file.stat().st_size
                })
        return templates
    
    def create_template_preview(self, template_name: str) -> Optional[Dict[str, Any]]:
        """Create preview of template with sample data."""
        try:
            # Create sample offender for preview
            sample_offender = Offender(
                case_number="40CE0625/405LF",
                full_name="Nguyễn Văn A",
                gender=Gender.MALE,
                birth_date=date(1990, 5, 15),
                address="TDP 1, P. Bắc Hồng, TX. Hồng Lĩnh, Hà Tĩnh",
                occupation="Nông dân",
                crime="Trộm cắp tài sản",
                case_type=CaseType.SUSPENDED_SENTENCE,
                sentence_number="Số 15/2025/HS-ST, ngày 15/5/2025",
                decision_number="Số 15/2025/QĐ-CA, ngày 29/5/2025",
                start_date=date(2025, 6, 1),
                duration_months=6,
                reduced_months=1,
                reduction_date=date(2025, 9, 2),
                reduction_count=1
            )
            
            # Generate preview
            preview_path = self.generate_confirmation_letter(sample_offender, template_name)
            
            if preview_path:
                return {
                    'template_name': template_name,
                    'preview_path': preview_path,
                    'sample_data': self._prepare_context(sample_offender)
                }
            
            return None
            
        except Exception as e:
            print(f"Lỗi tạo preview: {e}")
            return None 

    @staticmethod
    def export_to_word(template_path: str, context: dict, output_path: str):
        """
        Đổ dữ liệu vào template Word (docx) sử dụng docxtpl.
        Nếu trường nào chưa có dữ liệu, giữ nguyên {{field_name}} để người dùng bổ sung thủ công.
        """
        doc = DocxTemplate(template_path)
        # Nếu context thiếu trường, giữ nguyên placeholder
        class SafeDict(dict):
            def __missing__(self, key):
                return '{{' + key + '}}'
        doc.render(SafeDict(context))
        doc.save(output_path)

    @staticmethod
    def export_to_pdf(word_path: str, pdf_path: str) -> bool:
        """
        Chuyển file Word đã đổ dữ liệu sang PDF bằng docx2pdf.
        Trả về True nếu thành công, False nếu lỗi.
        """
        try:
            convert(word_path, pdf_path)
            return True
        except Exception as e:
            print(f"Lỗi chuyển Word sang PDF: {e}")
            return False

# Ví dụ sử dụng:
# DocumentService.export_to_word(
#     'assets/templates/CD44A_template.docx',
#     {'ho_ten': 'Nguyễn Văn A', 'so_ho_so': '40CE0625/405LF'},
#     'output.docx'
# )
# DocumentService.export_to_pdf('output.docx', 'output.pdf') 
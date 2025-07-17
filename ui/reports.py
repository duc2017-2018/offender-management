#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Reports widget for generating and viewing reports.
"""

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QGridLayout, QLabel, 
    QComboBox, QPushButton, QTextEdit, QGroupBox, QFrame, 
    QDateEdit, QFileDialog, QMessageBox, QSizePolicy
)
from PyQt6.QtCore import Qt, QDate
from PyQt6.QtGui import QFont, QPixmap

from typing import Dict, Any

from services.offender_service import OffenderService
from services.report_service import ReportService


class ReportsWidget(QWidget):
    """Widget for generating and viewing reports."""
    
    def __init__(self, offender_service: OffenderService, 
                 report_service: ReportService, parent=None):
        """Initialize reports widget."""
        super().__init__(parent)
        self.offender_service = offender_service
        self.report_service = report_service
        self.setup_ui()
        self.setup_connections()
        
    def setup_ui(self):
        """Setup user interface."""
        # Main layout
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(12, 12, 12, 12)
        main_layout.setSpacing(10)
        
        # Header section
        self.setup_header(main_layout)
        
        # Report configuration
        self.setup_report_config(main_layout)
        
        # Report preview
        self.setup_report_preview(main_layout)
        
        # Export buttons
        self.setup_export_buttons(main_layout)
        main_layout.addStretch()  # Đảm bảo co giãn full chiều dọc
        
    def setup_header(self, parent_layout):
        """Setup header section."""
        header_frame = QFrame()
        header_frame.setObjectName("reportsHeader")
        
        header_layout = QHBoxLayout(header_frame)
        header_layout.setContentsMargins(12, 6, 12, 6)
        header_layout.setSpacing(8)
        
        # Icon and title
        icon_label = QLabel()
        icon_pixmap = QPixmap("assets/logo_cand.png")
        if not icon_pixmap.isNull():
            icon_pixmap = icon_pixmap.scaled(
                24, 24, 
                Qt.AspectRatioMode.KeepAspectRatio, 
                Qt.TransformationMode.SmoothTransformation
            )
            icon_label.setPixmap(icon_pixmap)
        else:
            icon_label.setText("📈")
            icon_label.setFont(QFont("Segoe UI", 16))
        
        title_label = QLabel("BÁO CÁO & THỐNG KÊ")
        title_label.setObjectName("reportTitle")
        title_label.setFont(QFont("Segoe UI", 13, QFont.Weight.Bold))
        
        # Stats
        stats_label = QLabel("Tổng báo cáo: 0 | Đã xuất: 0")
        stats_label.setObjectName("reportStats")
        stats_label.setFont(QFont("Segoe UI", 10))
        
        header_layout.addWidget(icon_label)
        header_layout.addWidget(title_label)
        header_layout.addStretch()
        header_layout.addWidget(stats_label)
        
        parent_layout.addWidget(header_frame)
        
    def setup_report_config(self, parent_layout):
        """Setup report configuration section."""
        config_group = QGroupBox("Cấu hình báo cáo")
        config_group.setFont(QFont("Segoe UI", 11, QFont.Weight.Bold))
        config_layout = QGridLayout(config_group)
        config_layout.setContentsMargins(12, 12, 12, 12)
        config_layout.setSpacing(10)
        
        # Report type
        config_layout.addWidget(QLabel("Loại báo cáo:"), 0, 0)
        self.report_type_combo = QComboBox()
        self.report_type_combo.addItems([
            "Báo cáo tháng", "Báo cáo quý", "Báo cáo năm", 
            "Báo cáo trạng thái", "Báo cáo nguy cơ"
        ])
        self.report_type_combo.setObjectName("reportTypeCombo")
        self.report_type_combo.setMinimumHeight(32)
        self.report_type_combo.setMaximumHeight(40)
        self.report_type_combo.setSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed
        )
        config_layout.addWidget(self.report_type_combo, 0, 1)
        
        # Date range
        config_layout.addWidget(QLabel("Từ ngày:"), 1, 0)
        self.start_date_edit = QDateEdit()
        self.start_date_edit.setCalendarPopup(True)
        self.start_date_edit.setDate(QDate.currentDate().addMonths(-1))
        self.start_date_edit.setObjectName("startDateEdit")
        self.start_date_edit.setMinimumHeight(32)
        self.start_date_edit.setMaximumHeight(40)
        self.start_date_edit.setSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed
        )
        config_layout.addWidget(self.start_date_edit, 1, 1)
        
        config_layout.addWidget(QLabel("Đến ngày:"), 1, 2)
        self.end_date_edit = QDateEdit()
        self.end_date_edit.setCalendarPopup(True)
        self.end_date_edit.setDate(QDate.currentDate())
        self.end_date_edit.setObjectName("endDateEdit")
        self.end_date_edit.setMinimumHeight(32)
        self.end_date_edit.setMaximumHeight(40)
        self.end_date_edit.setSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed
        )
        config_layout.addWidget(self.end_date_edit, 1, 3)
        
        # Filters
        config_layout.addWidget(QLabel("Địa bàn:"), 2, 0)
        self.location_filter_combo = QComboBox()
        self.location_filter_combo.addItems([
            "Tất cả", "Phường A", "Phường B", "Phường C"
        ])
        self.location_filter_combo.setObjectName("locationFilterCombo")
        self.location_filter_combo.setMinimumHeight(32)
        self.location_filter_combo.setMaximumHeight(40)
        self.location_filter_combo.setSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed
        )
        config_layout.addWidget(self.location_filter_combo, 2, 1)
        
        config_layout.addWidget(QLabel("Loại án:"), 2, 2)
        self.case_type_filter_combo = QComboBox()
        self.case_type_filter_combo.addItems([
            "Tất cả", "Án treo", "Cải tạo", "Công ích"
        ])
        self.case_type_filter_combo.setObjectName("caseTypeFilterCombo")
        self.case_type_filter_combo.setMinimumHeight(32)
        self.case_type_filter_combo.setMaximumHeight(40)
        self.case_type_filter_combo.setSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed
        )
        config_layout.addWidget(self.case_type_filter_combo, 2, 3)
        
        # Generate button
        self.generate_button = QPushButton("TẠO BÁO CÁO")
        self.generate_button.setObjectName("generateReportButton")
        self.generate_button.setMinimumHeight(32)
        self.generate_button.setMaximumHeight(40)
        self.generate_button.setFont(QFont("Segoe UI", 11, QFont.Weight.Bold))
        self.generate_button.setSizePolicy(
            QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed
        )
        config_layout.addWidget(self.generate_button, 3, 3)
        
        parent_layout.addWidget(config_group)
        
    def setup_report_preview(self, parent_layout):
        """Setup report preview section."""
        preview_group = QGroupBox("Xem trước báo cáo")
        preview_group.setFont(QFont("Segoe UI", 11, QFont.Weight.Bold))
        preview_layout = QVBoxLayout(preview_group)
        preview_layout.setContentsMargins(12, 12, 12, 12)
        preview_layout.setSpacing(10)
        
        # Preview container with scroll
        preview_container = QFrame()
        preview_container.setObjectName("previewContainer")
        preview_container_layout = QVBoxLayout(preview_container)
        preview_container_layout.setContentsMargins(0, 0, 0, 0)
        preview_container_layout.setSpacing(0)
        
        self.report_preview = QTextEdit()
        self.report_preview.setReadOnly(True)
        self.report_preview.setMinimumHeight(300)
        self.report_preview.setFont(QFont("Segoe UI", 13))
        self.report_preview.setObjectName("reportPreview")
        self.report_preview.setPlaceholderText("Báo cáo sẽ hiển thị tại đây...")
        
        preview_container_layout.addWidget(self.report_preview)
        preview_layout.addWidget(preview_container)
        
        parent_layout.addWidget(preview_group)
        
    def setup_export_buttons(self, parent_layout):
        """Setup export buttons."""
        button_group = QGroupBox("Xuất báo cáo")
        button_group.setFont(QFont("Segoe UI", 11, QFont.Weight.Bold))
        button_layout = QVBoxLayout(button_group)
        button_layout.setContentsMargins(12, 12, 12, 12)
        button_layout.setSpacing(10)
        
        # Row 1: PDF, Excel, Print
        row1_layout = QHBoxLayout()
        row1_layout.setSpacing(10)
        
        self.export_pdf_button = QPushButton("📄 XUẤT PDF")
        self.export_pdf_button.setObjectName("exportPdfButton")
        self.export_pdf_button.setMinimumHeight(32)
        self.export_pdf_button.setMaximumHeight(40)
        self.export_pdf_button.setFont(QFont("Segoe UI", 11))
        self.export_pdf_button.setSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed
        )
        row1_layout.addWidget(self.export_pdf_button)
        
        self.export_excel_button = QPushButton("📊 XUẤT EXCEL")
        self.export_excel_button.setObjectName("exportExcelButton")
        self.export_excel_button.setMinimumHeight(32)
        self.export_excel_button.setMaximumHeight(40)
        self.export_excel_button.setFont(QFont("Segoe UI", 11))
        self.export_excel_button.setSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed
        )
        row1_layout.addWidget(self.export_excel_button)
        
        self.print_button = QPushButton("🖨️ IN BÁO CÁO")
        self.print_button.setObjectName("printReportButton")
        self.print_button.setMinimumHeight(32)
        self.print_button.setMaximumHeight(40)
        self.print_button.setFont(QFont("Segoe UI", 11))
        self.print_button.setSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed
        )
        row1_layout.addWidget(self.print_button)
        
        button_layout.addLayout(row1_layout)
        
        # Row 2: Confirmation, Email
        row2_layout = QHBoxLayout()
        row2_layout.setSpacing(10)
        
        self.print_confirmation_button = QPushButton("📋 IN GIẤY XÁC NHẬN")
        self.print_confirmation_button.setObjectName("printConfirmationButton")
        self.print_confirmation_button.setMinimumHeight(32)
        self.print_confirmation_button.setMaximumHeight(40)
        self.print_confirmation_button.setFont(QFont("Segoe UI", 11))
        self.print_confirmation_button.setSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed
        )
        row2_layout.addWidget(self.print_confirmation_button)
        
        self.email_button = QPushButton("📧 GỬI EMAIL")
        self.email_button.setObjectName("sendEmailButton")
        self.email_button.setMinimumHeight(32)
        self.email_button.setMaximumHeight(40)
        self.email_button.setFont(QFont("Segoe UI", 11))
        self.email_button.setSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed
        )
        row2_layout.addWidget(self.email_button)
        
        # Add stretch to center buttons
        row2_layout.addStretch()
        
        button_layout.addLayout(row2_layout)
        
        parent_layout.addWidget(button_group)
        
    def setup_connections(self):
        """Setup signal connections."""
        self.generate_button.clicked.connect(self.generate_report)
        self.export_excel_button.clicked.connect(self.export_to_excel)
        self.export_pdf_button.clicked.connect(self.export_to_pdf)
        self.print_button.clicked.connect(self.print_report)
        self.print_confirmation_button.clicked.connect(self.print_confirmation_letter)
        self.email_button.clicked.connect(self.send_email)
        
        # Keyboard shortcuts
        self.generate_button.setShortcut("Ctrl+G")
        self.export_excel_button.setShortcut("Ctrl+E")
        self.export_pdf_button.setShortcut("Ctrl+P")
        
    def generate_report(self):
        """Generate report based on configuration."""
        try:
            # Get report type
            report_type_map = {
                "Báo cáo tháng": "monthly",
                "Báo cáo quý": "quarterly", 
                "Báo cáo năm": "annual",
                "Báo cáo trạng thái": "status",
                "Báo cáo nguy cơ": "risk"
            }
            
            report_type = report_type_map.get(
                self.report_type_combo.currentText(), "monthly"
            )
            
            # Get filters
            filters = {
                'start_date': self.start_date_edit.date().toPyDate(),
                'end_date': self.end_date_edit.date().toPyDate(),
                'location': self.location_filter_combo.currentText(),
                'case_type': self.case_type_filter_combo.currentText()
            }
            
            # Get offenders
            offenders = self.offender_service.get_all_offenders()
            
            # Generate report
            report_data = self.report_service.generate_report(
                report_type, offenders, filters
            )
            
            # Display report
            self.display_report(report_data)
            
            QMessageBox.information(
                self, "Thành công", "Báo cáo đã được tạo thành công!"
            )
            
        except Exception as e:
            QMessageBox.critical(
                self, "Lỗi", f"Không thể tạo báo cáo: {str(e)}"
            )
            self.report_preview.setText(f"Lỗi tạo báo cáo: {str(e)}")
            
    def display_report(self, report_data: Dict[str, Any]):
        """Display report in preview area."""
        try:
            report_text = f"""
BÁO CÁO {report_data.get('report_type', '').upper()}
Thời gian: {report_data.get('period', 'N/A')}
Ngày tạo: {report_data.get('created_at', 'N/A')}

TỔNG QUAN:
• Tổng số đối tượng: {report_data.get('total_offenders', 0)}
• Đối tượng mới: {report_data.get('new_offenders', 0)}

PHÂN BỐ TRẠNG THÁI:
• Đang chấp hành: {report_data.get('active_offenders', 0)}
• Đã hoàn thành: {report_data.get('completed_offenders', 0)}
• Vi phạm: {report_data.get('violation_offenders', 0)}
• Sắp hết hạn: {report_data.get('expiring_soon', 0)}

PHÂN BỐ NGUY CƠ:
• Nguy cơ cao: {report_data.get('high_risk', 0)}
• Nguy cơ trung bình: {report_data.get('medium_risk', 0)}
• Nguy cơ thấp: {report_data.get('low_risk', 0)}

TỶ LỆ:
• Tỷ lệ hoàn thành: {report_data.get('completion_rate', 0):.1f}%
• Tỷ lệ vi phạm: {report_data.get('violation_rate', 0):.1f}%

CHI TIẾT:
"""
            
            # Add status distribution if available
            status_dist = report_data.get('status_distribution', {})
            if status_dist:
                report_text += f"""
Phân bố trạng thái chi tiết:
• Đang chấp hành: {status_dist.get('active', 0)}
• Đã hoàn thành: {status_dist.get('completed', 0)}
• Vi phạm: {status_dist.get('violations', 0)}
• Sắp kết thúc: {status_dist.get('expiring_soon', 0)}
"""
            
            # Add risk distribution if available
            risk_dist = report_data.get('risk_distribution', {})
            if risk_dist:
                report_text += f"""
Phân bố nguy cơ chi tiết:
• Nguy cơ cao: {risk_dist.get('high', 0)}
• Nguy cơ trung bình: {risk_dist.get('medium', 0)}
• Nguy cơ thấp: {risk_dist.get('low', 0)}
"""
            
            # Add top offenders if available
            top_offenders = report_data.get('top_offenders', [])
            if top_offenders:
                report_text += "\nĐỐI TƯỢNG NỔI BẬT:\n"
                for i, offender in enumerate(top_offenders[:5], 1):
                    status_val = offender.get('status', 'N/A')
                    risk_val = offender.get('risk_level', 'N/A')
                    report_text += (
                        f"{i}. {offender.get('name', 'N/A')} - "
                        f"{status_val}\n"
                    )
            
            self.report_preview.setText(report_text)
            
        except Exception as e:
            self.report_preview.setText(f"Lỗi hiển thị báo cáo: {str(e)}")
            
    def export_to_excel(self):
        """Export report to Excel."""
        try:
            filename, _ = QFileDialog.getSaveFileName(
                self, "Xuất Excel", "bao_cao.xlsx", "Excel Files (*.xlsx)"
            )
            
            if filename:
                # Get current report data
                report_type = self.report_type_combo.currentText()
                filters = {
                    'start_date': self.start_date_edit.date().toPyDate(),
                    'end_date': self.end_date_edit.date().toPyDate(),
                    'location': self.location_filter_combo.currentText(),
                    'case_type': self.case_type_filter_combo.currentText()
                }
                
                offenders = self.offender_service.get_all_offenders()
                report_data = self.report_service.generate_report(
                    "excel", offenders, filters
                )
                
                # Export to Excel using report service
                success = self.report_service.export_to_excel(offenders, filename)
                
                if success:
                    QMessageBox.information(
                        self, "Thành công", 
                        f"Báo cáo đã được xuất đến {filename}"
                    )
                else:
                    QMessageBox.critical(
                        self, "Lỗi", "Không thể xuất báo cáo Excel!"
                    )
                    
        except Exception as e:
            QMessageBox.critical(
                self, "Lỗi", f"Lỗi khi xuất Excel: {str(e)}"
            )
            
    def export_to_pdf(self):
        """Export report to PDF."""
        try:
            filename, _ = QFileDialog.getSaveFileName(
                self, "Xuất PDF", "bao_cao.pdf", "PDF Files (*.pdf)"
            )
            
            if filename:
                QMessageBox.information(
                    self, "Thông báo", 
                    "Tính năng xuất PDF sẽ được phát triển sau"
                )
                
        except Exception as e:
            QMessageBox.critical(
                self, "Lỗi", f"Lỗi khi xuất PDF: {str(e)}"
            )
            
    def print_report(self):
        """Print report."""
        try:
            QMessageBox.information(
                self, "Thông báo", 
                "Tính năng in báo cáo sẽ được phát triển sau"
            )
            
        except Exception as e:
            QMessageBox.critical(
                self, "Lỗi", f"Lỗi khi in báo cáo: {str(e)}"
            )
            
    def print_confirmation_letter(self):
        """Print confirmation letter."""
        try:
                QMessageBox.information(
                self, "Thông báo", 
                "Tính năng in giấy xác nhận sẽ được phát triển sau"
                )
                
        except Exception as e:
            QMessageBox.critical(
                self, "Lỗi", f"Lỗi khi in giấy xác nhận: {str(e)}"
            )
    
    def send_email(self):
        """Send report via email."""
        try:
            QMessageBox.information(
                self, "Thông báo", 
                "Tính năng gửi email sẽ được phát triển sau"
            )
            
        except Exception as e:
            QMessageBox.critical(
                self, "Lỗi", f"Lỗi khi gửi email: {str(e)}"
            )
            
    def refresh_data(self):
        """Refresh report data."""
        try:
            # Update filters with current data
            offenders = self.offender_service.get_all_offenders()
            
            # Update location filter
            locations = set()
            for offender in offenders:
                if hasattr(offender, 'address') and offender.address:
                    # Extract location from address
                    address_parts = offender.address.split(',')
                    if len(address_parts) > 0:
                        locations.add(address_parts[0].strip())
            
            current_location = self.location_filter_combo.currentText()
            self.location_filter_combo.clear()
            self.location_filter_combo.addItem("Tất cả")
            for location in sorted(locations):
                self.location_filter_combo.addItem(location)
            
            if current_location in locations:
                self.location_filter_combo.setCurrentText(current_location)
            
            # Update case type filter
            case_types = set()
            for offender in offenders:
                if hasattr(offender, 'case_type') and offender.case_type:
                    case_types.add(offender.case_type.value)
            
            current_case_type = self.case_type_filter_combo.currentText()
            self.case_type_filter_combo.clear()
            self.case_type_filter_combo.addItem("Tất cả")
            for case_type in sorted(case_types):
                self.case_type_filter_combo.addItem(case_type)
            
            if current_case_type in case_types:
                self.case_type_filter_combo.setCurrentText(current_case_type)
                
        except Exception as e:
            QMessageBox.critical(
                self, "Lỗi", f"Không thể cập nhật dữ liệu: {str(e)}"
            ) 
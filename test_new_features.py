#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Demo script to test new features.
"""

import sys
import os
from pathlib import Path

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton, QLabel
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont

from database.database_manager import DatabaseManager
from services.offender_service import OffenderService
from services.excel_service import ExcelService
from services.document_service import DocumentService
from ui.offender_form import OffenderForm
from ui.offender_list import OffenderList


class FeatureDemo(QMainWindow):
    """Demo window for new features."""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Demo - Tính Năng Mới")
        self.resize(1200, 800)
        
        # Initialize services
        self.db_manager = DatabaseManager()
        self.offender_service = OffenderService(self.db_manager)
        self.excel_service = ExcelService(self.offender_service)
        self.document_service = DocumentService()
        
        # Setup UI
        self.setup_ui()
        
    def setup_ui(self):
        """Setup demo UI."""
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        layout = QVBoxLayout(central_widget)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(20)
        
        # Title
        title = QLabel("🎯 DEMO TÍNH NĂNG MỚI")
        title.setFont(QFont("Segoe UI", 24, QFont.Weight.Bold))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("color: #1976D2; margin: 20px;")
        layout.addWidget(title)
        
        # Description
        desc = QLabel("""
        ✅ Form nhập liệu hiện đại - Bỏ 3 tab thành trang đơn
        ✅ Danh sách hiển thị 20 trường với top header nhỏ đẹp
        ✅ Cảnh báo trước 5 ngày (thay vì 30 ngày)
        ✅ Nhập từ Excel có tính năng tự động
        ✅ In mẫu giấy xác nhận từ file .docx
        """)
        desc.setFont(QFont("Segoe UI", 14))
        desc.setStyleSheet("color: #424242; margin: 20px;")
        desc.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(desc)
        
        # Demo buttons
        self.create_demo_buttons(layout)
        
        # Add stretch
        layout.addStretch()
        
    def create_demo_buttons(self, parent_layout):
        """Create demo buttons."""
        buttons_layout = QVBoxLayout()
        buttons_layout.setSpacing(15)
        
        # Form demo
        form_btn = QPushButton("📝 XEM FORM NHẬP LIỆU MỚI")
        form_btn.setMinimumHeight(50)
        form_btn.setFont(QFont("Segoe UI", 14, QFont.Weight.Bold))
        form_btn.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 10px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """)
        form_btn.clicked.connect(self.show_form_demo)
        buttons_layout.addWidget(form_btn)
        
        # List demo
        list_btn = QPushButton("📋 XEM DANH SÁCH MỚI")
        list_btn.setMinimumHeight(50)
        list_btn.setFont(QFont("Segoe UI", 14, QFont.Weight.Bold))
        list_btn.setStyleSheet("""
            QPushButton {
                background-color: #2196F3;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 10px;
            }
            QPushButton:hover {
                background-color: #1976D2;
            }
        """)
        list_btn.clicked.connect(self.show_list_demo)
        buttons_layout.addWidget(list_btn)
        
        # Excel demo
        excel_btn = QPushButton("📊 TEST NHẬP/XUẤT EXCEL")
        excel_btn.setMinimumHeight(50)
        excel_btn.setFont(QFont("Segoe UI", 14, QFont.Weight.Bold))
        excel_btn.setStyleSheet("""
            QPushButton {
                background-color: #FF9800;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 10px;
            }
            QPushButton:hover {
                background-color: #F57C00;
            }
        """)
        excel_btn.clicked.connect(self.test_excel_features)
        buttons_layout.addWidget(excel_btn)
        
        # Document demo
        doc_btn = QPushButton("📄 TEST IN GIẤY XÁC NHẬN")
        doc_btn.setMinimumHeight(50)
        doc_btn.setFont(QFont("Segoe UI", 14, QFont.Weight.Bold))
        doc_btn.setStyleSheet("""
            QPushButton {
                background-color: #9C27B0;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 10px;
            }
            QPushButton:hover {
                background-color: #7B1FA2;
            }
        """)
        doc_btn.clicked.connect(self.test_document_features)
        buttons_layout.addWidget(doc_btn)
        
        parent_layout.addLayout(buttons_layout)
        
    def show_form_demo(self):
        """Show form demo."""
        from PyQt6.QtWidgets import QDialog
        
        dialog = QDialog(self)
        dialog.setWindowTitle("Form Nhập Liệu Mới")
        dialog.resize(1000, 800)
        
        layout = QVBoxLayout(dialog)
        
        form = OffenderForm(self.offender_service)
        layout.addWidget(form)
        
        dialog.exec()
        
    def show_list_demo(self):
        """Show list demo."""
        from PyQt6.QtWidgets import QDialog
        from services.report_service import ReportService
        
        dialog = QDialog(self)
        dialog.setWindowTitle("Danh Sách Mới")
        dialog.resize(1400, 900)
        
        layout = QVBoxLayout(dialog)
        
        report_service = ReportService()
        offender_list = OffenderList(self.offender_service, report_service)
        layout.addWidget(offender_list)
        
        dialog.exec()
        
    def test_excel_features(self):
        """Test Excel features."""
        from PyQt6.QtWidgets import QMessageBox
        
        try:
            # Test export
            offenders = self.offender_service.get_all_offenders()
            if offenders:
                success = self.excel_service.export_to_excel(offenders, "demo_export.xlsx")
                if success:
                    QMessageBox.information(self, "Thành công", "Xuất Excel thành công! File: demo_export.xlsx")
                else:
                    QMessageBox.warning(self, "Lỗi", "Không thể xuất Excel")
            else:
                QMessageBox.information(self, "Thông báo", "Không có dữ liệu để xuất")
                
        except Exception as e:
            QMessageBox.critical(self, "Lỗi", f"Lỗi khi test Excel: {str(e)}")
            
    def test_document_features(self):
        """Test document features."""
        from PyQt6.QtWidgets import QMessageBox
        
        try:
            offenders = self.offender_service.get_all_offenders()
            if offenders:
                # Test with first offender
                offender = offenders[0]
                result = self.document_service.generate_confirmation_letter(offender)
                
                if result:
                    QMessageBox.information(self, "Thành công", f"Tạo giấy xác nhận thành công!\nFile: {result}")
                else:
                    QMessageBox.warning(self, "Lỗi", "Không thể tạo giấy xác nhận")
            else:
                QMessageBox.information(self, "Thông báo", "Không có dữ liệu để tạo giấy xác nhận")
                
        except Exception as e:
            QMessageBox.critical(self, "Lỗi", f"Lỗi khi test Document: {str(e)}")


def main():
    """Main function."""
    app = QApplication(sys.argv)
    
    # Set application style
    try:
        with open("assets/styles/style.qss", "r", encoding="utf-8") as f:
            app.setStyleSheet(f.read())
    except Exception as e:
        print(f"Không thể load style.qss: {e}")
    
    # Set default font
    font = QFont("Segoe UI", 13)
    app.setFont(font)
    
    # Show demo
    demo = FeatureDemo()
    demo.show()
    
    return app.exec()


if __name__ == "__main__":
    sys.exit(main()) 
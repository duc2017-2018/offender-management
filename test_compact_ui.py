#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test script for compact UI of OffenderList.
"""

import sys
import os
from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QLabel, QPushButton, QFrame
from PyQt6.QtCore import pyqtSignal, Qt

# Add the project root to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from ui.offender_list import OffenderList
from services.offender_service import OffenderService
from services.report_service import ReportService
from database.database_manager import DatabaseManager


class TestCompactUI(QMainWindow):
    """Test window for compact UI of OffenderList."""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Test Compact UI - OffenderList")
        self.setGeometry(100, 100, 1400, 900)
        
        # Initialize services
        self.db_manager = DatabaseManager()
        self.offender_service = OffenderService(self.db_manager)
        self.report_service = ReportService()
        
        # Setup UI
        self.setup_ui()
        
    def setup_ui(self):
        """Setup test UI."""
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        layout = QVBoxLayout(central_widget)
        
        # Title
        title = QLabel("🧪 TEST COMPACT UI - OFFENDER LIST")
        title.setStyleSheet("font-size: 18px; font-weight: bold; color: #1976D2; margin: 10px;")
        layout.addWidget(title)
        
        # Instructions
        instructions = QLabel("""
        Hướng dẫn test:
        1. Kiểm tra kích thước các nút tác vụ (nhỏ gọn, không bị chèn lấn)
        2. Kiểm tra filter panel (compact, dễ sử dụng)
        3. Kiểm tra responsive design
        4. Test các chức năng: thêm, sửa, xóa, import/export
        """)
        instructions.setStyleSheet("background-color: #f0f0f0; padding: 10px; border-radius: 5px;")
        layout.addWidget(instructions)
        
        # OffenderList
        self.offender_list = OffenderList(self.offender_service, self.report_service)
        layout.addWidget(self.offender_list)
        
        # Status label
        self.status_label = QLabel("✅ Giao diện compact đã được tải")
        self.status_label.setStyleSheet("color: #4CAF50; font-weight: bold; margin: 10px;")
        layout.addWidget(self.status_label)
        
    def show_status(self, message: str, color: str = "#1976D2"):
        """Show status message."""
        self.status_label.setText(message)
        self.status_label.setStyleSheet(f"color: {color}; font-weight: bold; margin: 10px;")


class DemoUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Demo UI - Button, Card, Alert")
        self.setMinimumSize(400, 400)
        layout = QVBoxLayout(self)
        layout.setSpacing(24)
        layout.setContentsMargins(32, 32, 32, 32)

        # 1. Button (Primary)
        btn = QPushButton("Primary Action")
        btn.setObjectName("btn-primary")
        btn.setProperty("class", "btn-primary")
        layout.addWidget(btn)

        # 2. Card
        card = QFrame()
        card.setObjectName("card")
        card.setProperty("class", "card")
        card.setFrameShape(QFrame.Shape.StyledPanel)
        card.setFrameShadow(QFrame.Shadow.Raised)
        card_layout = QVBoxLayout(card)
        card_layout.setSpacing(12)
        card_layout.setContentsMargins(24, 24, 24, 24)
        card_title = QLabel("Card Title")
        card_title.setStyleSheet("font-size: 16px; font-weight: 600; color: #1e40af;")
        card_content = QLabel("Đây là nội dung của card. Card sử dụng border, radius, padding, shadow theo chuẩn design system.")
        card_content.setWordWrap(True)
        card_layout.addWidget(card_title)
        card_layout.addWidget(card_content)
        layout.addWidget(card)

        # 3. Alert
        alert = QFrame()
        alert.setObjectName("alert")
        alert.setProperty("class", "alert")
        alert.setProperty("status", "warning")
        alert.setFrameShape(QFrame.Shape.StyledPanel)
        alert.setFrameShadow(QFrame.Shadow.Raised)
        alert_layout = QVBoxLayout(alert)
        alert_layout.setSpacing(8)
        alert_layout.setContentsMargins(16, 16, 16, 16)
        alert_label = QLabel("⚠️ Cảnh báo: Dữ liệu chưa được lưu!")
        alert_label.setStyleSheet("font-size: 14px; font-weight: 500;")
        alert_layout.addWidget(alert_label)
        layout.addWidget(alert)


def main():
    """Main test function."""
    app = QApplication(sys.argv)
    
    # Create test window
    test_window = TestCompactUI()
    test_window.show()

    # Apply styles
    with open("assets/styles/style.qss", "r", encoding="utf-8") as f:
        app.setStyleSheet(f.read())

    # Run the application
    sys.exit(app.exec())


if __name__ == "__main__":
    main() 
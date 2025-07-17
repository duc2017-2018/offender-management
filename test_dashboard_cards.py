#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test script for dashboard card click functionality.
"""

import sys
import os
from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton, QLabel, QHBoxLayout
from PyQt6.QtCore import pyqtSignal

# Add the project root to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from ui.dashboard import Dashboard
from ui.main_window import MainWindow
from services.offender_service import OffenderService
from services.user_service import UserService
from services.ai_service import AIService
from services.report_service import ReportService
from database.database_manager import DatabaseManager


class TestDashboardCards(QMainWindow):
    """Test window for dashboard card functionality."""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Test Dashboard Cards")
        self.setGeometry(100, 100, 1200, 800)
        
        # Initialize services
        self.db_manager = DatabaseManager()
        self.offender_service = OffenderService(self.db_manager)
        self.user_service = UserService(self.db_manager)
        self.ai_service = AIService()
        self.report_service = ReportService(self.offender_service)
        
        # Setup UI
        self.setup_ui()
        
    def setup_ui(self):
        """Setup test UI."""
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        layout = QVBoxLayout(central_widget)
        
        # Title
        title = QLabel("🧪 TEST DASHBOARD CARD CLICKS")
        title.setStyleSheet("font-size: 18px; font-weight: bold; color: #1976D2; margin: 10px;")
        layout.addWidget(title)
        
        # Instructions
        instructions = QLabel("""
        Hướng dẫn test:
        1. Click vào các card thống kê (Đang chấp hành, Sắp kết thúc, Vi phạm, Nguy cơ cao)
        2. Click vào các group box (Cảnh báo, AI Insights, Hoạt động gần đây)
        3. Kiểm tra xem có chuyển đến đúng trang/tính năng không
        """)
        instructions.setStyleSheet("background-color: #f0f0f0; padding: 10px; border-radius: 5px;")
        layout.addWidget(instructions)
        
        # Dashboard
        self.dashboard = Dashboard(self.offender_service, self.ai_service)
        self.dashboard.card_clicked.connect(self.handle_card_click)
        layout.addWidget(self.dashboard)
        
        # Status label
        self.status_label = QLabel("Chưa có action nào được thực hiện")
        self.status_label.setStyleSheet("color: #666; font-style: italic; margin: 10px;")
        layout.addWidget(self.status_label)
        
        # Test buttons
        test_layout = QHBoxLayout()
        
        refresh_btn = QPushButton("🔄 Refresh Dashboard")
        refresh_btn.clicked.connect(self.dashboard.refresh_data)
        test_layout.addWidget(refresh_btn)
        
        clear_btn = QPushButton("🗑️ Clear Status")
        clear_btn.clicked.connect(self.clear_status)
        test_layout.addWidget(clear_btn)
        
        layout.addLayout(test_layout)
        
    def handle_card_click(self, action_type: str, filter_data: dict):
        """Handle dashboard card click."""
        status_text = f"✅ Card clicked: {action_type}\n"
        status_text += f"📊 Filter data: {filter_data}\n"
        
        if action_type == "offender_list":
            status_text += "🎯 Action: Chuyển đến danh sách đối tượng"
            if filter_data.get("status") == "active":
                status_text += " (Filter: Đang chấp hành)"
            elif filter_data.get("status") == "warning":
                status_text += " (Filter: Sắp hết hạn)"
            elif filter_data.get("status") == "violation":
                status_text += " (Filter: Vi phạm)"
            elif filter_data.get("status") == "risk":
                status_text += " (Filter: Nguy cơ cao)"
                
        elif action_type == "alerts":
            status_text += "🚨 Action: Chuyển đến danh sách với filter cảnh báo"
            
        elif action_type == "ai_tools":
            status_text += "🤖 Action: Chuyển đến AI Tools"
            
        elif action_type == "reports":
            status_text += "📊 Action: Chuyển đến Reports"
            
        self.status_label.setText(status_text)
        self.status_label.setStyleSheet("color: #1976D2; font-weight: bold; background-color: #E3F2FD; padding: 10px; border-radius: 5px;")
        
    def clear_status(self):
        """Clear status label."""
        self.status_label.setText("Chưa có action nào được thực hiện")
        self.status_label.setStyleSheet("color: #666; font-style: italic; margin: 10px;")


def main():
    """Main test function."""
    app = QApplication(sys.argv)
    
    # Create test window
    test_window = TestDashboardCards()
    test_window.show()
    
    # Run the application
    sys.exit(app.exec())


if __name__ == "__main__":
    main() 
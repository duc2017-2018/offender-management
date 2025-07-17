#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test dashboard với notification cards tích hợp.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QLabel
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont

from ui.dashboard import Dashboard
from services.offender_service import OffenderService
from services.ai_service import AIService
from utils.database import DatabaseManager


class TestDashboardWindow(QMainWindow):
    """Test window cho dashboard với notification cards."""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Test Dashboard - Notification Cards")
        self.setGeometry(100, 100, 1200, 800)
        
        # Setup database và services
        self.db_manager = DatabaseManager()
        self.offender_service = OffenderService(self.db_manager)
        self.ai_service = AIService()
        
        # Setup UI
        self.setup_ui()
        
    def setup_ui(self):
        """Setup user interface."""
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        layout = QVBoxLayout(central_widget)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(20)
        
        # Title
        title_label = QLabel("🧪 TEST DASHBOARD - NOTIFICATION CARDS")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label.setFont(QFont("Segoe UI", 18, QFont.Weight.Bold))
        title_label.setStyleSheet("color: #1976D2; margin: 10px;")
        layout.addWidget(title_label)
        
        # Dashboard
        self.dashboard = Dashboard(self.offender_service, self.ai_service)
        self.dashboard.card_clicked.connect(self.handle_card_click)
        layout.addWidget(self.dashboard)
        
        # Test controls
        self.setup_test_controls(layout)
        
    def setup_test_controls(self, parent_layout):
        """Setup test controls."""
        from PyQt6.QtWidgets import QHBoxLayout, QPushButton, QLabel
        
        controls_layout = QHBoxLayout()
        controls_layout.setSpacing(10)
        
        # Test buttons
        test_buttons = [
            ("🔄 Refresh Data", self.refresh_data),
            ("📊 Show Statistics", self.show_statistics),
            ("🎯 Test Notifications", self.test_notifications),
            ("⚡ Simulate Updates", self.simulate_updates)
        ]
        
        for text, callback in test_buttons:
            btn = QPushButton(text)
            btn.setStyleSheet("""
                QPushButton {
                    background: #1976D2;
                    color: white;
                    border: none;
                    padding: 8px 16px;
                    border-radius: 6px;
                    font-weight: bold;
                }
                QPushButton:hover {
                    background: #1565C0;
                }
            """)
            btn.clicked.connect(callback)
            controls_layout.addWidget(btn)
        
        controls_layout.addStretch()
        parent_layout.addLayout(controls_layout)
        
    def handle_card_click(self, action_type: str, filter_data: dict):
        """Handle card click events."""
        print(f"🎯 Card clicked: {action_type}")
        print(f"📋 Filter data: {filter_data}")
        
        # Simulate navigation
        if action_type == "offender_list":
            print("📋 Navigating to offender list...")
        elif action_type == "ai_tools":
            print("🤖 Navigating to AI tools...")
        elif action_type == "activity_log":
            print("📝 Navigating to activity log...")
            
    def refresh_data(self):
        """Refresh dashboard data."""
        print("🔄 Refreshing dashboard data...")
        self.dashboard.refresh_data()
        
    def show_statistics(self):
        """Show current statistics."""
        print("📊 Showing statistics...")
        self.dashboard.show_statistics()
        
    def test_notifications(self):
        """Test notification cards."""
        print("🎯 Testing notification cards...")
        
        # Test updating notification content
        if hasattr(self.dashboard, 'notification_cards') and self.dashboard.notification_cards:
            # Update first notification
            if len(self.dashboard.notification_cards) > 0:
                self.dashboard.notification_cards[0].update_message(
                    "🧪 TEST: Cập nhật thông báo thành công!"
                )
                print("✅ Updated first notification card")
            
            # Test dismiss functionality
            if len(self.dashboard.notification_cards) > 1:
                self.dashboard.notification_cards[1].dismiss()
                print("✅ Dismissed second notification card")
                
    def simulate_updates(self):
        """Simulate real-time updates."""
        print("⚡ Simulating real-time updates...")
        
        # Simulate data changes
        import random
        
        # Update statistics with random values
        stats = {
            "active": random.randint(100, 200),
            "expiring": random.randint(5, 15),
            "violation": random.randint(1, 8),
            "high_risk": random.randint(10, 25)
        }
        
        self.dashboard.update_statistics_cards(stats)
        print(f"📊 Updated statistics: {stats}")
        
        # Update notifications
        self.dashboard.update_notifications()
        print("🔔 Updated notifications")


def main():
    """Main function."""
    app = QApplication(sys.argv)
    
    # Load stylesheet
    try:
        with open("assets/styles/style.qss", "r", encoding="utf-8") as f:
            app.setStyleSheet(f.read())
    except Exception as e:
        print(f"⚠️ Warning: Could not load style.qss: {e}")
    
    # Create and show test window
    window = TestDashboardWindow()
    window.show()
    
    print("🚀 Test Dashboard với Notification Cards đã khởi động!")
    print("📋 Các tính năng test:")
    print("  • 🔄 Refresh Data: Làm mới dữ liệu dashboard")
    print("  • 📊 Show Statistics: Hiển thị thống kê")
    print("  • 🎯 Test Notifications: Test notification cards")
    print("  • ⚡ Simulate Updates: Mô phỏng cập nhật real-time")
    print("  • Click vào notification cards để test action")
    
    sys.exit(app.exec())


if __name__ == "__main__":
    main() 
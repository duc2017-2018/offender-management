#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Demo for notification card component.
"""

import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QWidget, QPushButton, QLabel
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont

from ui.notification_card import (
    NotificationContainer, NotificationType,
    show_success_notification, show_warning_notification,
    show_error_notification, show_info_notification
)


class NotificationDemo(QMainWindow):
    """Demo window for notification cards."""
    
    def __init__(self):
        """Initialize demo window."""
        super().__init__()
        self.setWindowTitle("Notification Card Demo")
        self.resize(800, 600)
        
        # Setup UI
        self.setup_ui()
        
    def setup_ui(self):
        """Setup user interface."""
        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Main layout
        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(20)
        
        # Left side - Control buttons
        control_widget = QWidget()
        control_widget.setMaximumWidth(300)
        control_layout = QVBoxLayout(control_widget)
        control_layout.setContentsMargins(0, 0, 0, 0)
        control_layout.setSpacing(10)
        
        # Title
        title_label = QWidget()
        title_label.setObjectName("demoTitle")
        title_label.setMinimumHeight(40)
        title_label.setStyleSheet("""
            QWidget#demoTitle {
                background: #1976D2;
                color: white;
                border-radius: 8px;
                font-size: 16px;
                font-weight: bold;
                padding: 10px;
            }
        """)
        title_layout = QHBoxLayout(title_label)
        title_layout.addWidget(QLabel("🎯 Notification Demo"))
        control_layout.addWidget(title_label)
        
        # Success button
        success_btn = QPushButton("✅ Success Notification")
        success_btn.clicked.connect(self.show_success)
        control_layout.addWidget(success_btn)
        
        # Warning button
        warning_btn = QPushButton("⚠️ Warning Notification")
        warning_btn.clicked.connect(self.show_warning)
        control_layout.addWidget(warning_btn)
        
        # Error button
        error_btn = QPushButton("❌ Error Notification")
        error_btn.clicked.connect(self.show_error)
        control_layout.addWidget(error_btn)
        
        # Info button
        info_btn = QPushButton("ℹ️ Info Notification")
        info_btn.clicked.connect(self.show_info)
        control_layout.addWidget(info_btn)
        
        # Action notification button
        action_btn = QPushButton("🔗 Action Notification")
        action_btn.clicked.connect(self.show_action_notification)
        control_layout.addWidget(action_btn)
        
        # Clear all button
        clear_btn = QPushButton("🗑️ Clear All")
        clear_btn.clicked.connect(self.clear_all)
        control_layout.addWidget(clear_btn)
        
        # Spacer
        control_layout.addStretch()
        
        # Instructions
        instructions = QWidget()
        instructions.setObjectName("instructions")
        instructions.setStyleSheet("""
            QWidget#instructions {
                background: #f5f5f5;
                border: 1px solid #e0e0e0;
                border-radius: 8px;
                padding: 15px;
                font-size: 12px;
                color: #616161;
            }
        """)
        instructions_layout = QVBoxLayout(instructions)
        instructions_layout.addWidget(QLabel("📋 Instructions:"))
        instructions_layout.addWidget(QLabel("• Click buttons to show notifications"))
        instructions_layout.addWidget(QLabel("• Notifications auto-dismiss after 5s"))
        instructions_layout.addWidget(QLabel("• Error notifications don't auto-dismiss"))
        instructions_layout.addWidget(QLabel("• Click ✕ to dismiss manually"))
        control_layout.addWidget(instructions)
        
        main_layout.addWidget(control_widget)
        
        # Right side - Notification container
        self.notification_container = NotificationContainer()
        self.notification_container.setObjectName("notificationContainer")
        main_layout.addWidget(self.notification_container)
        
    def show_success(self):
        """Show success notification."""
        show_success_notification(
            self.notification_container,
            "Thành công!",
            "Dữ liệu đã được lưu thành công vào hệ thống."
        )
        
    def show_warning(self):
        """Show warning notification."""
        show_warning_notification(
            self.notification_container,
            "Cảnh báo!",
            "Có 3 đối tượng sắp hết hạn trong 5 ngày tới."
        )
        
    def show_error(self):
        """Show error notification."""
        show_error_notification(
            self.notification_container,
            "Lỗi!",
            "Không thể kết nối đến cơ sở dữ liệu. Vui lòng kiểm tra lại."
        )
        
    def show_info(self):
        """Show info notification."""
        show_info_notification(
            self.notification_container,
            "Thông tin",
            "Hệ thống đã được cập nhật phiên bản mới nhất."
        )
        
    def show_action_notification(self):
        """Show notification with action button."""
        notification = self.notification_container.add_notification(
            title="Cập nhật có sẵn",
            message="Phiên bản 2.1.0 đã có sẵn với nhiều tính năng mới.",
            notification_type=NotificationType.INFO,
            auto_dismiss=False,
            show_action=True,
            action_text="Cập nhật ngay"
        )
        notification.action_clicked.connect(self.on_update_clicked)
        
    def on_update_clicked(self):
        """Handle update action click."""
        show_success_notification(
            self.notification_container,
            "Đang cập nhật...",
            "Hệ thống đang tải phiên bản mới."
        )
        
    def clear_all(self):
        """Clear all notifications."""
        self.notification_container.clear_all()


def main():
    """Main function."""
    app = QApplication(sys.argv)
    
    # Load stylesheet
    try:
        with open("assets/styles/style.qss", "r", encoding="utf-8") as f:
            app.setStyleSheet(f.read())
    except Exception as e:
        print(f"Không thể load style.qss: {e}")
    
    # Set default font
    font = QFont("Segoe UI", 13)
    app.setFont(font)
    
    # Create and show demo window
    demo = NotificationDemo()
    demo.show()
    
    # Start event loop
    sys.exit(app.exec())


if __name__ == "__main__":
    main() 
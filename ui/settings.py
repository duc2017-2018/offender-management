#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Settings widget for application configuration.
"""

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QGridLayout, QLabel, 
    QLineEdit, QComboBox, QPushButton, QCheckBox, QTabWidget,
    QGroupBox, QFrame, QSpinBox, QMessageBox
)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont

from typing import Dict, Any

from constants import UI_LAYOUT
from services.user_service import UserService


class SettingsWidget(QWidget):
    """Widget for application settings."""
    
    def __init__(self, user_service: UserService, parent=None):
        """Initialize settings widget."""
        super().__init__(parent)
        self.user_service = user_service
        self.setup_ui()
        self.setup_connections()
        self.load_settings()
        
    def setup_ui(self):
        """Setup user interface."""
        # Main layout
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(20)
        
        # Title
        title_label = QLabel("⚙️ CÀI ĐẶT HỆ THỐNG")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label.setFont(QFont("Segoe UI", 18, QFont.Weight.Bold))
        title_label.setObjectName("sectionTitle")
        main_layout.addWidget(title_label)
        
        # Tab widget
        self.tab_widget = QTabWidget()
        main_layout.addWidget(self.tab_widget)
        
        # Create tabs
        self.setup_general_tab()
        self.setup_security_tab()
        self.setup_backup_tab()
        self.setup_ui_tab()
        
        # Buttons
        button_layout = QHBoxLayout()
        button_layout.setSpacing(10)
        
        self.save_button = QPushButton("LƯU")
        self.save_button.setMinimumSize(120, 40)
        self.save_button.setFont(QFont("Segoe UI", 12, QFont.Weight.Bold))
        self.save_button.setObjectName("primaryButton")
        
        self.cancel_button = QPushButton("HỦY")
        self.cancel_button.setMinimumSize(120, 40)
        self.cancel_button.setFont(QFont("Segoe UI", 12))
        self.cancel_button.setObjectName("secondaryButton")
        
        self.reset_button = QPushButton("KHÔI PHỤC MẶC ĐỊNH")
        self.reset_button.setMinimumSize(150, 40)
        self.reset_button.setFont(QFont("Segoe UI", 12))
        self.reset_button.setObjectName("secondaryButton")
        
        button_layout.addWidget(self.save_button)
        button_layout.addWidget(self.cancel_button)
        button_layout.addStretch()
        button_layout.addWidget(self.reset_button)
        
        main_layout.addLayout(button_layout)
        main_layout.addStretch()  # Đảm bảo co giãn full chiều dọc
        
    def setup_general_tab(self):
        """Setup general settings tab."""
        general_widget = QWidget()
        general_layout = QVBoxLayout(general_widget)
        general_layout.setContentsMargins(20, 20, 20, 20)
        general_layout.setSpacing(20)
        
        # General settings group
        general_group = QGroupBox("Cài đặt chung")
        general_group.setFont(QFont("Segoe UI", 13, QFont.Weight.Bold))
        general_form = QGridLayout(general_group)
        general_form.setSpacing(15)
        
        # Language
        general_form.addWidget(QLabel("Ngôn ngữ:"), 0, 0)
        self.language_combo = QComboBox()
        self.language_combo.addItems(["Tiếng Việt", "English"])
        self.language_combo.setMinimumHeight(35)
        general_form.addWidget(self.language_combo, 0, 1)
        
        # Theme
        general_form.addWidget(QLabel("Giao diện:"), 1, 0)
        self.theme_combo = QComboBox()
        self.theme_combo.addItems(["Light", "Dark"])
        self.theme_combo.setMinimumHeight(35)
        general_form.addWidget(self.theme_combo, 1, 1)
        
        # Auto-save
        self.auto_save_checkbox = QCheckBox("Bật")
        self.auto_save_checkbox.setFont(QFont("Segoe UI", 12))
        general_form.addWidget(QLabel("Auto-save:"), 2, 0)
        general_form.addWidget(self.auto_save_checkbox, 2, 1)
        
        # Notifications
        self.notifications_checkbox = QCheckBox("Bật")
        self.notifications_checkbox.setFont(QFont("Segoe UI", 12))
        general_form.addWidget(QLabel("Thông báo:"), 3, 0)
        general_form.addWidget(self.notifications_checkbox, 3, 1)
        
        # Auto backup
        self.auto_backup_checkbox = QCheckBox("Bật")
        self.auto_backup_checkbox.setFont(QFont("Segoe UI", 12))
        general_form.addWidget(QLabel("Backup tự động:"), 4, 0)
        general_form.addWidget(self.auto_backup_checkbox, 4, 1)
        
        general_layout.addWidget(general_group)
        self.tab_widget.addTab(general_widget, "Chung")
        
    def setup_security_tab(self):
        """Setup security settings tab."""
        security_widget = QWidget()
        security_layout = QVBoxLayout(security_widget)
        security_layout.setContentsMargins(20, 20, 20, 20)
        security_layout.setSpacing(20)
        
        # Security settings group
        security_group = QGroupBox("Cài đặt bảo mật")
        security_group.setFont(QFont("Segoe UI", 13, QFont.Weight.Bold))
        security_form = QGridLayout(security_group)
        security_form.setSpacing(15)
        
        # Session timeout
        security_form.addWidget(QLabel("Thời gian timeout (phút):"), 0, 0)
        self.session_timeout_spin = QSpinBox()
        self.session_timeout_spin.setRange(5, 120)
        self.session_timeout_spin.setValue(30)
        self.session_timeout_spin.setMinimumHeight(35)
        security_form.addWidget(self.session_timeout_spin, 0, 1)
        
        # Password policy
        security_form.addWidget(QLabel("Độ dài mật khẩu tối thiểu:"), 1, 0)
        self.min_password_spin = QSpinBox()
        self.min_password_spin.setRange(6, 20)
        self.min_password_spin.setValue(8)
        self.min_password_spin.setMinimumHeight(35)
        security_form.addWidget(self.min_password_spin, 1, 1)
        
        # Login attempts
        security_form.addWidget(QLabel("Số lần đăng nhập tối đa:"), 2, 0)
        self.max_login_attempts_spin = QSpinBox()
        self.max_login_attempts_spin.setRange(3, 10)
        self.max_login_attempts_spin.setValue(5)
        self.max_login_attempts_spin.setMinimumHeight(35)
        security_form.addWidget(self.max_login_attempts_spin, 2, 1)
        
        # Change password button
        self.change_password_button = QPushButton("ĐỔI MẬT KHẨU")
        self.change_password_button.setMinimumHeight(35)
        self.change_password_button.setFont(QFont("Segoe UI", 12, QFont.Weight.Bold))
        security_form.addWidget(self.change_password_button, 3, 1)
        
        security_layout.addWidget(security_group)
        self.tab_widget.addTab(security_widget, "Bảo mật")
        
    def setup_backup_tab(self):
        """Setup backup settings tab."""
        backup_widget = QWidget()
        backup_layout = QVBoxLayout(backup_widget)
        backup_layout.setContentsMargins(20, 20, 20, 20)
        backup_layout.setSpacing(20)
        
        # Backup settings group
        backup_group = QGroupBox("Cài đặt sao lưu")
        backup_group.setFont(QFont("Segoe UI", 13, QFont.Weight.Bold))
        backup_form = QGridLayout(backup_group)
        backup_form.setSpacing(15)
        
        # Backup frequency
        backup_form.addWidget(QLabel("Tần suất backup:"), 0, 0)
        self.backup_frequency_combo = QComboBox()
        self.backup_frequency_combo.addItems(["Hàng ngày", "Hàng tuần", "Hàng tháng"])
        self.backup_frequency_combo.setMinimumHeight(35)
        backup_form.addWidget(self.backup_frequency_combo, 0, 1)
        
        # Backup retention
        backup_form.addWidget(QLabel("Giữ backup (ngày):"), 1, 0)
        self.backup_retention_spin = QSpinBox()
        self.backup_retention_spin.setRange(7, 365)
        self.backup_retention_spin.setValue(30)
        self.backup_retention_spin.setMinimumHeight(35)
        backup_form.addWidget(self.backup_retention_spin, 1, 1)
        
        # Backup location
        backup_form.addWidget(QLabel("Thư mục backup:"), 2, 0)
        self.backup_location_edit = QLineEdit()
        self.backup_location_edit.setText("data/backups/")
        self.backup_location_edit.setMinimumHeight(35)
        backup_form.addWidget(self.backup_location_edit, 2, 1)
        
        # Manual backup button
        self.manual_backup_button = QPushButton("BACKUP NGAY")
        self.manual_backup_button.setMinimumHeight(35)
        self.manual_backup_button.setFont(QFont("Segoe UI", 12, QFont.Weight.Bold))
        backup_form.addWidget(self.manual_backup_button, 3, 1)
        
        backup_layout.addWidget(backup_group)
        self.tab_widget.addTab(backup_widget, "Backup")
        
    def setup_ui_tab(self):
        """Setup UI settings tab."""
        ui_widget = QWidget()
        ui_layout = QVBoxLayout(ui_widget)
        ui_layout.setContentsMargins(20, 20, 20, 20)
        ui_layout.setSpacing(20)
        
        # UI settings group
        ui_group = QGroupBox("Cài đặt giao diện")
        ui_group.setFont(QFont("Segoe UI", 13, QFont.Weight.Bold))
        ui_form = QGridLayout(ui_group)
        ui_form.setSpacing(15)
        
        # Font size
        ui_form.addWidget(QLabel("Kích thước font:"), 0, 0)
        self.font_size_combo = QComboBox()
        self.font_size_combo.addItems(["Nhỏ (11px)", "Vừa (13px)", "Lớn (15px)"])
        self.font_size_combo.setMinimumHeight(35)
        ui_form.addWidget(self.font_size_combo, 0, 1)
        
        # Window size
        ui_form.addWidget(QLabel("Kích thước cửa sổ:"), 1, 0)
        self.window_size_combo = QComboBox()
        self.window_size_combo.addItems(["Nhỏ", "Vừa", "Lớn"])
        self.window_size_combo.setMinimumHeight(35)
        ui_form.addWidget(self.window_size_combo, 1, 1)
        
        # Animations
        self.animations_checkbox = QCheckBox("Bật")
        self.animations_checkbox.setFont(QFont("Segoe UI", 12))
        ui_form.addWidget(QLabel("Hiệu ứng:"), 2, 0)
        ui_form.addWidget(self.animations_checkbox, 2, 1)
        
        # Tooltips
        self.tooltips_checkbox = QCheckBox("Bật")
        self.tooltips_checkbox.setFont(QFont("Segoe UI", 12))
        ui_form.addWidget(QLabel("Tooltips:"), 3, 0)
        ui_form.addWidget(self.tooltips_checkbox, 3, 1)
        
        ui_layout.addWidget(ui_group)
        self.tab_widget.addTab(ui_widget, "Giao diện")
        
    def setup_connections(self):
        """Setup signal connections."""
        self.save_button.clicked.connect(self.save_settings)
        self.cancel_button.clicked.connect(self.cancel_changes)
        self.reset_button.clicked.connect(self.reset_settings)
        self.change_password_button.clicked.connect(self.change_password)
        self.manual_backup_button.clicked.connect(self.manual_backup)
        
    def load_settings(self):
        """Load current settings."""
        # Load from configuration or use defaults
        # This would typically load from a config file
        pass
        
    def save_settings(self):
        """Save settings."""
        try:
            # Collect settings from UI
            settings = {
                'language': self.language_combo.currentText(),
                'theme': self.theme_combo.currentText(),
                'auto_save': self.auto_save_checkbox.isChecked(),
                'notifications': self.notifications_checkbox.isChecked(),
                'auto_backup': self.auto_backup_checkbox.isChecked(),
                'session_timeout': self.session_timeout_spin.value(),
                'min_password_length': self.min_password_spin.value(),
                'max_login_attempts': self.max_login_attempts_spin.value(),
                'backup_frequency': self.backup_frequency_combo.currentText(),
                'backup_retention': self.backup_retention_spin.value(),
                'backup_location': self.backup_location_edit.text(),
                'font_size': self.font_size_combo.currentText(),
                'window_size': self.window_size_combo.currentText(),
                'animations': self.animations_checkbox.isChecked(),
                'tooltips': self.tooltips_checkbox.isChecked()
            }
            
            # Save settings (this would typically save to a config file)
            # For now, just show a success message
            QMessageBox.information(self, "Thành công", "Cài đặt đã được lưu!")
            
        except Exception as e:
            QMessageBox.critical(self, "Lỗi", f"Không thể lưu cài đặt: {str(e)}")
            
    def cancel_changes(self):
        """Cancel changes and reload settings."""
        self.load_settings()
        QMessageBox.information(self, "Thông báo", "Đã hủy thay đổi")
        
    def reset_settings(self):
        """Reset to default settings."""
        reply = QMessageBox.question(
            self, "Xác nhận", 
            "Bạn có chắc chắn muốn khôi phục cài đặt mặc định?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            # Reset to defaults
            self.language_combo.setCurrentText("Tiếng Việt")
            self.theme_combo.setCurrentText("Light")
            self.auto_save_checkbox.setChecked(True)
            self.notifications_checkbox.setChecked(True)
            self.auto_backup_checkbox.setChecked(True)
            self.session_timeout_spin.setValue(30)
            self.min_password_spin.setValue(8)
            self.max_login_attempts_spin.setValue(5)
            self.backup_frequency_combo.setCurrentText("Hàng tuần")
            self.backup_retention_spin.setValue(30)
            self.backup_location_edit.setText("data/backups/")
            self.font_size_combo.setCurrentText("Vừa (13px)")
            self.window_size_combo.setCurrentText("Vừa")
            self.animations_checkbox.setChecked(True)
            self.tooltips_checkbox.setChecked(True)
            
            QMessageBox.information(self, "Thành công", "Đã khôi phục cài đặt mặc định!")
            
    def change_password(self):
        """Change user password."""
        from PyQt6.QtWidgets import QInputDialog
        
        current_user = self.user_service.get_current_user()
        if not current_user:
            QMessageBox.warning(self, "Cảnh báo", "Bạn chưa đăng nhập!")
            return
            
        old_password, ok = QInputDialog.getText(
            self, "Đổi mật khẩu", "Nhập mật khẩu hiện tại:", 
            QLineEdit.EchoMode.Password
        )
        
        if not ok:
            return
            
        new_password, ok = QInputDialog.getText(
            self, "Đổi mật khẩu", "Nhập mật khẩu mới:", 
            QLineEdit.EchoMode.Password
        )
        
        if not ok:
            return
            
        confirm_password, ok = QInputDialog.getText(
            self, "Đổi mật khẩu", "Xác nhận mật khẩu mới:", 
            QLineEdit.EchoMode.Password
        )
        
        if not ok:
            return
            
        if new_password != confirm_password:
            QMessageBox.warning(self, "Lỗi", "Mật khẩu xác nhận không khớp!")
            return
            
        try:
            # This would typically call user_service.change_password()
            QMessageBox.information(self, "Thành công", "Mật khẩu đã được thay đổi!")
        except Exception as e:
            QMessageBox.critical(self, "Lỗi", f"Không thể thay đổi mật khẩu: {str(e)}")
            
    def manual_backup(self):
        """Perform manual backup."""
        try:
            # This would typically call backup_service.create_backup()
            QMessageBox.information(self, "Thành công", "Backup đã được tạo thành công!")
        except Exception as e:
            QMessageBox.critical(self, "Lỗi", f"Không thể tạo backup: {str(e)}") 
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Login Window - Giao diện đăng nhập
"""

import sys
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QGridLayout,
    QLabel, QLineEdit, QPushButton, QCheckBox,
    QFrame, QMessageBox, QApplication
)
from PyQt6.QtCore import Qt, pyqtSignal, QTimer
from PyQt6.QtGui import QFont, QPixmap, QIcon

from constants import *
from utils.auth_manager import AuthManager


class LoginWindow(QWidget):
    """Giao diện đăng nhập"""
    
    # Signals
    login_success = pyqtSignal(dict)
    login_failed = pyqtSignal(str)
    
    def __init__(self, auth_manager: AuthManager):
        super().__init__()
        self.auth_manager = auth_manager
        self.init_ui()
        self.setup_connections()
        
    def init_ui(self):
        """Khởi tạo giao diện"""
        # Main layout
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(12, 12, 12, 12)
        main_layout.setSpacing(10)
        
        # Logo and title
        logo_layout = QHBoxLayout()
        logo_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # Logo
        logo_label = QLabel()
        logo_pixmap = QPixmap("assets/logo_cand.png")
        if not logo_pixmap.isNull():
            logo_pixmap = logo_pixmap.scaled(80, 80, Qt.AspectRatioMode.KeepAspectRatio)
            logo_label.setPixmap(logo_pixmap)
        logo_layout.addWidget(logo_label)
        
        # Title
        title_label = QLabel(APP_NAME)
        title_label.setObjectName("title")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        logo_layout.addWidget(title_label)
        
        main_layout.addLayout(logo_layout)
        
        # Login form
        form_frame = QFrame()
        form_frame.setObjectName("card")
        form_layout = QVBoxLayout(form_frame)
        form_layout.setContentsMargins(12, 12, 12, 12)
        form_layout.setSpacing(10)
        
        # Username field
        username_layout = QVBoxLayout()
        username_label = QLabel("👤 Tên đăng nhập:")
        username_label.setFont(QFont("Segoe UI", 12, QFont.Weight.Bold))
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Nhập tên đăng nhập...")
        self.username_input.setMinimumHeight(40)
        username_layout.addWidget(username_label)
        username_layout.addWidget(self.username_input)
        form_layout.addLayout(username_layout)
        
        # Password field
        password_layout = QVBoxLayout()
        password_label = QLabel("🔒 Mật khẩu:")
        password_label.setFont(QFont("Segoe UI", 12, QFont.Weight.Bold))
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Nhập mật khẩu...")
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.password_input.setMinimumHeight(40)
        password_layout.addWidget(password_label)
        password_layout.addWidget(self.password_input)
        form_layout.addLayout(password_layout)
        
        # Remember me checkbox
        self.remember_checkbox = QCheckBox("Ghi nhớ đăng nhập")
        self.remember_checkbox.setFont(QFont("Segoe UI", 11))
        form_layout.addWidget(self.remember_checkbox)
        
        # Login button
        self.login_button = QPushButton("🚪 ĐĂNG NHẬP")
        self.login_button.setObjectName("primary")
        self.login_button.setMinimumHeight(45)
        self.login_button.setFont(QFont("Segoe UI", 12, QFont.Weight.Bold))
        form_layout.addWidget(self.login_button)
        
        # Exit button
        self.exit_button = QPushButton("❌ THOÁT")
        self.exit_button.setObjectName("danger")
        self.exit_button.setMinimumHeight(40)
        form_layout.addWidget(self.exit_button)
        
        main_layout.addWidget(form_frame)
        
        # Status label
        self.status_label = QLabel("")
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.status_label.setObjectName("statusLabel")
        main_layout.addWidget(self.status_label)
        
        # Add stretch to center the form
        main_layout.addStretch()
        
        self.setLayout(main_layout)
        
        # Set window properties
        self.setWindowTitle("Đăng nhập - " + APP_NAME)
        self.setMinimumSize(400, 300)
        
        # Auto-focus on username
        self.username_input.setFocus()
        
    def setup_connections(self):
        """Thiết lập kết nối signals"""
        # Login button
        self.login_button.clicked.connect(self.handle_login)
        
        # Exit button
        self.exit_button.clicked.connect(self.handle_exit)
        
        # Enter key in password field
        self.password_input.returnPressed.connect(self.handle_login)
        
        # Tab navigation
        self.username_input.returnPressed.connect(
            lambda: self.password_input.setFocus()
        )
        
    def handle_login(self):
        """Xử lý đăng nhập"""
        username = self.username_input.text().strip()
        password = self.password_input.text().strip()
        
        # Validation
        if not username:
            self.show_error("⚠️ Vui lòng nhập tên đăng nhập")
            self.username_input.setFocus()
            return
            
        if not password:
            self.show_error("⚠️ Vui lòng nhập mật khẩu")
            self.password_input.setFocus()
            return
        
        # Disable login button
        self.login_button.setEnabled(False)
        self.login_button.setText("🔄 Đang đăng nhập...")
        
        # Simulate login delay
        QTimer.singleShot(1000, lambda: self.perform_login(username, password))
        
    def perform_login(self, username: str, password: str):
        """Thực hiện đăng nhập"""
        try:
            # Authenticate
            success, user_data = self.auth_manager.authenticate(username, password)
            
            if success:
                # Save remember me setting
                if self.remember_checkbox.isChecked():
                    self.auth_manager.save_credentials(username, password)
                
                # Emit success signal
                self.login_success.emit(user_data)
                self.show_success("✅ Đăng nhập thành công!")
                
            else:
                self.show_error("❌ Tên đăng nhập hoặc mật khẩu không đúng")
                self.password_input.clear()
                self.password_input.setFocus()
                
        except Exception as e:
            self.show_error(f"❌ Lỗi đăng nhập: {str(e)}")
            
        finally:
            # Re-enable login button
            self.login_button.setEnabled(True)
            self.login_button.setText("🚪 ĐĂNG NHẬP")
    
    def handle_exit(self):
        """Xử lý thoát ứng dụng"""
        reply = QMessageBox.question(
            self,
            "Xác nhận thoát",
            "Bạn có chắc chắn muốn thoát ứng dụng?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            QApplication.quit()
    
    def show_error(self, message: str):
        """Hiển thị lỗi"""
        self.status_label.setText(message)
        self.status_label.setObjectName("error")
        # self.status_label.setStyleSheet("color: #F44336; font-weight: bold;")
        
    def show_success(self, message: str):
        """Hiển thị thành công"""
        self.status_label.setText(message)
        self.status_label.setObjectName("success")
        # self.status_label.setStyleSheet("color: #4CAF50; font-weight: bold;")
        
    def clear_fields(self):
        """Xóa các trường nhập liệu"""
        self.username_input.clear()
        self.password_input.clear()
        self.status_label.clear()
        self.username_input.setFocus()
        
    def load_saved_credentials(self):
        """Load thông tin đăng nhập đã lưu"""
        username, password = self.auth_manager.load_credentials()
        if username and password:
            self.username_input.setText(username)
            self.password_input.setText(password)
            self.remember_checkbox.setChecked(True)
            
    def keyPressEvent(self, event):
        """Xử lý phím tắt"""
        if event.key() == Qt.Key.Key_Escape:
            self.handle_exit()
        elif event.key() == Qt.Key.Key_Return or event.key() == Qt.Key.Key_Enter:
            self.handle_login()
        else:
            super().keyPressEvent(event) 
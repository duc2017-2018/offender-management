#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Login dialog for user authentication.
"""

from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, 
    QPushButton, QMessageBox, QFrame, QGridLayout
)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont, QPixmap, QIcon

from constants import UI_LAYOUT
from services.user_service import UserService


class LoginDialog(QDialog):
    """Login dialog for user authentication."""
    
    # Signal emitted when login is successful
    login_successful = pyqtSignal()
    
    def __init__(self, user_service: UserService, parent=None):
        """Initialize login dialog."""
        super().__init__(parent)
        self.user_service = user_service
        self.setup_ui()
        self.setup_connections()
        
    def setup_ui(self):
        """Setup user interface."""
        # Window properties
        self.setWindowTitle("Đăng nhập - Hệ thống Quản lý Đối tượng Thi hành án")
        self.setMinimumSize(400, 300)
        self.setWindowFlags(Qt.WindowType.Window | Qt.WindowType.WindowCloseButtonHint)
        
        # Main layout
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(12, 12, 12, 12)
        main_layout.setSpacing(10)
        
        # Logo and title
        title_layout = QHBoxLayout()
        
        # Logo
        logo_label = QLabel()
        logo_pixmap = QPixmap("assets/logo_cand.png")
        if not logo_pixmap.isNull():
            logo_pixmap = logo_pixmap.scaled(60, 60, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
            logo_label.setPixmap(logo_pixmap)
        else:
            logo_label.setText("🏛️")
            logo_label.setFont(QFont("Segoe UI", 24))
        
        logo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_layout.addWidget(logo_label)
        
        # Title
        title_label = QLabel("HỆ THỐNG QUẢN LÝ\nĐỐI TƯỢNG THI HÀNH ÁN")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label.setFont(QFont("Segoe UI", 16, QFont.Weight.Bold))
        title_label.setObjectName("loginDialogTitle")
        title_layout.addWidget(title_label)
        
        main_layout.addLayout(title_layout)
        
        # Login form
        form_layout = QGridLayout()
        form_layout.setSpacing(15)
        form_layout.setContentsMargins(12, 12, 12, 12)
        
        # Username
        username_label = QLabel("Tên đăng nhập:")
        username_label.setFont(QFont("Segoe UI", 13))
        self.username_edit = QLineEdit()
        self.username_edit.setPlaceholderText("Nhập tên đăng nhập")
        self.username_edit.setMinimumHeight(40)
        form_layout.addWidget(username_label, 0, 0)
        form_layout.addWidget(self.username_edit, 0, 1)
        
        # Password
        password_label = QLabel("Mật khẩu:")
        password_label.setFont(QFont("Segoe UI", 13))
        self.password_edit = QLineEdit()
        self.password_edit.setPlaceholderText("Nhập mật khẩu")
        self.password_edit.setEchoMode(QLineEdit.EchoMode.Password)
        self.password_edit.setMinimumHeight(40)
        form_layout.addWidget(password_label, 1, 0)
        form_layout.addWidget(self.password_edit, 1, 1)
        
        main_layout.addLayout(form_layout)
        
        # Buttons
        button_layout = QHBoxLayout()
        button_layout.setSpacing(10)
        
        # Login button
        self.login_button = QPushButton("ĐĂNG NHẬP")
        self.login_button.setMinimumHeight(45)
        self.login_button.setFont(QFont("Segoe UI", 13, QFont.Weight.Bold))
        self.login_button.setObjectName("loginDialogBtn")
        
        # Cancel button
        self.cancel_button = QPushButton("THOÁT")
        self.cancel_button.setMinimumHeight(45)
        self.cancel_button.setFont(QFont("Segoe UI", 13))
        self.cancel_button.setObjectName("loginDialogBtn")
        
        button_layout.addWidget(self.login_button)
        button_layout.addWidget(self.cancel_button)
        
        main_layout.addLayout(button_layout)
        
        # Add stretch to push everything to center
        main_layout.addStretch()
        
        self.setLayout(main_layout)
        
        # Set focus to username field
        self.username_edit.setFocus()
        
    def setup_connections(self):
        """Setup signal connections."""
        self.login_button.clicked.connect(self.handle_login)
        self.cancel_button.clicked.connect(self.reject)
        
        # Enter key in password field triggers login
        self.password_edit.returnPressed.connect(self.handle_login)
        
    def handle_login(self):
        """Handle login attempt."""
        username = self.username_edit.text().strip()
        password = self.password_edit.text().strip()
        
        # Validate input
        if not username:
            QMessageBox.warning(self, "Lỗi", "Vui lòng nhập tên đăng nhập!")
            self.username_edit.setFocus()
            return
        
        if not password:
            QMessageBox.warning(self, "Lỗi", "Vui lòng nhập mật khẩu!")
            self.password_edit.setFocus()
            return
        
        # Attempt login
        try:
            user = self.user_service.authenticate(username, password)
            if user:
                QMessageBox.information(self, "Thành công", f"Chào mừng {user.full_name}!")
                self.accept()
            else:
                QMessageBox.warning(self, "Lỗi", "Tên đăng nhập hoặc mật khẩu không đúng!")
                self.password_edit.clear()
                self.password_edit.setFocus()
        except Exception as e:
            QMessageBox.critical(self, "Lỗi", f"Lỗi đăng nhập: {str(e)}")
    
    def keyPressEvent(self, event):
        """Handle key press events."""
        if event.key() == Qt.Key.Key_Escape:
            self.reject()
        else:
            super().keyPressEvent(event) 
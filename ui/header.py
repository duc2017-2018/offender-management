#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Header Widget - Header ứng dụng
"""

from PyQt6.QtWidgets import QWidget, QHBoxLayout, QLabel, QPushButton, QSizePolicy, QMenu
from PyQt6.QtCore import Qt, QTimer, QDateTime
from PyQt6.QtGui import QPixmap, QFont
from constants import UI_FONT, APP_NAME


class HeaderWidget(QWidget):
    """Header ứng dụng: logo, tiêu đề, user, đồng hồ"""
    
    def __init__(self, username="admin"):
        super().__init__()
        self.username = username
        self.setup_ui()
        self.setup_timer()
        
    def setup_ui(self):
        """Thiết lập giao diện header"""
        layout = QHBoxLayout(self)
        layout.setContentsMargins(4, 8, 4, 8)  # giảm padding
        layout.setSpacing(8)  # spacing nhỏ hơn

        # Logo
        self.logo_label = QLabel()
        try:
            pixmap = QPixmap("assets/images/logo_cand.png")
            if not pixmap.isNull():
                pixmap = pixmap.scaled(
                    32, 32, Qt.AspectRatioMode.KeepAspectRatio
                )
                self.logo_label.setPixmap(pixmap)
        except Exception:
            self.logo_label.setText("🏛️")
            self.logo_label.setFont(QFont(UI_FONT['family'], 18))
        layout.addWidget(self.logo_label)

        # Tiêu đề
        self.title_label = QLabel(APP_NAME)
        title_font = QFont(UI_FONT['family'], 16, UI_FONT['weight_bold'])
        self.title_label.setFont(title_font)
        layout.addWidget(self.title_label)

        # Breadcrumb
        self.breadcrumb = QLabel("Dashboard")
        self.breadcrumb.setObjectName("breadcrumb")
        self.breadcrumb.setFont(QFont(UI_FONT['family'], 12))
        layout.addWidget(self.breadcrumb)

        layout.addStretch()

        # User avatar + dropdown
        self.avatar_btn = QPushButton("👤")
        self.avatar_btn.setObjectName("avatarBtn")
        self.avatar_btn.setFixedSize(36, 36)
        self.avatar_btn.setStyleSheet("border-radius: 18px; font-size: 18px;")
        self.avatar_menu = QMenu()
        self.avatar_menu.addAction("Hồ sơ cá nhân")
        self.avatar_menu.addAction("Đổi mật khẩu")
        self.avatar_menu.addSeparator()
        self.avatar_menu.addAction("Đăng xuất")
        self.avatar_btn.setMenu(self.avatar_menu)
        layout.addWidget(self.avatar_btn)

        # Settings button + dropdown
        self.settings_btn = QPushButton("⚙️")
        self.settings_btn.setSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)
        self.settings_btn.setToolTip("Cài đặt")
        self.settings_btn.setObjectName("settingsBtn")
        self.settings_menu = QMenu()
        self.settings_menu.addAction("Chủ đề giao diện")
        self.settings_menu.addAction("Ngôn ngữ")
        self.settings_btn.setMenu(self.settings_menu)
        layout.addWidget(self.settings_btn)

        # Logout button (ẩn, dùng trong avatar menu)
        self.logout_btn = QPushButton("🚪")
        self.logout_btn.setVisible(False)
        layout.addWidget(self.logout_btn)

        # Đồng hồ
        self.time_label = QLabel()
        time_font = QFont(UI_FONT['family'], 12)
        self.time_label.setFont(time_font)
        self.time_label.setObjectName("timeLabel")
        layout.addWidget(self.time_label)
        self.update_time()

        self.set_tab_order_accessibility()

    def setup_timer(self):
        """Thiết lập timer cập nhật thời gian"""
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_time)
        self.timer.start(1000)  # Update every second

    def update_time(self):
        """Cập nhật thời gian"""
        now = QDateTime.currentDateTime().toString("HH:mm:ss dd/MM/yyyy")
        self.time_label.setText(now)
        
    def update_title(self, title: str):
        """Cập nhật tiêu đề"""
        self.title_label.setText(title)
        
    def update_user(self, username: str):
        """Cập nhật thông tin user"""
        self.username = username
        # self.user_label.setText(f"Người dùng: {username}") # This line was removed as per the edit hint
        
    def set_logout_callback(self, callback):
        """Thiết lập callback cho nút logout"""
        self.logout_btn.clicked.connect(callback)
        
    def set_settings_callback(self, callback):
        """Thiết lập callback cho nút settings"""
        self.settings_btn.clicked.connect(callback) 

    def set_tab_order_accessibility(self):
        """Đảm bảo accessibility: set tab order cho các nút header."""
        # Tab order: avatar_btn -> settings_btn -> time_label
        self.setTabOrder(self.avatar_btn, self.settings_btn)
        self.setTabOrder(self.settings_btn, self.time_label) 

    def is_sticky(self) -> bool:
        """Header luôn sticky (luôn trên cùng)."""
        return True 
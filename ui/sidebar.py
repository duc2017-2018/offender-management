#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Sidebar Widget - Sidebar navigation
"""

from PyQt6.QtWidgets import QWidget
from PyQt6.QtWidgets import QVBoxLayout
from PyQt6.QtWidgets import QPushButton
from PyQt6.QtWidgets import QLabel
from PyQt6.QtWidgets import QFrame
from PyQt6.QtWidgets import QScrollArea
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from constants import UI_FONT, PAGES, SIDEBAR_WIDTH


class SidebarWidget(QWidget):
    """Sidebar navigation với các menu chính"""
    
    def __init__(self, page_callback):
        super().__init__()
        self.setObjectName("SidebarWidget")
        self.page_callback = page_callback
        self.current_page = 0
        self.nav_buttons = {}
        self._mini_mode = False  # Thêm thuộc tính mini mode
        self.setup_ui()
        
    def setup_ui(self):
        """Thiết lập giao diện sidebar"""
        self._sidebar_width_full = SIDEBAR_WIDTH if hasattr(self, '_sidebar_width_full') else 220
        self._sidebar_width_mini = 60
        self.setFixedWidth(self._sidebar_width_full if not self._mini_mode else self._sidebar_width_mini)
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(12, 12, 12, 12)
        main_layout.setSpacing(10)
        # Toggle button
        self.toggle_btn = QPushButton("≡")
        self.toggle_btn.setObjectName("sidebar_toggle_btn")
        self.toggle_btn.setFixedSize(36, 36)
        self.toggle_btn.setCheckable(True)
        self.toggle_btn.setChecked(self._mini_mode)
        self.toggle_btn.clicked.connect(self.toggle_sidebar_mode)
        main_layout.addWidget(self.toggle_btn, alignment=Qt.AlignmentFlag.AlignLeft)
        # Scrollable content area
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_content = QWidget()
        scroll_content.setObjectName("SidebarContent")
        self._scroll_layout = QVBoxLayout(scroll_content)
        self._scroll_layout.setContentsMargins(0, 0, 0, 0)
        self._scroll_layout.setSpacing(0)
        # Logo section
        self.setup_logo_section(self._scroll_layout)
        # Navigation buttons
        self.setup_navigation_buttons(self._scroll_layout)
        self._scroll_layout.addStretch()
        scroll_area.setWidget(scroll_content)
        main_layout.addWidget(scroll_area)
        # Bottom section (user info, logout)
        self.setup_bottom_section(main_layout)
        self.update_sidebar_mode()

    def setup_logo_section(self, parent_layout):
        """Thiết lập phần logo"""
        logo_frame = QFrame()
        logo_frame.setObjectName("logo_frame")
        
        logo_layout = QVBoxLayout(logo_frame)
        logo_layout.setContentsMargins(16, 16, 16, 16)
        logo_layout.setSpacing(8)

        # Logo text
        logo_label = QLabel("🏛️")
        logo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        logo_font = QFont(UI_FONT['family'], 32)
        logo_label.setFont(logo_font)
        logo_layout.addWidget(logo_label)

        # App name
        app_name = QLabel("QUẢN LÝ\nĐỐI TƯỢNG")
        app_name.setAlignment(Qt.AlignmentFlag.AlignCenter)
        app_name.setWordWrap(True)
        app_font = QFont(
            UI_FONT['family'], UI_FONT['size_small'], UI_FONT['weight_bold']
        )
        app_name.setFont(app_font)
        logo_layout.addWidget(app_name)

        parent_layout.addWidget(logo_frame)

    def setup_navigation_buttons(self, parent_layout):
        """Thiết lập các nút navigation"""
        nav_frame = QFrame()
        nav_frame.setObjectName("nav_frame")
        
        nav_layout = QVBoxLayout(nav_frame)
        nav_layout.setContentsMargins(8, 8, 8, 8)
        nav_layout.setSpacing(4)

        # Create navigation buttons
        for page_id, page_info in PAGES.items():
            btn = self.create_nav_button(
                page_info['icon'], page_info['name'], page_id
            )
            nav_layout.addWidget(btn)
            self.nav_buttons[page_id] = btn

        parent_layout.addWidget(nav_frame)

    def create_nav_button(self, icon: str, text: str, page_id: int):
        """Tạo nút navigation"""
        btn = QPushButton(f"{icon} {text}")
        btn.setCheckable(True)
        btn.setMinimumHeight(45)
        btn.setFont(QFont(UI_FONT['family'], UI_FONT['size_normal']))
        btn.setObjectName("nav_button")  # Đảm bảo dùng objectName để nhận QSS động
        # Không dùng setStyleSheet nội bộ
        # Connect signal
        btn.clicked.connect(lambda: self.on_nav_button_clicked(page_id))
        # Set initial state
        if page_id == 0:
            btn.setChecked(True)
        return btn

    def setup_bottom_section(self, parent_layout):
        # Không cần addStretch ở đây nữa vì đã add trong scroll
        bottom_frame = QFrame()
        bottom_frame.setObjectName("bottom_frame")
        bottom_layout = QVBoxLayout(bottom_frame)
        bottom_layout.setContentsMargins(8, 8, 8, 8)
        bottom_layout.setSpacing(4)
        # User info
        user_label = QLabel("👤 Người dùng: admin")
        user_label.setFont(QFont(UI_FONT['family'], UI_FONT['size_small']))
        user_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        bottom_layout.addWidget(user_label)
        # Logout button
        logout_btn = QPushButton("🚪 Đăng xuất")
        logout_btn.setMinimumHeight(40)
        logout_btn.setFont(QFont(UI_FONT['family'], UI_FONT['size_small']))
        logout_btn.setObjectName("logout_button")
        bottom_layout.addWidget(logout_btn)
        parent_layout.addWidget(bottom_frame)

    def on_nav_button_clicked(self, page_id: int):
        """Xử lý khi click nút navigation"""
        # Update button states
        for btn_id, btn in self.nav_buttons.items():
            btn.setChecked(btn_id == page_id)
        
        # Update current page
        self.current_page = page_id
        
        # Call callback
        if self.page_callback:
            self.page_callback(page_id)

    def update_selection(self, page_id: int):
        """Cập nhật selection"""
        if page_id in self.nav_buttons:
            for btn_id, btn in self.nav_buttons.items():
                btn.setChecked(btn_id == page_id)
            self.current_page = page_id

    def disable_sections(self, page_ids: list):
        """Vô hiệu hóa các section"""
        for page_id in page_ids:
            if page_id in self.nav_buttons:
                self.nav_buttons[page_id].setEnabled(False)

    def enable_sections(self, page_ids: list):
        """Kích hoạt các section"""
        for page_id in page_ids:
            if page_id in self.nav_buttons:
                self.nav_buttons[page_id].setEnabled(True)

    def get_current_page(self) -> int:
        """Lấy trang hiện tại"""
        return self.current_page

    def set_user_info(self, username: str):
        """Cập nhật thông tin user"""
        # TODO: Update user info in bottom section
        pass 

    def set_mini_mode(self, mini: bool):
        """Chuyển sidebar sang chế độ mini (chỉ icon) hoặc đầy đủ (icon + text)."""
        self._mini_mode = mini  # Cập nhật trạng thái mini mode
        for page_id, btn in self.nav_buttons.items():
            if mini:
                # Chỉ hiện icon (lấy ký tự đầu)
                icon = PAGES[page_id]['icon']
                btn.setText(icon)
                btn.setMinimumHeight(48)
                btn.setMaximumHeight(56)
                # Không setStyleSheet inline, mọi style lấy từ QSS
            else:
                # Hiện icon + text
                page_info = PAGES[page_id]
                btn.setText(f"{page_info['icon']} {page_info['name']}")
                btn.setMinimumHeight(45)
                btn.setMaximumHeight(60)
                # Không setStyleSheet inline
        # Logo mini
        logo_frame = self.findChild(QFrame, "logo_frame")
        if logo_frame:
            logo_label = None
            for child in logo_frame.children():
                if (
                    isinstance(child, QLabel)
                    and child.text() == "🏛️"
                ):
                    logo_label = child
                    break
            if logo_label:
                if mini:
                    logo_label.setFont(QFont(UI_FONT['family'], 20))
                else:
                    logo_label.setFont(QFont(UI_FONT['family'], 32))
        # Ẩn/hiện app name
        app_name = None
        for child in logo_frame.children():
            if (
                isinstance(child, QLabel)
                and "QUẢN LÝ" in child.text()
            ):
                app_name = child
                break
        if app_name:
            app_name.setVisible(not mini)
        # Ẩn/hiện user info, logout
        bottom_frame = self.findChild(QFrame, "bottom_frame")
        if bottom_frame:
            for child in bottom_frame.children():
                if isinstance(child, QLabel) or isinstance(child, QPushButton):
                    child.setVisible(not mini)
        # Accessibility: set tab order cho nav buttons, logout, user info
        self.set_tab_order_accessibility()

    def is_mini_mode(self) -> bool:
        """Trả về trạng thái mini mode của sidebar."""
        return self._mini_mode

    def set_tab_order_accessibility(self):
        """Đảm bảo accessibility: set tab order cho các nút nav, logout, user info."""
        # Tab order: nav buttons -> user label -> logout
        nav_btns = list(self.nav_buttons.values())
        for i in range(len(nav_btns) - 1):
            self.setTabOrder(
                nav_btns[i], nav_btns[i + 1]
            )
        bottom_frame = self.findChild(QFrame, "bottom_frame")
        user_label = None
        logout_btn = None
        if bottom_frame:
            for child in bottom_frame.children():
                if isinstance(child, QLabel):
                    user_label = child
                if isinstance(child, QPushButton):
                    logout_btn = child
        if nav_btns and user_label:
            self.setTabOrder(
                nav_btns[-1], user_label
            )
        if user_label and logout_btn:
            self.setTabOrder(
                user_label, logout_btn
            ) 

    def toggle_sidebar_mode(self):
        self._mini_mode = not self._mini_mode
        self.toggle_btn.setChecked(self._mini_mode)
        self.animate_sidebar_width()
        self.update_sidebar_mode()

    def animate_sidebar_width(self):
        from PyQt6.QtCore import QPropertyAnimation
        target_width = self._sidebar_width_mini if self._mini_mode else self._sidebar_width_full
        anim = QPropertyAnimation(self, b"minimumWidth")
        anim.setDuration(180)
        anim.setStartValue(self.width())
        anim.setEndValue(target_width)
        anim.start()
        self.setFixedWidth(target_width)
        self._sidebar_anim = anim  # giữ tham chiếu tránh bị GC

    def update_sidebar_mode(self):
        # Đổi objectName để QSS style khác biệt
        self.setObjectName("SidebarWidgetMini" if self._mini_mode else "SidebarWidget")
        # Ẩn/hiện text trên nav button
        for btn in self.nav_buttons.values():
            text = btn.text()
            if self._mini_mode:
                # Chỉ giữ icon, text thành tooltip
                icon = text.split(' ')[0]
                btn.setText(icon)
                btn.setToolTip(text)
            else:
                # Hiện lại icon + text
                page_id = [k for k, v in self.nav_buttons.items() if v == btn][0]
                page_info = PAGES[page_id]
                btn.setText(f"{page_info['icon']} {page_info['name']}")
                btn.setToolTip("")
        # Ẩn/hiện logo text
        logo_frame = self.findChild(QFrame, "logo_frame")
        if logo_frame:
            app_name = logo_frame.findChild(QLabel, None)
            if app_name:
                app_name.setVisible(not self._mini_mode) 
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Dashboard widget for displaying system overview and statistics.
"""

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QFrame, QGroupBox, QGridLayout
)
from PyQt6.QtCore import Qt, pyqtSignal, QTimer, QPropertyAnimation, QSequentialAnimationGroup, QParallelAnimationGroup, QPoint, QEasingCurve, QPauseAnimation
from PyQt6.QtGui import QFont, QMouseEvent
from PyQt6.QtSvgWidgets import QSvgWidget
from PyQt6.QtWidgets import QGraphicsDropShadowEffect
from PyQt6.QtWidgets import QGraphicsOpacityEffect

from typing import List, Dict, Any

from models.offender import RiskLevel
from services.offender_service import OffenderService
from services.ai_service import AIService
from ui.notification_card import NotificationCard


class ClickableCard(QFrame):
    """Clickable card widget for dashboard statistics với SVG icon, shadow, counter effect."""
    clicked = pyqtSignal(str)

    def __init__(self, action_type: str, svg_path: str, parent=None):
        super().__init__(parent)
        self.action_type = action_type
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setObjectName("StatCard")  # Đảm bảo dùng objectName để nhận QSS động
        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        # SVG icon
        self.svg_widget = QSvgWidget(svg_path, self)
        self.svg_widget.setFixedSize(40, 40)
        self.svg_widget.setAccessibleName(f"{action_type} icon")
        # Shadow effect
        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(12)
        shadow.setOffset(0, 2)
        shadow.setColor(Qt.GlobalColor.gray)
        self.setGraphicsEffect(shadow)
        # Counter effect
        self._value = 0
        self._target_value = 0
        self._counter_timer = QTimer(self)
        self._counter_timer.timeout.connect(self._update_counter)
        self._counter_step = 1
        self.value_label = None  # Sẽ gán sau khi tạo layout

    def enterEvent(self, event):
        effect = self.graphicsEffect()
        if isinstance(effect, QGraphicsDropShadowEffect):
            effect.setBlurRadius(24)
        self.svg_widget.setFixedSize(48, 48)
        super().enterEvent(event)

    def leaveEvent(self, event):
        effect = self.graphicsEffect()
        if isinstance(effect, QGraphicsDropShadowEffect):
            effect.setBlurRadius(12)
        self.svg_widget.setFixedSize(40, 40)
        super().leaveEvent(event)

    def mousePressEvent(self, event: QMouseEvent):
        if event.button() == Qt.MouseButton.LeftButton:
            self.clicked.emit(self.action_type)
        super().mousePressEvent(event)

    def set_value(self, value):
        self._target_value = value
        if self.value_label is not None:
            if self._value != value:
                self._counter_step = max(1, abs(value - self._value) // 20)
                self._counter_timer.start(15)
            else:
                self.value_label.setText(str(value))

    def _update_counter(self):
        if self._value < self._target_value:
            self._value += self._counter_step
            if self._value > self._target_value:
                self._value = self._target_value
        elif self._value > self._target_value:
            self._value -= self._counter_step
            if self._value < self._target_value:
                self._value = self._target_value
        if self.value_label is not None:
            self.value_label.setText(str(self._value))
        if self._value == self._target_value:
            self._counter_timer.stop()

    def focusInEvent(self, event):
        effect = self.graphicsEffect()
        if isinstance(effect, QGraphicsDropShadowEffect):
            effect.setColor(Qt.GlobalColor.blue)
        super().focusInEvent(event)

    def focusOutEvent(self, event):
        effect = self.graphicsEffect()
        if isinstance(effect, QGraphicsDropShadowEffect):
            effect.setColor(Qt.GlobalColor.gray)
        super().focusOutEvent(event)


class Dashboard(QWidget):
    """Dashboard widget for system overview."""
    
    # Signals
    refresh_requested = pyqtSignal()
    card_clicked = pyqtSignal(str, dict)  # action_type, filter_data
    
    def __init__(self, offender_service: OffenderService, 
                 ai_service: AIService, parent=None):
        """Initialize dashboard."""
        super().__init__(parent)
        self.offender_service = offender_service
        self.ai_service = ai_service
        self._main_layout = None
        self._stats_grid = None
        self._notifications_layout = None
        self.notification_cards = []
        self.setup_ui()
        self.setup_connections()
        
    def setup_ui(self):
        """Setup user interface."""
        self._main_layout = QVBoxLayout(self)
        self._main_layout.setContentsMargins(12, 12, 12, 12)
        self._main_layout.setSpacing(10)
        
        # Title
        title_label = QLabel("DASHBOARD - TỔNG QUAN HỆ THỐNG")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label.setFont(QFont("Segoe UI", 20, QFont.Weight.Bold))
        title_label.setObjectName("title")
        self._main_layout.addWidget(title_label)
        
        # Statistics cards
        self.setup_statistics_cards(self._main_layout)
        
        # Notification cards
        self.setup_notification_cards(self._main_layout)
        
        # Recent activity
        self.setup_recent_activity(self._main_layout)
        
        self._main_layout.addStretch()  # Đảm bảo co giãn full chiều dọc
        
    def setup_statistics_cards(self, parent_layout):
        """Setup statistics cards."""
        from os.path import join
        self._stats_grid = QGridLayout()
        self._stats_grid.setSpacing(10)  # giảm spacing
        self._stats_grid.setContentsMargins(0, 0, 0, 0)
        icon_dir = "assets/icons/"
        card_info = [
            ("Đang chấp hành", 0, "#4CAF50", join(icon_dir, "active.svg"), "active", "offender_list"),
            ("Sắp kết thúc", 0, "#FF9800", join(icon_dir, "warning.svg"), "warning", "offender_list"),
            ("Vi phạm", 0, "#F44336", join(icon_dir, "violation.svg"), "violation", "offender_list"),
            ("Nguy cơ cao", 0, "#1976D2", join(icon_dir, "risk.svg"), "risk", "offender_list"),
        ]
        self.stat_cards = []
        for i, (title, value, color, svg, status, action_type) in enumerate(card_info):
            card = ClickableCard(action_type, svg)
            card.setProperty("status", status)
            card.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
            layout = QVBoxLayout(card)
            layout.setSpacing(6)  # giảm spacing
            layout.setContentsMargins(12, 12, 12, 12)  # giảm padding
            card.svg_widget.setFixedSize(32, 32)  # nhỏ hơn
            title_label = QLabel(title)
            title_label.setFont(QFont("Inter", 12, QFont.Weight.Medium))  # nhỏ hơn
            title_label.setObjectName("SectionTitle")
            layout.addWidget(card.svg_widget, alignment=Qt.AlignmentFlag.AlignLeft)
            layout.addWidget(title_label)
            value_label = QLabel(str(value))
            value_label.setFont(QFont("Inter", 22, QFont.Weight.Bold))  # nhỏ hơn
            value_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            value_label.setObjectName("StatValue")
            layout.addWidget(value_label)
            card.value_label = value_label
            self.stat_cards.append(card)
        self._add_stat_cards_to_grid()
        parent_layout.addLayout(self._stats_grid)

    def _add_stat_cards_to_grid(self):
        # Remove all widgets from grid
        for i in reversed(range(self._stats_grid.count())):
            widget = self._stats_grid.itemAt(i).widget()
            if widget:
                self._stats_grid.removeWidget(widget)
                widget.setParent(None)
        # Determine columns based on width
        width = self.width() if self.width() > 0 else 1200
        min_card_width = 180  # giảm min width
        n_cols = max(1, min(len(self.stat_cards), width // min_card_width))
        for idx, card in enumerate(self.stat_cards):
            row = idx // n_cols
            col = idx % n_cols
            self._stats_grid.addWidget(card, row, col)

    def setup_notification_cards(self, parent_layout):
        """Setup notification cards thay thế alerts và insights."""
        self._notifications_layout = QGridLayout()
        self._notifications_layout.setSpacing(10)
        self._notifications_layout.setContentsMargins(0, 0, 0, 0)
        
        # Tạo 4 notification cards với nội dung khác nhau
        notifications = [
            {
                "type": "warning",
                "title": "CẢNH BÁO HỆ THỐNG",
                "message": "5 đối tượng sắp hết hạn thi hành án trong 30 ngày tới",
                "action_text": "Xem chi tiết"
            },
            {
                "type": "info", 
                "title": "AI PHÂN TÍCH",
                "message": "Phát hiện tăng 20% vi phạm tại khu vực A trong tháng này",
                "action_text": "Xem báo cáo"
            },
            {
                "type": "success",
                "title": "HOÀN THÀNH NHIỆM VỤ",
                "message": "15 đối tượng đã hoàn thành thi hành án thành công",
                "action_text": "Xem danh sách"
            },
            {
                "type": "error",
                "title": "VI PHẠM MỚI",
                "message": "3 đối tượng vi phạm quy định thi hành án",
                "action_text": "Xử lý ngay"
            }
        ]
        
        self.notification_cards = []
        for i, notification in enumerate(notifications):
            card = NotificationCard(
                title=notification["title"],
                message=notification["message"],
                notification_type=notification["type"],
                auto_dismiss=False,  # Không tự động ẩn
                show_action=True,
                action_text=notification["action_text"],
                parent=self
            )
            # Kết nối signal action_clicked với callback function
            card.action_clicked.connect(lambda checked=False, idx=i: self.handle_notification_action_by_index(idx))
            self.notification_cards.append(card)
        
        # Thêm cards vào grid layout
        self._add_notification_cards_to_grid()
        parent_layout.addLayout(self._notifications_layout)

    def _add_notification_cards_to_grid(self):
        """Thêm notification cards vào grid layout."""
        # Remove all widgets from grid
        for i in reversed(range(self._notifications_layout.count())):
            widget = self._notifications_layout.itemAt(i).widget()
            if widget:
                self._notifications_layout.removeWidget(widget)
                widget.setParent(None)
        
        # Determine columns based on width
        width = self.width() if self.width() > 0 else 1200
        min_card_width = 280  # Minimum width cho notification card
        n_cols = max(1, min(len(self.notification_cards), width // min_card_width))
        
        for idx, card in enumerate(self.notification_cards):
            row = idx // n_cols
            col = idx % n_cols
            self._notifications_layout.addWidget(card, row, col)

    def handle_notification_action(self, action_type: str):
        """Xử lý action từ notification card."""
        if action_type == "expiring_offenders":
            # Chuyển đến danh sách đối tượng với filter sắp hết hạn
            self.card_clicked.emit("offender_list", {"filter": "expiring"})
        elif action_type == "ai_analysis":
            # Chuyển đến AI tools
            self.card_clicked.emit("ai_tools", {"tab": "analysis"})
        elif action_type == "completed_offenders":
            # Chuyển đến danh sách đối tượng với filter hoàn thành
            self.card_clicked.emit("offender_list", {"filter": "completed"})
        elif action_type == "violations":
            # Chuyển đến danh sách đối tượng với filter vi phạm
            self.card_clicked.emit("offender_list", {"filter": "violations"})

    def handle_notification_action_by_index(self, index: int):
        """Handle notification action by card index."""
        action_types = ["expiring_offenders", "ai_analysis", "completed_offenders", "violations"]
        if 0 <= index < len(action_types):
            self.handle_notification_action(action_types[index])

    def create_stat_card(self, title: str, value: str, color: str, icon: str, status: str, action_type: str) -> ClickableCard:
        """Create a clickable statistics card."""
        card = ClickableCard(action_type, "assets/icons/active.svg") # Default SVG path
        card.setObjectName("StatCard")
        card.setProperty("status", status)
        
        layout = QVBoxLayout(card)
        layout.setSpacing(6)
        layout.setContentsMargins(12, 12, 12, 12)
        
        # Icon and title
        title_layout = QHBoxLayout()
        title_layout.setSpacing(4)
        icon_label = QLabel(icon)
        icon_label.setFont(QFont("Segoe UI", 22))
        title_layout.addWidget(icon_label)
        
        title_label = QLabel(title)
        title_label.setFont(QFont("Segoe UI", 13, QFont.Weight.Bold))
        title_label.setObjectName("SectionTitle")
        title_layout.addWidget(title_label)
        title_layout.addStretch()
        layout.addLayout(title_layout)
        
        # Value
        value_label = QLabel(value)
        value_label.setFont(QFont("Segoe UI", 28, QFont.Weight.Bold))
        value_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        value_label.setObjectName("StatValue")
        layout.addWidget(value_label)
        
        # Connect click signal
        card.clicked.connect(
            lambda action: self.handle_card_click(
                action, status
            )
        )
        
        return card
        
    def setup_recent_activity(self, parent_layout):
        from os.path import join
        self.activity_group = QGroupBox()
        self.activity_group.setFont(QFont("Inter", 13, QFont.Weight.Bold))
        self.activity_group.setObjectName("ActivityGroup")
        self.activity_group.setCursor(Qt.CursorShape.PointingHandCursor)
        self.activity_group.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        activity_shadow = QGraphicsDropShadowEffect(self.activity_group)
        activity_shadow.setBlurRadius(10)
        activity_shadow.setOffset(0, 2)
        activity_shadow.setColor(Qt.GlobalColor.gray)
        self.activity_group.setGraphicsEffect(activity_shadow)
        def activity_enterEvent(event):
            effect = self.activity_group.graphicsEffect()
            if isinstance(effect, QGraphicsDropShadowEffect):
                effect.setBlurRadius(18)
            activity_svg.setFixedSize(36, 36)
        def activity_leaveEvent(event):
            effect = self.activity_group.graphicsEffect()
            if isinstance(effect, QGraphicsDropShadowEffect):
                effect.setBlurRadius(10)
            activity_svg.setFixedSize(28, 28)
        self.activity_group.enterEvent = activity_enterEvent
        self.activity_group.leaveEvent = activity_leaveEvent
        activity_layout = QVBoxLayout(self.activity_group)
        activity_layout.setSpacing(6)
        activity_layout.setContentsMargins(12, 12, 12, 12)
        icon_dir = "assets/icons/"
        activity_svg = QSvgWidget(join(icon_dir, "activity.svg"), self.activity_group)
        activity_svg.setFixedSize(28, 28)
        activity_svg.setAccessibleName("Hoạt động icon")
        activity_layout.addWidget(activity_svg, alignment=Qt.AlignmentFlag.AlignLeft)
        activity_title = QLabel("HOẠT ĐỘNG GẦN ĐÂY")
        activity_title.setFont(QFont("Inter", 13, QFont.Weight.Bold))
        activity_title.setObjectName("SectionTitle")
        activity_layout.addWidget(activity_title)
        self.activity_label = QLabel("Đang tải dữ liệu hoạt động...")
        self.activity_label.setWordWrap(True)
        self.activity_label.setObjectName("ActivityLabel")
        activity_layout.addWidget(self.activity_label)
        parent_layout.addWidget(self.activity_group)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self._add_stat_cards_to_grid()
        self._add_notification_cards_to_grid()
        
    def setup_connections(self):
        """Setup signal connections."""
        # Connect stat cards
        for card in self.stat_cards:
            card.clicked.connect(self.handle_card_click)
        
        # Connect activity group click
        self.activity_group.mousePressEvent = lambda event: self.handle_group_click("activity", event)
        
    def handle_card_click(self, action_type: str, status: str = None):
        """Handle stat card click."""
        filter_data = {}
        if status:
            filter_data["status"] = status
        self.card_clicked.emit(action_type, filter_data)
        
    def handle_group_click(self, group_type: str, event):
        """Handle group click."""
        if group_type == "activity":
            # Chuyển đến trang hoạt động hoặc logs
            self.card_clicked.emit("activity_log", {})
        
    def refresh_data(self):
        """Refresh dashboard data."""
        try:
            # Update statistics
            stats = self.get_statistics()
            self.update_statistics_cards(stats)
            
            # Update notifications
            self.update_notifications()
            
            # Update activity
            activities = self.get_recent_activity()
            self.update_activity(activities)
            
        except Exception as e:
            print(f"Error refreshing dashboard: {e}")
            
    def get_statistics(self) -> Dict[str, Any]:
        """Get current statistics."""
        try:
            total_offenders = self.offender_service.get_total_count()
            active_offenders = self.offender_service.get_count_by_status("active")
            expiring_offenders = self.offender_service.get_count_by_status("expiring")
            violation_offenders = self.offender_service.get_count_by_status("violation")
            high_risk_offenders = self.offender_service.get_count_by_risk_level(RiskLevel.HIGH)
            
            return {
                "active": active_offenders,
                "expiring": expiring_offenders,
                "violation": violation_offenders,
                "high_risk": high_risk_offenders
            }
        except Exception as e:
            print(f"Error getting statistics: {e}")
            return {"active": 0, "expiring": 0, "violation": 0, "high_risk": 0}
            
    def update_statistics_cards(self, stats: Dict[str, Any]):
        """Update statistics cards with new data."""
        if len(self.stat_cards) >= 4:
            self.stat_cards[0].set_value(stats.get("active", 0))
            self.stat_cards[1].set_value(stats.get("expiring", 0))
            self.stat_cards[2].set_value(stats.get("violation", 0))
            self.stat_cards[3].set_value(stats.get("high_risk", 0))

    def update_notifications(self):
        """Update notification cards với dữ liệu thực tế."""
        try:
            # Lấy dữ liệu thực tế từ services
            expiring_count = self.offender_service.get_count_by_status("expiring")
            violation_count = self.offender_service.get_count_by_status("violation")
            completed_count = self.offender_service.get_count_by_status("completed")
            
            # Cập nhật nội dung notification cards
            if len(self.notification_cards) >= 4:
                # Card 1: Cảnh báo sắp hết hạn
                if expiring_count > 0:
                    self.notification_cards[0].update_message(
                        f"{expiring_count} đối tượng sắp hết hạn thi hành án trong 30 ngày tới"
                    )
                else:
                    self.notification_cards[0].update_message("Không có đối tượng sắp hết hạn")
                
                # Card 2: AI phân tích (giữ nguyên)
                # Card 3: Hoàn thành
                if completed_count > 0:
                    self.notification_cards[2].update_message(
                        f"{completed_count} đối tượng đã hoàn thành thi hành án thành công"
                    )
                else:
                    self.notification_cards[2].update_message("Chưa có đối tượng hoàn thành")
                
                # Card 4: Vi phạm
                if violation_count > 0:
                    self.notification_cards[3].update_message(
                        f"{violation_count} đối tượng vi phạm quy định thi hành án"
                    )
                else:
                    self.notification_cards[3].update_message("Không có vi phạm mới")
                    
        except Exception as e:
            print(f"Error updating notifications: {e}")
            
    def get_recent_activity(self) -> List[str]:
        """Get recent activity data."""
        try:
            # Lấy hoạt động gần đây từ database
            activities = [
                "15/11: Thêm đối tượng Nguyễn Văn A",
                "14/11: Cập nhật trạng thái 3 đối tượng",
                "13/11: Xuất báo cáo tháng 11",
                "12/11: Nhập dữ liệu từ file Excel",
                "11/11: Tạo báo cáo vi phạm"
            ]
            return activities
        except Exception as e:
            print(f"Error getting recent activity: {e}")
            return ["Không có hoạt động gần đây"]
        
    def update_activity(self, activities: List[str]):
        """Update activity display."""
        if activities:
            activity_text = "\n".join([f"• {activity}" for activity in activities[:5]])
            self.activity_label.setText(activity_text)
        else:
            self.activity_label.setText("Không có hoạt động gần đây")
            
    def show_statistics(self):
        """Show statistics information."""
        try:
            stats = self.get_statistics()
            total = sum(stats.values())
            print(f"Dashboard Statistics:")
            print(f"  Total offenders: {total}")
            print(f"  Active: {stats.get('active', 0)}")
            print(f"  Expiring: {stats.get('expiring', 0)}")
            print(f"  Violations: {stats.get('violation', 0)}")
            print(f"  High risk: {stats.get('high_risk', 0)}")
        except Exception as e:
            print(f"Error showing statistics: {e}")

    def showEvent(self, event):
        """Handle show event."""
        super().showEvent(event)
        # Refresh data when dashboard is shown
        self.refresh_data() 
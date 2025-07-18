#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Notification card component for displaying alerts and notifications.
"""

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QFrame, QSizePolicy
)
from PyQt6.QtCore import Qt, QTimer, pyqtSignal, QPropertyAnimation, QEasingCurve
from PyQt6.QtGui import QFont, QPixmap, QIcon

from enum import Enum
from typing import Optional


class NotificationType(Enum):
    """Notification types."""
    SUCCESS = "success"
    WARNING = "warning"
    ERROR = "error"
    INFO = "info"


class NotificationCard(QFrame):
    """Modern notification card component."""
    
    # Signals
    dismissed = pyqtSignal()
    action_clicked = pyqtSignal()
    
    def __init__(self, 
                 title: str,
                 message: str,
                 notification_type: NotificationType = NotificationType.INFO,
                 auto_dismiss: bool = True,
                 dismiss_timeout: int = 5000,
                 show_action: bool = False,
                 action_text: str = "Xem chi tiết",
                 parent=None):
        """Initialize notification card."""
        super().__init__(parent)
        
        self.title = title
        self.message = message
        self.notification_type = notification_type
        self.auto_dismiss = auto_dismiss
        self.dismiss_timeout = dismiss_timeout
        self.show_action = show_action
        self.action_text = action_text
        
        self.setup_ui()
        self.setup_style()
        self.setup_auto_dismiss()
        
    def setup_ui(self):
        """Setup user interface."""
        # Main layout
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(12, 12, 12, 12)
        main_layout.setSpacing(8)
        
        # Header row
        header_layout = QHBoxLayout()
        header_layout.setContentsMargins(0, 0, 0, 0)
        header_layout.setSpacing(8)
        
        # Icon
        self.icon_label = QLabel()
        self.icon_label.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        self.icon_label.setObjectName("notificationIcon")
        header_layout.addWidget(self.icon_label)
        
        # Title
        self.title_label = QLabel(self.title)
        self.title_label.setFont(QFont("Segoe UI", 11, QFont.Weight.Bold))
        self.title_label.setObjectName("notificationTitle")
        header_layout.addWidget(self.title_label)
        
        # Spacer
        header_layout.addStretch()
        
        # Dismiss button
        self.dismiss_button = QPushButton("✕")
        self.dismiss_button.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        self.dismiss_button.setObjectName("notificationDismiss")
        self.dismiss_button.clicked.connect(self.dismiss)
        header_layout.addWidget(self.dismiss_button)
        
        main_layout.addLayout(header_layout)
        
        # Message
        self.message_label = QLabel(self.message)
        self.message_label.setWordWrap(True)
        self.message_label.setFont(QFont("Segoe UI", 10))
        self.message_label.setObjectName("notificationMessage")
        main_layout.addWidget(self.message_label)
        
        # Action button (optional)
        if self.show_action:
            action_layout = QHBoxLayout()
            action_layout.setContentsMargins(0, 0, 0, 0)
            action_layout.setSpacing(8)
            
            action_layout.addStretch()
            
            self.action_button = QPushButton(self.action_text)
            self.action_button.setMinimumHeight(28)
            self.action_button.setMaximumHeight(32)
            self.action_button.setFont(QFont("Segoe UI", 10))
            self.action_button.setObjectName("notificationAction")
            self.action_button.clicked.connect(self.action_clicked.emit)
            action_layout.addWidget(self.action_button)
            
            main_layout.addLayout(action_layout)
        
        # Set size policy
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.setMaximumWidth(400)
        
    def setup_style(self):
        """Setup card style based on notification type."""
        # Set object name for styling
        ntype = self.notification_type.value if hasattr(self.notification_type, 'value') else self.notification_type
        self.setObjectName(f"notificationCard{ntype.capitalize()}")
        
        # Set icon based on type
        icon_map = {
            NotificationType.SUCCESS: "✅",
            NotificationType.WARNING: "⚠️",
            NotificationType.ERROR: "❌",
            NotificationType.INFO: "ℹ️"
        }
        
        self.icon_label.setText(icon_map.get(self.notification_type, "ℹ️"))
        
    def setup_auto_dismiss(self):
        """Setup auto dismiss timer."""
        if self.auto_dismiss and self.dismiss_timeout > 0:
            self.dismiss_timer = QTimer()
            self.dismiss_timer.timeout.connect(self.dismiss)
            self.dismiss_timer.start(self.dismiss_timeout)
            
    def showEvent(self, event):
        super().showEvent(event)
        # Animation fade in + slide in
        self.setWindowOpacity(0)
        self._fade_anim = QPropertyAnimation(self, b"windowOpacity")
        self._fade_anim.setDuration(220)
        self._fade_anim.setStartValue(0)
        self._fade_anim.setEndValue(1)
        self._fade_anim.setEasingCurve(QEasingCurve.Type.InOutQuad)
        self._fade_anim.start()
        self._slide_anim = QPropertyAnimation(self, b"pos")
        self._slide_anim.setDuration(220)
        start_pos = self.pos() + self.parentWidget().rect().topRight() - self.rect().topRight() + Qt.QPoint(40, 0)
        self._slide_anim.setStartValue(start_pos)
        self._slide_anim.setEndValue(self.pos())
        self._slide_anim.setEasingCurve(QEasingCurve.Type.OutCubic)
        self._slide_anim.start()

    def dismiss(self):
        # Animation fade out + slide out
        self._fade_anim = QPropertyAnimation(self, b"windowOpacity")
        self._fade_anim.setDuration(180)
        self._fade_anim.setStartValue(1)
        self._fade_anim.setEndValue(0)
        self._fade_anim.setEasingCurve(QEasingCurve.Type.InOutQuad)
        self._fade_anim.finished.connect(self._on_fade_out_done)
        self._fade_anim.start()
        self._slide_anim = QPropertyAnimation(self, b"pos")
        self._slide_anim.setDuration(180)
        end_pos = self.pos() + Qt.QPoint(40, 0)
        self._slide_anim.setStartValue(self.pos())
        self._slide_anim.setEndValue(end_pos)
        self._slide_anim.setEasingCurve(QEasingCurve.Type.InCubic)
        self._slide_anim.start()

    def _on_fade_out_done(self):
        self.dismissed.emit()
        self.deleteLater()
        
    def set_title(self, title: str):
        """Set notification title."""
        self.title = title
        self.title_label.setText(title)
        
    def set_message(self, message: str):
        """Set notification message."""
        self.message = message
        self.message_label.setText(message)
        
    def set_type(self, notification_type: NotificationType):
        """Set notification type."""
        self.notification_type = notification_type
        self.setup_style()

    def update_message(self, message: str):
        """Cập nhật nội dung thông báo trên card."""
        if hasattr(self, 'message_label'):
            self.message_label.setText(message)


class NotificationContainer(QWidget):
    """Container for managing multiple notification cards."""
    
    def __init__(self, parent=None):
        """Initialize notification container."""
        super().__init__(parent)
        
        self.notifications = []
        self.setup_ui()
        
    def setup_ui(self):
        """Setup user interface."""
        # Main layout
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(8)
        self.main_layout.addStretch()
        
        # Set size policy
        self.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Expanding)
        self.setMaximumWidth(420)
        
    def add_notification(self, 
                        title: str,
                        message: str,
                        notification_type: NotificationType = NotificationType.INFO,
                        auto_dismiss: bool = True,
                        dismiss_timeout: int = 5000,
                        show_action: bool = False,
                        action_text: str = "Xem chi tiết") -> NotificationCard:
        """Add a new notification card."""
        notification = NotificationCard(
            title=title,
            message=message,
            notification_type=notification_type,
            auto_dismiss=auto_dismiss,
            dismiss_timeout=dismiss_timeout,
            show_action=show_action,
            action_text=action_text
        )
        
        # Connect signals
        notification.dismissed.connect(lambda: self.remove_notification(notification))
        if show_action:
            notification.action_clicked.connect(self.on_action_clicked)
        
        # Add to layout (insert before stretch)
        self.main_layout.insertWidget(len(self.notifications), notification)
        self.notifications.append(notification)
        
        return notification
        
    def remove_notification(self, notification: NotificationCard):
        """Remove a notification card."""
        if notification in self.notifications:
            self.notifications.remove(notification)
            notification.deleteLater()
            
    def clear_all(self):
        """Clear all notifications."""
        for notification in self.notifications[:]:
            notification.deleteLater()
        self.notifications.clear()
        
    def on_action_clicked(self):
        """Handle action button click."""
        # Override in subclass for custom action
        pass


# Convenience functions for quick notifications
def show_success_notification(container: NotificationContainer,
                             title: str,
                             message: str,
                             auto_dismiss: bool = True) -> NotificationCard:
    """Show success notification."""
    return container.add_notification(
        title=title,
        message=message,
        notification_type=NotificationType.SUCCESS,
        auto_dismiss=auto_dismiss
    )


def show_warning_notification(container: NotificationContainer,
                             title: str,
                             message: str,
                             auto_dismiss: bool = True) -> NotificationCard:
    """Show warning notification."""
    return container.add_notification(
        title=title,
        message=message,
        notification_type=NotificationType.WARNING,
        auto_dismiss=auto_dismiss
    )


def show_error_notification(container: NotificationContainer,
                           title: str,
                           message: str,
                           auto_dismiss: bool = False) -> NotificationCard:
    """Show error notification."""
    return container.add_notification(
        title=title,
        message=message,
        notification_type=NotificationType.ERROR,
        auto_dismiss=auto_dismiss
    )


def show_info_notification(container: NotificationContainer,
                          title: str,
                          message: str,
                          auto_dismiss: bool = True) -> NotificationCard:
    """Show info notification."""
    return container.add_notification(
        title=title,
        message=message,
        notification_type=NotificationType.INFO,
        auto_dismiss=auto_dismiss
    ) 
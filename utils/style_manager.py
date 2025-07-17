#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Style Manager - Quản lý style cho ứng dụng
"""

import os
from pathlib import Path
from PyQt6.QtWidgets import QApplication, QWidget
from PyQt6.QtCore import QFile, QTextStream, QIODevice
from PyQt6.QtGui import QFont, QPalette, QColor


class StyleManager:
    """Quản lý style: load QSS, áp dụng style động, hỗ trợ dark/light mode"""
    def __init__(self):
        self.current_theme = "light"

    def apply_global_styles(self, app, theme="light"):
        self.current_theme = theme
        qss_file = f"assets/styles/style.qss"
        try:
            with open(qss_file, "r", encoding="utf-8") as f:
                app.setStyleSheet(f.read())
        except Exception as e:
            print(f"Không thể load QSS: {e}")
        
        # Set global font
        font = QFont("Segoe UI", 10)
        app.setFont(font)
        
        # Set color palette
        self.set_color_palette(app)
        
    def apply_widget_styles(self, widget: QWidget) -> None:
        """Áp dụng style cho widget cụ thể"""
        # Có thể override style cho widget riêng lẻ
        pass
    
    def set_color_palette(self, app: QApplication) -> None:
        """Set color palette cho ứng dụng"""
        palette = QPalette()
        
        # Light theme colors
        if self.current_theme == "light":
            palette.setColor(QPalette.ColorRole.Window, QColor("#FFFFFF"))
            palette.setColor(QPalette.ColorRole.WindowText, QColor("#333333"))
            palette.setColor(QPalette.ColorRole.Base, QColor("#FFFFFF"))
            palette.setColor(QPalette.ColorRole.AlternateBase, QColor("#F5F5F5"))
            palette.setColor(QPalette.ColorRole.ToolTipBase, QColor("#FFFFFF"))
            palette.setColor(QPalette.ColorRole.ToolTipText, QColor("#333333"))
            palette.setColor(QPalette.ColorRole.Text, QColor("#333333"))
            palette.setColor(QPalette.ColorRole.Button, QColor("#0066CC"))
            palette.setColor(QPalette.ColorRole.ButtonText, QColor("#FFFFFF"))
            palette.setColor(QPalette.ColorRole.BrightText, QColor("#FFFFFF"))
            palette.setColor(QPalette.ColorRole.Link, QColor("#0066CC"))
            palette.setColor(QPalette.ColorRole.Highlight, QColor("#0066CC"))
            palette.setColor(QPalette.ColorRole.HighlightedText, QColor("#FFFFFF"))
        
        app.setPalette(palette)
    
    def get_default_stylesheet(self) -> str:
        """Trả về style mặc định nếu không load được file"""
        return """
        QWidget {
            font-family: "Segoe UI", "Arial", sans-serif;
            font-size: 13px;
        }
        
        QPushButton {
            background-color: #0066CC;
            color: white;
            border: none;
            border-radius: 8px;
            padding: 6px 12px;
            min-height: 32px;
            max-height: 40px;
        }
        
        QPushButton:hover {
            background-color: #dbe9f4;
            color: #0066CC;
        }
        
        QLineEdit, QComboBox {
            background-color: white;
            border: 1px solid #CCCCCC;
            border-radius: 6px;
            padding: 4px 8px;
            min-height: 20px;
        }
        
        QLineEdit:focus, QComboBox:focus {
            border: 1px solid #007ACC;
        }
        """
    
    def apply_drop_shadow(self, widget: QWidget) -> None:
        """Áp dụng drop shadow cho widget"""
        shadow_style = """
        QWidget {
            background-color: white;
            border: 1px solid #E0E0E0;
            border-radius: 8px;
        }
        """
        widget.setStyleSheet(shadow_style)
    
    def get_status_color(self, status: str) -> str:
        """Lấy màu theo trạng thái"""
        colors = {
            "active": "#4CAF50",      # Đang chấp hành
            "warning": "#FF9800",     # Sắp kết thúc
            "completed": "#9E9E9E",   # Hoàn thành
            "violation": "#F44336"    # Vi phạm
        }
        return colors.get(status.lower(), "#666666")
    
    def get_risk_color(self, risk_level: str) -> str:
        """Lấy màu theo mức độ nguy cơ"""
        colors = {
            "low": "#4CAF50",         # Thấp
            "medium": "#FF9800",      # Trung bình
            "high": "#F44336"         # Cao
        }
        return colors.get(risk_level.lower(), "#666666")
    
    def apply_status_style(self, widget: QWidget, status: str) -> None:
        """Áp dụng style theo trạng thái"""
        color = self.get_status_color(status)
        style = f"""
        QWidget {{
            background-color: {color};
            color: white;
            border-radius: 4px;
            padding: 4px 8px;
        }}
        """
        widget.setStyleSheet(style)
    
    def apply_risk_style(self, widget: QWidget, risk_level: str) -> None:
        """Áp dụng style theo mức độ nguy cơ"""
        color = self.get_risk_color(risk_level)
        style = f"""
        QWidget {{
            background-color: {color};
            color: white;
            border-radius: 4px;
            padding: 4px 8px;
        }}
        """
        widget.setStyleSheet(style)
    
    def reload_styles(self, app: QApplication) -> None:
        """Reload lại style"""
        self.apply_global_styles(app)
        print("✅ Đã reload style thành công")
    
    def switch_theme(self, app: QApplication, theme: str) -> None:
        """Chuyển đổi theme"""
        self.current_theme = theme
        self.apply_global_styles(app)
        print(f"✅ Đã chuyển sang theme: {theme}")


# Global instance
style_manager = StyleManager() 
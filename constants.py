#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Constants - Quản lý tất cả constants của dự án
"""

try:
    from PyQt6.QtGui import QFont
except ImportError:
    from PyQt6.QtWidgets import QFont

# ============================================================================
# APP CONFIGURATION
# ============================================================================
APP_NAME = "🏛️ Quản Lý Đối Tượng Thi Hành Án"
APP_VERSION = "1.0.0"
APP_AUTHOR = "Development Team"

# Window settings - Updated with new design
WINDOW_WIDTH = 1400
WINDOW_HEIGHT = 900
WINDOW_MIN_WIDTH = 1200
WINDOW_MIN_HEIGHT = 800
SIDEBAR_WIDTH = 280  # Chiều rộng sidebar

# ============================================================================
# COMPONENT SIZES
# ============================================================================
COMPONENT_SIZES = {
    'label_width': 170,
    'input_width': 280,
    'input_height': 30,
    'button_width': 90,
    'button_height': 30,
    'primary_button_width': 100,
    'primary_button_height': 30,
    'secondary_button_width': 90,
    'secondary_button_height': 30,
    'small_button_width': 70,
    'small_button_height': 30
}

# ============================================================================
# LAYOUT SPACING
# ============================================================================
LAYOUT_SPACING = {
    'main_margin': 15,
    'section_margin': 10,
    'item_spacing': 8,
    'group_spacing': 15,
    'form_spacing': 12
}

# ============================================================================
# DATABASE
# ============================================================================
DATABASE_PATH = "data/database.db"
BACKUP_PATH = "data/backups/"
EXPORT_PATH = "data/exports/"
LOG_PATH = "data/logs/"

# ============================================================================
# UI COLORS & STYLES - Updated with new design
# ============================================================================
# Primary colors
PRIMARY_COLOR = "#2563EB"      # Xanh dương chính
PRIMARY_DARK = "#1E40AF"       # Xanh dương đậm
PRIMARY_LIGHT = "#DBEAFE"      # Xanh dương nhạt

# Secondary colors
SECONDARY_COLOR = "#64748B"    # Xám xanh
ACCENT_COLOR = "#10B981"       # Xanh lá (success)
WARNING_COLOR = "#F59E0B"      # Cam (warning)
ERROR_COLOR = "#EF4444"        # Đỏ (error)
INFO_COLOR = "#3B82F6"         # Xanh (info)

# Background colors
BACKGROUND_COLOR = "#F8FAFC"   # Nền chính
CARD_BACKGROUND = "#FFFFFF"    # Nền thẻ
BORDER_COLOR = "#E2E8F0"       # Viền

# Status colors - Updated
STATUS_ACTIVE = "#10B981"      # Đang chấp hành
STATUS_WARNING = "#F59E0B"     # Sắp kết thúc
STATUS_COMPLETED = "#6B7280"   # Hoàn thành
STATUS_VIOLATION = "#EF4444"    # Vi phạm
STATUS_SUSPENDED = "#8B5CF6"    # Hoãn thi hành
STATUS_CONDITIONAL = "#06B6D4"  # Tha tù có điều kiện

# Risk level colors
RISK_LOW = "#10B981"           # Thấp
RISK_MEDIUM = "#F59E0B"        # Trung bình
RISK_HIGH = "#EF4444"          # Cao

# ============================================================================
# STYLE RULES & STANDARDS
# ============================================================================
# Layout standards
UI_LAYOUT = {
    'contents_margins': (10, 10, 10, 10),  # (left, top, right, bottom)
    'spacing': 10,  # Spacing giữa các widget
    'form_spacing': 10,  # Spacing trong form
    'section_spacing': 10,  # Spacing giữa các section
    'input_min_width': 140,  # Chiều rộng tối thiểu cho input
    'input_min_height': 30,  # Chiều cao tối thiểu cho input
    'button_min_width': 100,  # Chiều rộng tối thiểu cho button
    'button_min_height': 30  # Chiều cao tối thiểu cho button
}

# Font standards
UI_FONT = {
    'family': 'Segoe UI',
    'size': 13,                            # Font size chuẩn
    'size_small': 11,                      # Font size nhỏ
    'size_normal': 14,  # Font size bình thường
    'size_large': 15,                      # Font size lớn
    'size_title': 18,                      # Font size tiêu đề
    'weight_normal': QFont.Weight.Normal,  # Font weight bình thường
    'weight_bold': QFont.Weight.Bold,      # Font weight đậm
    'weight_light': QFont.Weight.Light     # Font weight nhẹ
}

# Button standards
UI_BUTTON = {
    'padding': '8px 16px',                 # Padding chuẩn
    'min_height': 36,                      # Chiều cao tối thiểu
    'max_height': 44,                      # Chiều cao tối đa
    'border_radius': 8,                    # Bo góc
    'hover_bg': '#dbe9f4',                 # Màu hover
    'hover_color': '#0066CC'               # Màu text hover
}

# Input standards
UI_INPUT = {
    'padding': '6px 12px',                  # Padding chuẩn
    'border_radius': 8,                    # Bo góc
    'border': '1.5px solid #ccc',            # Viền chuẩn
    'focus_border': '1.5px solid #007ACC'    # Viền khi focus
}

# Tab standards
UI_TAB = {
    'padding': '8px 16px',                 # Padding chuẩn
    'border': '1px solid #ccc',            # Viền chuẩn
    'selected_bg': 'white',                # Background khi selected
    'selected_font_weight': 'bold'         # Font weight khi selected
}

# QSS Style rules
UI_QSS = {
    # File QSS chính
    'main_file': 'assets/styles/style.qss',
    
    # Quy tắc cấm
    'forbidden': [
        'KHÔNG có file style.qss trong thư mục ui/',
        'KHÔNG dùng setStyleSheet() inline trong UI code',
        'KHÔNG gộp StyleManager vào file QSS',
        'KHÔNG có nhiều file QSS riêng lẻ'
    ],
    
    # Quy tắc bắt buộc
    'required': [
        'Dùng layout thay vì setGeometry()',
        'setContentsMargins(12, 12, 12, 12)',
        'setSpacing(10)',
        'Font-size: 13px',
        'QPushButton: padding 6px 12px, min-height 32px, max-height 40px',
        'QLineEdit/QComboBox: padding 4px 8px, border-radius 6px',
        'QPushButton:hover: background #dbe9f4',
        'QLineEdit:focus: border 1px solid #007ACC',
        'QTabWidget: tab padding 6px 12px, border 1px solid #ccc'
    ]
}

# Color scheme chuẩn
UI_COLORS = {
    'primary': '#0066CC',
    'secondary': '#424242',
    'success': '#4CAF50',
    'warning': '#FF9800',
    'error': '#F44336',
    'info': '#2196F3',
    
    # Status colors
    'status_active': '#4CAF50',      # Đang chấp hành
    'status_warning': '#FF9800',     # Sắp kết thúc
    'status_completed': '#9E9E9E',   # Hoàn thành
    'status_violation': '#F44336',   # Vi phạm
    
    # Risk colors
    'risk_low': '#4CAF50',          # Thấp
    'risk_medium': '#FF9800',       # Trung bình
    'risk_high': '#F44336'          # Cao
}

# ============================================================================
# FONTS
# ============================================================================
FONTS = {
    'family': 'Segoe UI',
    'size_small': 12,
    'size_normal': 14,
    'size_large': 16,
    'size_title': 24
}

# ============================================================================
# APP INFO
# ============================================================================
APP_INFO = {
    'name': APP_NAME,
    'version': APP_VERSION,
    'author': APP_AUTHOR,
    'organization': 'Công an tỉnh Hà Tĩnh'
}

# ============================================================================
# NAVIGATION PAGES
# ============================================================================
PAGES = {
    0: {"name": "Dashboard", "icon": "📊"},
    1: {"name": "Đối tượng", "icon": "👥"},
    2: {"name": "Danh sách", "icon": "📋"},
    3: {"name": "Báo cáo", "icon": "📈"},
    4: {"name": "AI Tools", "icon": "🤖"},
    5: {"name": "Cài đặt", "icon": "⚙️"}
}

# ============================================================================
# OFFENDER STATUS
# ============================================================================
OFFENDER_STATUS = {
    "ACTIVE": "Đang chấp hành",
    "WARNING": "Sắp kết thúc",
    "COMPLETED": "Hoàn thành",
    "VIOLATION": "Vi phạm",
    "SUSPENDED": "Hoãn thi hành",
    "CONDITIONAL": "Tha tù có điều kiện"
}

# ============================================================================
# OFFENDER TYPES
# ============================================================================
OFFENDER_TYPES = {
    "AN_TREO": "Án treo",
    "CAI_TAO": "Cải tạo",
    "TU_GIAM": "Tù giam",
    "TU_CHUNG_THAN": "Tù chung thân"
}

# ============================================================================
# RISK LEVELS
# ============================================================================
RISK_LEVELS = {
    "LOW": "Thấp",
    "MEDIUM": "Trung bình", 
    "HIGH": "Cao"
}

# ============================================================================
# REPORT TYPES
# ============================================================================
REPORT_TYPES = {
    "MONTHLY": "Báo cáo tháng",
    "QUARTERLY": "Báo cáo quý",
    "YEARLY": "Báo cáo năm",
    "VIOLATION": "Báo cáo vi phạm",
    "COMPLETION": "Báo cáo hoàn thành"
}

# ============================================================================
# DEFAULT VALUES
# ============================================================================
DEFAULT_USERNAME = "admin"
DEFAULT_PASSWORD = "admin"

# Sample data
SAMPLE_OFFENDERS = [
    {
        "id": 1,
        "so_hs": "40CE0625",
        "ho_ten": "Nguyễn Văn A",
        "ngay_sinh": "1990-05-15",
        "gioi_tinh": "Nam",
        "noi_cu_tru": "TDP 1, P. Bắc Hồng",
        "nghe_nghiep": "Nông dân",
        "toi_danh": "Trộm cắp tài sản",
        "loai_an": "Án treo",
        "ngay_bat_dau": "2025-06-01",
        "thoi_gian_thu_thach": 6,
        "duoc_giam": 1,
        "ngay_duoc_giam": "2025-09-02",
        "so_lan_giam": 1,
        "trang_thai": "Đang chấp hành",
        "nguy_co": "Trung bình"
    },
    {
        "id": 2,
        "so_hs": "41CG0626",
        "ho_ten": "Trần Thị B",
        "ngay_sinh": "1985-08-20",
        "gioi_tinh": "Nữ",
        "noi_cu_tru": "TDP 2, P. Nam Hồng",
        "nghe_nghiep": "Thợ may",
        "toi_danh": "Gây thương tích",
        "loai_an": "Cải tạo",
        "ngay_bat_dau": "2025-05-15",
        "thoi_gian_thu_thach": 12,
        "duoc_giam": 2,
        "ngay_duoc_giam": "2025-11-15",
        "so_lan_giam": 1,
        "trang_thai": "Sắp kết thúc",
        "nguy_co": "Cao"
    }
]

# ============================================================================
# MESSAGES
# ============================================================================
MESSAGES = {
    "LOGIN_SUCCESS": "✅ Đăng nhập thành công",
    "LOGIN_FAILED": "❌ Đăng nhập thất bại",
    "LOGOUT_SUCCESS": "✅ Đăng xuất thành công",
    "SAVE_SUCCESS": "✅ Lưu thành công",
    "DELETE_SUCCESS": "✅ Xóa thành công",
    "EXPORT_SUCCESS": "✅ Xuất file thành công",
    "ERROR_GENERAL": "❌ Có lỗi xảy ra",
    "WARNING_SERVICE": "⚠️ Service chưa được khởi tạo"
}

# ============================================================================
# FILE PATTERNS
# ============================================================================
FILE_PATTERNS = {
    "EXCEL": "*.xlsx",
    "PDF": "*.pdf",
    "BACKUP": "*.db",
    "LOG": "*.log"
}

# ============================================================================
# VALIDATION RULES
# ============================================================================
VALIDATION = {
    "MIN_PASSWORD_LENGTH": 6,
    "MAX_NAME_LENGTH": 100,
    "MIN_AGE": 14,
    "MAX_AGE": 100,
    "MIN_SENTENCE_MONTHS": 1,
    "MAX_SENTENCE_MONTHS": 60
}

# ============================================================================
# AI CONFIG
# ============================================================================
AI_CONFIG = {
    "ENABLED": True,
    "MODEL_PATH": "models/risk_predictor.pkl",
    "CONFIDENCE_THRESHOLD": 0.7,
    "MAX_PREDICTIONS": 100
}

# ============================================================================
# EXPORT CONFIG
# ============================================================================
EXPORT_CONFIG = {
    "EXCEL_TEMPLATE": "data/templates/report_template.xlsx",
    "PDF_TEMPLATE": "data/templates/report_template.pdf",
    "DEFAULT_FILENAME": "bao_cao_{date}",
    "MAX_FILE_SIZE": 10 * 1024 * 1024  # 10MB
}

# =========================================================================
# ICONS - Đường dẫn icon dùng cho UI
# =========================================================================
ICON_SAVE = "assets/save.png"
ICON_CANCEL = "assets/cancel.png"
ICON_CALENDAR = "assets/calendar.png"
ICON_DELETE = "assets/delete.png"
ICON_EDIT = "assets/edit.png"
ICON_INFO = "assets/info.png"
ICON_PRINT = "assets/print.png"
ICON_ARROW_DOWN = "assets/arrow_down.png" 

# =================== UI STYLE RULES ===================
# ĐÃ LOẠI BỎ HOÀN TOÀN border: 1px solid white VÀ MỌI BORDER TRẮNG THÔ TRONG 
# QGroupBox, QFrame, QWidget Ở FILE QSS.
# KHÔNG ĐƯỢC PHÉP DÙNG BORDER TRẮNG THÔ TRONG UI.
# TẤT CẢ STYLE BORDER, NỀN, BO GÓC PHẢI ĐƯỢC ĐỊNH NGHĨA ĐÚNG CHUẨN QSS VÀ 
# constants.py. 

# =================== DESIGN SYSTEM TOKENS ===================
# Color Palette
COLOR_PALETTE = {
    'primary': '#1e40af',
    'primary_light': '#3b82f6',
    'primary_dark': '#1e3a8a',
    'neutral_gray': '#64748b',
    'light_gray': '#f1f5f9',
    'white': '#ffffff',
    'dark_gray': '#334155',
    'error': '#dc2626',
    'warning': '#f59e0b',
    'success': '#16a34a',
    'info': '#0ea5e9',
    'purple': '#9333ea',
    # Status
    'active': '#10b981',
    'pending': '#f59e0b',
    'overdue': '#ef4444',
    'completed': '#6b7280',
    'special': '#8b5cf6',
}

# Typography
TYPOGRAPHY = {
    'font_family_primary': 'Inter, Segoe UI, Roboto, Arial, sans-serif',
    'font_family_secondary': 'SF Pro Display, Arial, sans-serif',
    'font_family_mono': 'JetBrains Mono, Consolas, monospace',
    'font_family_vn': 'Roboto, Noto Sans, Arial Unicode MS',
    'h1': {'size': 32, 'line_height': 40, 'weight': 700},
    'h2': {'size': 24, 'line_height': 32, 'weight': 700},
    'h3': {'size': 20, 'line_height': 28, 'weight': 600},
    'h4': {'size': 18, 'line_height': 24, 'weight': 600},
    'h5': {'size': 16, 'line_height': 20, 'weight': 600},
    'body_lg': {'size': 16, 'line_height': 24, 'weight': 400},
    'body_md': {'size': 14, 'line_height': 20, 'weight': 400},
    'body_sm': {'size': 12, 'line_height': 16, 'weight': 400},
    'caption': {'size': 11, 'line_height': 14, 'weight': 400},
    'font_weight_light': 300,
    'font_weight_regular': 400,
    'font_weight_medium': 500,
    'font_weight_semibold': 600,
    'font_weight_bold': 700,
}

# Spacing Scale (px)
SPACING = {
    'xs': 4,
    'sm': 8,
    'md': 16,
    'lg': 24,
    'xl': 32,
    '2xl': 48,
    '3xl': 64,
}

# Grid & Breakpoints
GRID = {
    'columns_desktop': 12,
    'columns_tablet': 8,
    'columns_mobile': 4,
    'gutter_desktop': 24,
    'gutter_tablet': 16,
    'gutter_mobile': 12,
    'container_xl': 1400,
    'container_lg': 1200,
    'container_md': 992,
    'container_sm': 768,
    'container_xs': '100%',
}
BREAKPOINTS = {
    'xs': 0,
    'sm': 576,
    'md': 768,
    'lg': 992,
    'xl': 1200,
    'xxl': 1400,
}

# Button Specs
BUTTON_SPECS = {
    'primary': {
        'bg': '#1e40af', 'color': '#fff', 'height': 40, 'padding': '12px 24px', 'radius': 8, 'font': 14, 'weight': 500
    },
    'secondary': {
        'bg': 'transparent', 'color': '#1e40af', 'border': '1px solid #1e40af', 'height': 40, 'padding': '12px 24px', 'radius': 8, 'font': 14, 'weight': 500
    },
    'danger': {
        'bg': '#dc2626', 'color': '#fff', 'height': 40, 'padding': '12px 24px', 'radius': 8, 'font': 14, 'weight': 500
    },
    'icon': {
        'size': 32, 'icon_size': 16, 'radius': 6
    }
}

# Input/Select Specs
INPUT_SPECS = {
    'height': 40, 'padding': '12px 16px', 'border': '1px solid #d1d5db', 'radius': 8, 'font': 14, 'focus_border': '2px solid #1e40af'
}

# Card Specs
CARD_SPECS = {
    'bg': '#fff', 'border': '1px solid #e5e7eb', 'radius': 12, 'padding': 24, 'shadow': '0 1px 3px rgba(0,0,0,0.1)'
}

# Modal Specs
MODAL_SPECS = {
    'bg': '#fff', 'radius': 16, 'padding': 32, 'shadow': '0 20px 25px rgba(0,0,0,0.15)', 'backdrop': 'rgba(0,0,0,0.5)'
}

# Alert Specs
ALERT_SPECS = {
    'radius': 8, 'padding': 16, 'border_left': '4px solid',
}

# Badge Specs
BADGE_SPECS = {
    'height': 24, 'padding': '4px 8px', 'radius': 12, 'font': 12, 'weight': 500
}

# Table Specs
TABLE_SPECS = {
    'header_bg': '#f8fafc', 'header_text': 12, 'header_weight': 600, 'header_padding': '12px 16px',
    'row_height': 48, 'row_padding': '12px 16px', 'cell_font': 14, 'cell_weight': 400, 'cell_padding': '12px 16px',
    'border': '1px solid #e5e7eb', 'row_border': '1px solid #f1f5f9',
}

# Status Icon Specs
STATUS_ICON_SPECS = {
    'size': 16,
}

# Progress Bar Specs
PROGRESS_BAR_SPECS = {
    'height': 8, 'radius': 4, 'bg': '#e5e7eb', 'progress': '#1e40af'
}

# Animation & Transition
ANIMATION = {
    'fast': 150,
    'normal': 300,
    'slow': 500,
    'easing': 'cubic-bezier(0.4, 0, 0.2, 1)'
}

# Header Specs (compact top bar)
HEADER_SPECS = {
    'min_height': 36,
    'padding': '4px 12px',
    'font_size': 14,
    'font_weight': 'bold',
    'background': '#F2F2F2',
    'border_bottom': '#E6E6E6',
}

 
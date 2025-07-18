#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Main window for the offender management system.
"""

from PyQt6.QtWidgets import (
    QMainWindow, QVBoxLayout, QStackedWidget, QStatusBar, QMessageBox,
    QWidget, QSizePolicy, QSplitter, QScrollArea
)
from PyQt6.QtCore import pyqtSignal, Qt
from PyQt6.QtGui import QKeySequence, QAction

from .header import HeaderWidget as Header
from .sidebar import SidebarWidget as Sidebar
from .dashboard import Dashboard
from .offender_form import OffenderForm
from .offender_list import OffenderList
from .reports import ReportsWidget as Reports
from .ai_tools import AIToolsWidget as AITools
from .settings import SettingsWidget as Settings

from services.offender_service import OffenderService
from services.user_service import UserService
from services.ai_service import AIService
from services.report_service import ReportService


class MainWindow(QMainWindow):
    """Main application window."""
    
    # Signals
    offender_updated = pyqtSignal()
    offender_deleted = pyqtSignal(int)
    
    def __init__(self, offender_service: OffenderService, 
                 user_service: UserService, ai_service: AIService, 
                 report_service: ReportService, parent=None):
        """Initialize main window."""
        super().__init__(parent)
        
        # Store services
        self.offender_service = offender_service
        self.user_service = user_service
        self.ai_service = ai_service
        self.report_service = report_service
        
        # Initialize UI
        self.setup_ui()
        self.setup_connections()
        self.setup_menu()
        self.setup_status_bar()
        
        # Show dashboard by default
        self.show_dashboard()
        
    def setup_ui(self):
        """Setup user interface."""
        # Window properties
        self.setWindowTitle("Hệ thống Quản lý Đối tượng Thi hành án")
        self.setMinimumSize(1200, 800)
        
        # Central widget
        central_widget = QWidget()
        central_widget.setSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding
        )
        self.setCentralWidget(central_widget)
        
        # Main layout
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # Header (sticky, luôn trên cùng)
        self.header = Header("admin")
        self.header.setObjectName("HeaderWidget")  # Để style sticky nếu cần
        main_layout.addWidget(self.header)
        
        # Content area dùng QSplitter để sidebar co giãn
        self.content_splitter = QSplitter()
        self.content_splitter.setOrientation(Qt.Orientation.Horizontal)
        self.content_splitter.setChildrenCollapsible(False)
        
        # Sidebar
        self.sidebar = Sidebar(self.on_sidebar_page_changed)
        self.sidebar.setMinimumWidth(180)
        self.sidebar.setMaximumWidth(400)
        self.sidebar.setSizePolicy(
            QSizePolicy.Policy.Preferred,
            QSizePolicy.Policy.Expanding
        )
        self.sidebar.setObjectName("SidebarWidget")  # Để style nếu cần
        self.content_splitter.addWidget(self.sidebar)
        
        # Main content scroll area
        self.stacked_widget = QStackedWidget()
        self.stacked_widget.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Expanding
        )
        main_scroll_area = QScrollArea()
        main_scroll_area.setWidgetResizable(True)
        main_scroll_area.setFrameShape(QScrollArea.Shape.NoFrame)
        main_scroll_area.setVerticalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAsNeeded
        )
        main_scroll_area.setHorizontalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAlwaysOff
        )
        main_scroll_area.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Expanding
        )
        main_scroll_area.setWidget(self.stacked_widget)
        main_scroll_area.setObjectName("MainContentScrollArea")
        self.content_splitter.addWidget(main_scroll_area)
        
        # Stretch: sidebar co giãn, nội dung chính co giãn tối đa
        self.content_splitter.setStretchFactor(0, 0)
        self.content_splitter.setStretchFactor(1, 1)
        
        main_layout.addWidget(self.content_splitter)
        
        # Initialize pages
        self.setup_pages()

        # Accessibility: set tab order cho sidebar, header, main content
        self.set_tab_order_accessibility()

    def set_tab_order_accessibility(self):
        """Đảm bảo accessibility: tab order cho sidebar, header, main content."""
        self.setTabOrder(self.sidebar, self.header)
        self.setTabOrder(self.header, self.stacked_widget)
        
    def setup_pages(self):
        """Setup all application pages."""
        # Dashboard
        self.dashboard = Dashboard(self.offender_service, self.ai_service)
        self.stacked_widget.addWidget(self.dashboard)         # index 0
        
        # Offender form
        self.offender_form = OffenderForm(self.offender_service)
        self.stacked_widget.addWidget(self.offender_form)     # index 1
        
        # Offender list
        self.offender_list = OffenderList(self.offender_service, self.report_service)
        self.stacked_widget.addWidget(self.offender_list)     # index 2
        
        # Reports
        self.reports = Reports(self.offender_service, self.report_service)
        self.stacked_widget.addWidget(self.reports)           # index 3
        
        # AI Tools
        self.ai_tools = AITools(self.offender_service, self.ai_service)
        self.stacked_widget.addWidget(self.ai_tools)          # index 4

        # TẠM THỜI BỎ QStackedWidget CHO CÁN BỘ (Staff) nếu chưa có widget riêng
        # Nếu sau này có StaffWidget, thêm vào đây:
        # from .staff import StaffWidget
        # self.staff = StaffWidget(self.user_service)
        # self.stacked_widget.addWidget(self.staff)  # index 5
        
        # Settings
        self.settings = Settings(self.user_service)
        self.stacked_widget.addWidget(self.settings)          # index 5
        
    def setup_connections(self):
        """Setup signal connections."""
        # Sidebar navigation đã được xử lý trong on_sidebar_page_changed
        
        # Header connections - xóa vì HeaderWidget không có signal logout_clicked
        # self.header.logout_clicked.connect(self.handle_logout)
        
        # Offender form connections
        self.offender_form.offender_saved.connect(self.handle_offender_saved)
        
        # Offender list connections
        self.offender_list.offender_selected.connect(self.handle_offender_selected)
        self.offender_list.offender_deleted.connect(self.handle_offender_deleted)
        
        # Dashboard connections
        self.dashboard.refresh_requested.connect(self.refresh_data)
        self.dashboard.card_clicked.connect(self.handle_dashboard_card_clicked)
        
    def handle_dashboard_card_clicked(self, action_type: str, filter_data: dict):
        """Handle dashboard card click and navigate to appropriate page."""
        try:
            if action_type == "offender_list":
                # Chuyển đến danh sách đối tượng với filter
                self.show_offender_list_with_filter(filter_data)
            elif action_type == "alerts":
                # Chuyển đến danh sách đối tượng với filter cảnh báo
                self.show_offender_list_with_filter({"status": "warning"})
            elif action_type == "ai_tools":
                # Chuyển đến AI Tools
                self.show_ai_tools()
            elif action_type == "reports":
                # Chuyển đến Reports
                self.show_reports()
            else:
                # Default: chuyển đến danh sách đối tượng
                self.show_offender_list()
                
        except Exception as e:
            print(f"Error handling dashboard card click: {e}")
            # Fallback to offender list
            self.show_offender_list()
            
    def show_offender_list_with_filter(self, filter_data: dict):
        """Show offender list with specific filter."""
        # Chuyển đến trang danh sách đối tượng
        self.stacked_widget.setCurrentWidget(self.offender_list)
        self.sidebar.update_selection(2)  # Index của offender list
        self.status_bar.showMessage("Danh sách đối tượng")
        
        # Áp dụng filter nếu có
        if filter_data:
            status = filter_data.get("status")
            if status == "active":
                # Filter đối tượng đang chấp hành
                self.offender_list.apply_status_filter("active")
            elif status == "warning":
                # Filter đối tượng sắp hết hạn
                self.offender_list.apply_status_filter("expiring")
            elif status == "violation":
                # Filter đối tượng vi phạm
                self.offender_list.apply_status_filter("violation")
            elif status == "risk":
                # Filter đối tượng nguy cơ cao
                self.offender_list.apply_status_filter("high_risk")
        
    def setup_menu(self):
        """Setup application menu."""
        menubar = self.menuBar()
        
        # File menu
        file_menu = menubar.addMenu("&Tệp")
        
        new_offender_action = QAction("&Thêm đối tượng mới", self)
        new_offender_action.setShortcut(QKeySequence.StandardKey.New)
        new_offender_action.triggered.connect(self.show_offender_form)
        file_menu.addAction(new_offender_action)
        
        file_menu.addSeparator()
        
        exit_action = QAction("&Thoát", self)
        exit_action.setShortcut(QKeySequence.StandardKey.Quit)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)
        
        # Edit menu
        edit_menu = menubar.addMenu("&Chỉnh sửa")
        
        refresh_action = QAction("&Làm mới", self)
        refresh_action.setShortcut(QKeySequence.StandardKey.Refresh)
        refresh_action.triggered.connect(self.refresh_data)
        edit_menu.addAction(refresh_action)
        
        # View menu
        view_menu = menubar.addMenu("&Xem")
        
        dashboard_action = QAction("&Dashboard", self)
        dashboard_action.triggered.connect(self.show_dashboard)
        view_menu.addAction(dashboard_action)
        
        list_action = QAction("&Danh sách đối tượng", self)
        list_action.triggered.connect(self.show_offender_list)
        view_menu.addAction(list_action)
        
        # Help menu
        help_menu = menubar.addMenu("&Trợ giúp")
        
        about_action = QAction("&Giới thiệu", self)
        about_action.triggered.connect(self.show_about)
        help_menu.addAction(about_action)
        
    def setup_status_bar(self):
        """Setup status bar."""
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage("Sẵn sàng")
        
    def show_dashboard(self):
        """Show dashboard page."""
        self.stacked_widget.setCurrentWidget(self.dashboard)
        self.sidebar.update_selection(0)
        self.status_bar.showMessage("Dashboard")
        
    def show_offender_form(self):
        """Show offender form page."""
        self.stacked_widget.setCurrentWidget(self.offender_form)
        self.sidebar.update_selection(1)
        self.status_bar.showMessage("Nhập liệu đối tượng")
        
    def show_offender_list(self):
        """Show offender list page."""
        self.stacked_widget.setCurrentWidget(self.offender_list)
        self.sidebar.update_selection(2)
        self.offender_list.refresh_data()
        self.status_bar.showMessage("Danh sách đối tượng")
        
    def show_reports(self):
        """Show reports page."""
        self.stacked_widget.setCurrentWidget(self.reports)
        self.sidebar.update_selection(3)
        self.status_bar.showMessage("Báo cáo")
        
    def show_ai_tools(self):
        """Show AI tools page."""
        self.stacked_widget.setCurrentWidget(self.ai_tools)
        self.sidebar.update_selection(4)
        self.status_bar.showMessage("AI Tools")
        
    def show_settings(self):
        """Show settings page."""
        self.stacked_widget.setCurrentWidget(self.settings)
        self.sidebar.update_selection(5)
        self.status_bar.showMessage("Cài đặt")
        
    def handle_logout(self):
        """Handle logout."""
        reply = QMessageBox.question(
            self, "Xác nhận", "Bạn có muốn đăng xuất?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            self.user_service.logout()
            self.close()
            
    def handle_offender_saved(self, offender_id: int):
        """Handle offender saved event."""
        self.offender_updated.emit()
        self.dashboard.refresh_data()
        self.offender_list.refresh_data()
        self.status_bar.showMessage("Đối tượng đã được lưu thành công")
        
    def handle_offender_selected(self, offender_id: int):
        """Handle offender selected event."""
        # Could open offender form in edit mode
        self.show_offender_form()
        
    def handle_offender_deleted(self, offender_id: int):
        """Handle offender deleted event."""
        self.offender_deleted.emit(offender_id)
        self.dashboard.refresh_data()
        self.offender_list.refresh_data()
        self.status_bar.showMessage("Đối tượng đã được xóa")
        
    def refresh_data(self):
        """Refresh all data."""
        self.dashboard.refresh_data()
        self.offender_list.refresh_data()
        self.status_bar.showMessage("Dữ liệu đã được làm mới")
        
    def show_about(self):
        """Show about dialog."""
        QMessageBox.about(
            self, "Giới thiệu",
            "Hệ thống Quản lý Đối tượng Thi hành án\n"
            "Phiên bản 1.0.0\n\n"
            "Phát triển bởi Development Team"
        )
        
    def on_sidebar_page_changed(self, page_id):
        self.stacked_widget.setCurrentIndex(page_id)
        # Cập nhật status bar
        if page_id == 0:
            self.status_bar.showMessage("Dashboard")
        elif page_id == 1:
            self.status_bar.showMessage("Nhập liệu đối tượng")
        elif page_id == 2:
            self.status_bar.showMessage("Danh sách đối tượng")
        elif page_id == 3:
            self.status_bar.showMessage("Báo cáo")
        elif page_id == 4:
            self.status_bar.showMessage("AI Tools")
        # page_id == 5: Cài đặt (không còn staff)
        elif page_id == 5:
            self.status_bar.showMessage("Cài đặt")
        
    def resizeEvent(self, event):
        """Tự động thu nhỏ sidebar khi cửa sổ hẹp, mở rộng khi rộng."""
        super().resizeEvent(event)
        width = self.width()
        if width < 900:
            # Mini sidebar: chỉ hiện icon, ẩn text, thu nhỏ chiều rộng
            self.sidebar.set_mini_mode(True)
            self.sidebar.setMinimumWidth(60)
            self.sidebar.setMaximumWidth(80)
        else:
            # Full sidebar: hiện icon + text, mở rộng chiều rộng
            self.sidebar.set_mini_mode(False)
            self.sidebar.setMinimumWidth(180)
            self.sidebar.setMaximumWidth(400)
        
    def closeEvent(self, event):
        """Handle window close event."""
        reply = QMessageBox.question(
            self, "Xác nhận thoát", 
            "Bạn có chắc chắn muốn thoát ứng dụng?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            event.accept()
        else:
            event.ignore() 
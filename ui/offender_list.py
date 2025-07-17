#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Offender list widget for displaying and managing offenders.
"""

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
    QLineEdit, QComboBox, QPushButton, QTableWidget, QTableWidgetItem,
    QHeaderView, QMessageBox, QMenu, QFrame, QGroupBox, QDateEdit,
    QScrollArea, QSplitter, QToolButton, QSizePolicy
)
from PyQt6.QtCore import Qt, pyqtSignal, QDate
from PyQt6.QtGui import QFont, QAction, QPixmap

from typing import List, Optional

from models.offender import Offender, Status, RiskLevel
from services.offender_service import OffenderService
from services.report_service import ReportService
from ui.print_template_dialog import PrintTemplateDialog


class OffenderList(QWidget):
    """Widget for displaying and managing offender list."""
    
    # Signals
    offender_selected = pyqtSignal(int)  # Emits offender ID when selected
    offender_deleted = pyqtSignal(int)   # Emits offender ID when deleted
    
    def __init__(self, offender_service: OffenderService, 
                 report_service: ReportService, parent=None):
        """Initialize offender list."""
        super().__init__(parent)
        self.offender_service = offender_service
        self.report_service = report_service
        self.offenders: List[Offender] = []
        self.filtered_offenders: List[Offender] = []
        self.current_page = 1
        self.page_size = 10
        self.total_pages = 1
        self.setup_ui()
        self.setup_table()  # Đảm bảo self.table luôn được khởi tạo
        self.refresh_data()
        
    def setup_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(12, 12, 12, 12)
        main_layout.setSpacing(10)
        self.setup_header(main_layout)
        content_splitter = QSplitter(Qt.Orientation.Horizontal)
        content_splitter.setChildrenCollapsible(False)
        self.setup_filter_panel(content_splitter)
        # Bulk action bar
        self.bulk_action_bar = QFrame()
        self.bulk_action_bar.setObjectName("bulkActionBar")  # Đảm bảo nhận QSS động
        self.bulk_action_bar.setVisible(False)
        bulk_layout = QHBoxLayout(self.bulk_action_bar)
        bulk_layout.setContentsMargins(8, 4, 8, 4)
        bulk_layout.setSpacing(12)
        self.bulk_selected_label = QLabel()
        self.bulk_selected_label.setFont(QFont("Segoe UI", 11, QFont.Weight.Bold))
        bulk_layout.addWidget(self.bulk_selected_label)
        self.bulk_delete_btn = QPushButton("🗑️ Xóa")
        self.bulk_export_btn = QPushButton("📤 Xuất Excel")
        self.bulk_print_btn = QPushButton("🖨️ In báo cáo")
        for btn in [self.bulk_delete_btn, self.bulk_export_btn, self.bulk_print_btn]:
            btn.setMinimumHeight(32)
            btn.setFont(QFont("Segoe UI", 11))
            bulk_layout.addWidget(btn)
        bulk_layout.addStretch()
        main_layout.addWidget(self.bulk_action_bar)
        content_splitter.setSizes([300, 700])
        content_splitter.setStretchFactor(0, 0)
        content_splitter.setStretchFactor(1, 1)
        main_layout.addWidget(content_splitter)
        self.bulk_delete_btn.clicked.connect(self.bulk_delete_selected)
        self.bulk_export_btn.clicked.connect(self.bulk_export_selected)
        self.bulk_print_btn.clicked.connect(self.bulk_print_selected)
        self.bulk_delete_btn.setToolTip("Xóa các đối tượng đã chọn")
        self.bulk_export_btn.setToolTip("Xuất Excel các đối tượng đã chọn")
        self.bulk_print_btn.setToolTip("In báo cáo các đối tượng đã chọn")
        
    def setup_header(self, parent_layout):
        """Setup header section."""
        header_frame = QFrame()
        header_frame.setObjectName("listHeader")
        # Thu gọn header: giảm padding, font-size
        header_layout = QHBoxLayout(header_frame)
        header_layout.setContentsMargins(12, 6, 12, 6)
        header_layout.setSpacing(8)
        
        # Icon and title
        icon_label = QLabel()
        icon_pixmap = QPixmap("assets/logo_cand.png")
        if not icon_pixmap.isNull():
            icon_pixmap = icon_pixmap.scaled(24, 24, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
            icon_label.setPixmap(icon_pixmap)
        else:
            icon_label.setText("📋")
            icon_label.setFont(QFont("Segoe UI", 16))
        
        title_label = QLabel("DANH SÁCH ĐỐI TƯỢNG THI HÀNH ÁN")
        title_label.setFont(QFont("Segoe UI", 13, QFont.Weight.Bold))
        
        # Stats
        stats_label = QLabel(
            "Tổng: 0 | Đang chấp hành: 0 | Sắp hết hạn: 0"
        )
        stats_label.setFont(QFont("Segoe UI", 10))
        
        header_layout.addWidget(icon_label)
        header_layout.addWidget(title_label)
        header_layout.addStretch()
        header_layout.addWidget(stats_label)
        
        parent_layout.addWidget(header_frame)
        
    def setup_filter_panel(self, parent):
        """Setup filter panel."""
        filter_widget = QWidget()
        filter_widget.setObjectName("filterPanel")  # Đảm bảo nhận QSS động
        filter_widget.setMaximumWidth(320)
        filter_widget.setMinimumWidth(260)
        filter_widget.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Expanding)
        
        filter_layout = QVBoxLayout(filter_widget)
        filter_layout.setContentsMargins(12, 12, 12, 12)
        filter_layout.setSpacing(12)
        
        # Search section
        self.setup_search_section(filter_layout)
        
        # Filter section
        self.setup_filter_section(filter_layout)
        
        # Action buttons
        self.setup_action_buttons(filter_layout)
        
        parent.addWidget(filter_widget)
        
    def setup_search_section(self, parent_layout):
        """Setup search section."""
        search_group = QGroupBox("🔍 TÌM KIẾM")
        search_group.setFont(QFont("Segoe UI", 11, QFont.Weight.Bold))
        
        search_layout = QVBoxLayout(search_group)
        search_layout.setSpacing(8)
        
        # Search input
        self.search_edit = QLineEdit()
        self.search_edit.setPlaceholderText(
            "Tìm theo tên, số hồ sơ, địa chỉ..."
        )
        self.search_edit.setMinimumHeight(32)
        self.search_edit.setFont(QFont("Segoe UI", 11))
        search_layout.addWidget(self.search_edit)
        
        # Quick filters
        quick_filter_layout = QHBoxLayout()
        quick_filter_layout.setSpacing(6)
        
        self.active_filter_btn = QPushButton("🟢 Đang chấp hành")
        self.active_filter_btn.setCheckable(True)
        self.active_filter_btn.setMinimumHeight(28)
        self.active_filter_btn.setFont(QFont("Segoe UI", 9))
        quick_filter_layout.addWidget(self.active_filter_btn)
        
        self.expiring_filter_btn = QPushButton("🟠 Sắp hết hạn")
        self.expiring_filter_btn.setCheckable(True)
        self.expiring_filter_btn.setMinimumHeight(28)
        self.expiring_filter_btn.setFont(QFont("Segoe UI", 9))
        quick_filter_layout.addWidget(self.expiring_filter_btn)
        
        search_layout.addLayout(quick_filter_layout)
        parent_layout.addWidget(search_group)
        
    def setup_filter_section(self, parent_layout):
        """Setup filter section."""
        filter_group = QGroupBox("🔧 BỘ LỌC")
        filter_group.setFont(QFont("Segoe UI", 11, QFont.Weight.Bold))
        filter_layout = QVBoxLayout(filter_group)
        filter_layout.setSpacing(8)
        # Status filter
        status_layout = QHBoxLayout()
        status_label = QLabel("Trạng thái:")
        status_label.setFont(QFont("Segoe UI", 11))
        status_layout.addWidget(status_label)
        self.status_filter_combo = QComboBox()
        self.status_filter_combo.addItems([
            "Tất cả", "Đang chấp hành", "Sắp kết thúc", "Hoàn thành", "Vi phạm"
        ])
        self.status_filter_combo.setMinimumHeight(32)
        self.status_filter_combo.setFont(QFont("Segoe UI", 11))
        status_layout.addWidget(self.status_filter_combo)
        # Clear button for status
        status_clear_btn = QToolButton()
        status_clear_btn.setText("✕")
        status_clear_btn.setToolTip("Xóa lọc trạng thái")
        status_clear_btn.setFixedSize(22, 22)
        status_clear_btn.clicked.connect(lambda: self.status_filter_combo.setCurrentIndex(0))
        status_layout.addWidget(status_clear_btn)
        filter_layout.addLayout(status_layout)
        # Risk filter
        risk_layout = QHBoxLayout()
        risk_label = QLabel("Nguy cơ:")
        risk_label.setFont(QFont("Segoe UI", 11))
        risk_layout.addWidget(risk_label)
        self.risk_filter_combo = QComboBox()
        self.risk_filter_combo.addItems([
            "Tất cả", "Thấp", "Trung bình", "Cao"
        ])
        self.risk_filter_combo.setMinimumHeight(32)
        self.risk_filter_combo.setFont(QFont("Segoe UI", 11))
        risk_layout.addWidget(self.risk_filter_combo)
        # Clear button for risk
        risk_clear_btn = QToolButton()
        risk_clear_btn.setText("✕")
        risk_clear_btn.setToolTip("Xóa lọc nguy cơ")
        risk_clear_btn.setFixedSize(22, 22)
        risk_clear_btn.clicked.connect(lambda: self.risk_filter_combo.setCurrentIndex(0))
        risk_layout.addWidget(risk_clear_btn)
        filter_layout.addLayout(risk_layout)
        # Area filter (Phường/xã)
        area_layout = QHBoxLayout()
        area_label = QLabel("Phường/xã:")
        area_label.setFont(QFont("Segoe UI", 11))
        area_layout.addWidget(area_label)
        self.ward_filter_combo = QComboBox()
        self.ward_filter_combo.addItem("Tất cả")
        self.ward_filter_combo.setMinimumHeight(32)
        self.ward_filter_combo.setFont(QFont("Segoe UI", 11))
        area_layout.addWidget(self.ward_filter_combo)
        # Clear button for ward
        ward_clear_btn = QToolButton()
        ward_clear_btn.setText("✕")
        ward_clear_btn.setToolTip("Xóa lọc phường/xã")
        ward_clear_btn.setFixedSize(22, 22)
        ward_clear_btn.clicked.connect(lambda: self.ward_filter_combo.setCurrentIndex(0))
        area_layout.addWidget(ward_clear_btn)
        filter_layout.addLayout(area_layout)
        # Case type filter (Loại án)
        case_type_layout = QHBoxLayout()
        case_type_label = QLabel("Loại án:")
        case_type_label.setFont(QFont("Segoe UI", 11))
        case_type_layout.addWidget(case_type_label)
        self.case_type_filter_combo = QComboBox()
        self.case_type_filter_combo.addItem("Tất cả")
        self.case_type_filter_combo.setMinimumHeight(32)
        self.case_type_filter_combo.setFont(QFont("Segoe UI", 11))
        case_type_layout.addWidget(self.case_type_filter_combo)
        # Clear button for case type
        case_type_clear_btn = QToolButton()
        case_type_clear_btn.setText("✕")
        case_type_clear_btn.setToolTip("Xóa lọc loại án")
        case_type_clear_btn.setFixedSize(22, 22)
        case_type_clear_btn.clicked.connect(lambda: self.case_type_filter_combo.setCurrentIndex(0))
        case_type_layout.addWidget(case_type_clear_btn)
        filter_layout.addLayout(case_type_layout)
        # Start date filter (Ngày bắt đầu từ)
        start_date_layout = QHBoxLayout()
        start_date_label = QLabel("Từ ngày:")
        start_date_label.setFont(QFont("Segoe UI", 11))
        start_date_layout.addWidget(start_date_label)
        self.start_date_filter = QDateEdit()
        self.start_date_filter.setCalendarPopup(True)
        self.start_date_filter.setDisplayFormat("dd/MM/yyyy")
        self.start_date_filter.setMinimumHeight(32)
        self.start_date_filter.setFont(QFont("Segoe UI", 11))
        self.start_date_filter.setDate(QDate(2000, 1, 1))
        start_date_layout.addWidget(self.start_date_filter)
        # Clear button for start date
        start_date_clear_btn = QToolButton()
        start_date_clear_btn.setText("✕")
        start_date_clear_btn.setToolTip("Xóa lọc từ ngày")
        start_date_clear_btn.setFixedSize(22, 22)
        start_date_clear_btn.clicked.connect(lambda: self.start_date_filter.setDate(QDate(2000, 1, 1)))
        start_date_layout.addWidget(start_date_clear_btn)
        filter_layout.addLayout(start_date_layout)
        # End date filter (Đến ngày hoàn thành)
        end_date_layout = QHBoxLayout()
        end_date_label = QLabel("Đến ngày:")
        end_date_label.setFont(QFont("Segoe UI", 11))
        end_date_layout.addWidget(end_date_label)
        self.end_date_filter = QDateEdit()
        self.end_date_filter.setCalendarPopup(True)
        self.end_date_filter.setDisplayFormat("dd/MM/yyyy")
        self.end_date_filter.setMinimumHeight(32)
        self.end_date_filter.setFont(QFont("Segoe UI", 11))
        self.end_date_filter.setDate(QDate.currentDate())
        end_date_layout.addWidget(self.end_date_filter)
        # Clear button for end date
        end_date_clear_btn = QToolButton()
        end_date_clear_btn.setText("✕")
        end_date_clear_btn.setToolTip("Xóa lọc đến ngày")
        end_date_clear_btn.setFixedSize(22, 22)
        end_date_clear_btn.clicked.connect(lambda: self.end_date_filter.setDate(QDate.currentDate()))
        end_date_layout.addWidget(end_date_clear_btn)
        filter_layout.addLayout(end_date_layout)
        # Filter button
        self.filter_button = QPushButton("🔍 LỌC")
        self.filter_button.setMinimumHeight(32)
        self.filter_button.setFont(QFont("Segoe UI", 11, QFont.Weight.Bold))
        filter_layout.addWidget(self.filter_button)
        # Reset all filters button
        reset_btn = QPushButton("Đặt lại bộ lọc")
        reset_btn.setMinimumHeight(28)
        reset_btn.setFont(QFont("Segoe UI", 10))
        reset_btn.clicked.connect(self.reset_all_filters)
        filter_layout.addWidget(reset_btn)
        parent_layout.addWidget(filter_group)

    def setup_action_buttons(self, parent_layout):
        """Setup action buttons."""
        action_group = QGroupBox("⚡ THAO TÁC")
        action_group.setFont(QFont("Segoe UI", 11, QFont.Weight.Bold))
        
        action_layout = QVBoxLayout(action_group)
        action_layout.setSpacing(8)
        
        # Row 1: Add, Edit, Delete
        row1_layout = QHBoxLayout()
        self.add_button = self.create_action_button("➕ Thêm mới", "#10B981")
        self.edit_button = self.create_action_button("✏️ Sửa", "#3B82F6")
        self.delete_button = self.create_action_button("🗑️ Xóa", "#EF4444")
        row1_layout.addWidget(self.add_button)
        row1_layout.addWidget(self.edit_button)
        row1_layout.addWidget(self.delete_button)
        action_layout.addLayout(row1_layout)
        
        # Row 2: Import, Export
        row2_layout = QHBoxLayout()
        self.import_excel_button = self.create_action_button("📥 Import", "#8B5CF6")
        self.export_excel_button = self.create_action_button("📤 Excel", "#10B981")
        self.export_json_button = self.create_action_button("📄 JSON", "#F59E0B")
        row2_layout.addWidget(self.import_excel_button)
        row2_layout.addWidget(self.export_excel_button)
        row2_layout.addWidget(self.export_json_button)
        action_layout.addLayout(row2_layout)
        
        # Row 3: Refresh
        row3_layout = QHBoxLayout()
        self.refresh_button = self.create_action_button("🔄 Làm mới", "#6B7280")
        row3_layout.addWidget(self.refresh_button)
        row3_layout.addStretch()
        action_layout.addLayout(row3_layout)
        
        parent_layout.addWidget(action_group)
        
    def create_action_button(self, text: str, color: str) -> QPushButton:
        """Create action button."""
        btn = QPushButton(text)
        btn.setMinimumHeight(32)
        btn.setFont(QFont("Segoe UI", 11))
        btn.setProperty("color", color)
        return btn
        
    def setup_table_panel(self, parent):
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        scroll_area.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        table_widget = QWidget()
        table_widget.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        table_layout = QVBoxLayout(table_widget)
        table_layout.setContentsMargins(10, 10, 10, 10)
        table_layout.setSpacing(6)
        
        self.setup_table()
        table_layout.addWidget(self.table)
        # Pagination UI
        self.pagination_bar = QHBoxLayout()
        self.pagination_bar.setContentsMargins(0, 0, 0, 0)
        self.pagination_bar.setSpacing(8)
        table_layout.addLayout(self.pagination_bar)
        table_layout.addStretch()  # Đảm bảo co giãn full chiều dọc
        scroll_area.setWidget(table_widget)
        parent.addWidget(scroll_area)

    def setup_table(self):
        self.table = QTableWidget()
        self.table.setAlternatingRowColors(True)
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.table.setSelectionMode(QTableWidget.SelectionMode.SingleSelection)
        self.table.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.table.setMinimumHeight(600)
        self.table.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        # Set headers - thêm cột checkbox đầu tiên
        headers = ["☑", "ID", "Số hồ sơ", "Họ tên", "Giới tính", "Ngày sinh", 
            "Phường/xã", "Địa chỉ", "Nghề nghiệp", "Tội danh", "Loại án", "Số bản án",
            "Số quyết định", "Ngày bắt đầu", "Thời gian (tháng)", 
            "Được giảm (tháng)", "Ngày giảm", "Số lần giảm",
            "Ngày hoàn thành", "Trạng thái", "Ngày còn lại", "Mức độ nguy cơ"]
        self.table.setColumnCount(len(headers))
        self.table.setHorizontalHeaderLabels(headers)
        header = self.table.horizontalHeader()
        header.setStretchLastSection(True)
        header.setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)
        self.table.verticalHeader().setDefaultSectionSize(32)
        # Checkbox header logic
        self.table.horizontalHeader().sectionClicked.connect(self.on_header_checkbox_clicked)
        self.header_checkbox_state = False
        self.selected_ids = set()

    def on_header_checkbox_clicked(self, idx):
        if idx == 0:
            # Toggle select all on current page
            self.header_checkbox_state = not self.header_checkbox_state
            for row in range(self.table.rowCount()):
                item = self.table.item(row, 0)
                if item is not None:
                    item.setCheckState(Qt.CheckState.Checked if self.header_checkbox_state else Qt.CheckState.Unchecked)
                    offender_id_item = self.table.item(row, 1)
                    if offender_id_item:
                        oid = offender_id_item.text()
                        if self.header_checkbox_state:
                            self.selected_ids.add(oid)
                        else:
                            self.selected_ids.discard(oid)
            self.update_bulk_action_bar()

    def populate_table_with_data(self, offenders: List[Offender]):
        # Only show current page
        total = len(offenders)
        start_idx = (self.current_page - 1) * self.page_size
        end_idx = min(self.current_page * self.page_size, total)
        page_offenders = offenders[start_idx:end_idx]
        self.table.setRowCount(len(page_offenders))
        for row, offender in enumerate(page_offenders):
            # Checkbox
            checkbox_item = QTableWidgetItem()
            checkbox_item.setFlags(checkbox_item.flags() | Qt.ItemFlag.ItemIsUserCheckable)
            oid = str(offender.id)
            if oid in self.selected_ids:
                checkbox_item.setCheckState(Qt.CheckState.Checked)
            else:
                checkbox_item.setCheckState(Qt.CheckState.Unchecked)
            self.table.setItem(row, 0, checkbox_item)
            # Connect checkbox state change
            self.table.itemChanged.connect(self.on_row_checkbox_changed)
            # ID
            id_item = QTableWidgetItem(str(offender.id))
            id_item.setFlags(id_item.flags() & ~Qt.ItemFlag.ItemIsEditable)
            self.table.setItem(row, 1, id_item)
            
            # Full name
            name_item = QTableWidgetItem(offender.full_name)
            self.table.setItem(row, 2, name_item)
            
            # Case number
            case_item = QTableWidgetItem(offender.case_number)
            self.table.setItem(row, 3, case_item)
            
            # Status
            status_val = offender.status.value if hasattr(offender.status, 'value') else str(offender.status)
            status_item = QTableWidgetItem(status_val)
            # Tô màu status
            if offender.status == Status.ACTIVE:
                status_item.setBackground(Qt.GlobalColor.green)
                status_item.setForeground(Qt.GlobalColor.white)
            elif offender.status == Status.EXPIRING_SOON:
                status_item.setBackground(Qt.GlobalColor.yellow)
                status_item.setForeground(Qt.GlobalColor.black)
            elif offender.status == Status.COMPLETED:
                status_item.setBackground(Qt.GlobalColor.gray)
                status_item.setForeground(Qt.GlobalColor.white)
            elif offender.status == Status.VIOLATION:
                status_item.setBackground(Qt.GlobalColor.red)
                status_item.setForeground(Qt.GlobalColor.white)
            self.table.setItem(row, 4, status_item)
            
            # Risk level
            risk_val = offender.risk_level.value if hasattr(offender.risk_level, 'value') else str(offender.risk_level)
            risk_item = QTableWidgetItem(risk_val)
            # Tô màu risk
            if offender.risk_level == RiskLevel.LOW:
                risk_item.setBackground(Qt.GlobalColor.green)
                risk_item.setForeground(Qt.GlobalColor.white)
            elif offender.risk_level == RiskLevel.MEDIUM:
                risk_item.setBackground(Qt.GlobalColor.yellow)
                risk_item.setForeground(Qt.GlobalColor.black)
            elif offender.risk_level == RiskLevel.HIGH:
                risk_item.setBackground(Qt.GlobalColor.red)
                risk_item.setForeground(Qt.GlobalColor.white)
            self.table.setItem(row, 5, risk_item)
            
            # Ward
            ward_item = QTableWidgetItem(offender.ward)
            self.table.setItem(row, 6, ward_item)
            
            # Address
            address_item = QTableWidgetItem(offender.address)
            self.table.setItem(row, 7, address_item)
            
            # Occupation
            occupation_item = QTableWidgetItem(offender.occupation)
            self.table.setItem(row, 8, occupation_item)
            
            # Crime type
            case_type_val = offender.case_type.value if hasattr(offender.case_type, 'value') else str(offender.case_type)
            crime_item = QTableWidgetItem(case_type_val)
            self.table.setItem(row, 9, crime_item)
            
            # Sentence
            sentence_item = QTableWidgetItem(offender.sentence)
            self.table.setItem(row, 10, sentence_item)
            
            # Court
            court_item = QTableWidgetItem(offender.court)
            self.table.setItem(row, 11, court_item)
            
            # Decision number
            decision_item = QTableWidgetItem(offender.decision_number)
            self.table.setItem(row, 12, decision_item)
            
            # Decision date
            decision_date = offender.decision_date.strftime("%d/%m/%Y") if offender.decision_date else ""
            decision_date_item = QTableWidgetItem(decision_date)
            self.table.setItem(row, 13, decision_date_item)
            
            # Notes
            notes_item = QTableWidgetItem(offender.notes)
            self.table.setItem(row, 14, notes_item)
            
        # Ngắt kết nối tránh lặp signal
        self.table.itemChanged.disconnect(self.on_row_checkbox_changed)
        self.table.itemChanged.connect(self.on_row_checkbox_changed)
        self.update_header_checkbox_state()
        self.update_bulk_action_bar()

    def on_row_checkbox_changed(self, item):
        if item.column() == 0:
            row = item.row()
            id_item = self.table.item(row, 1)
            if id_item:
                oid = id_item.text()
                if item.checkState() == Qt.CheckState.Checked:
                    self.selected_ids.add(oid)
                else:
                    self.selected_ids.discard(oid)
            self.update_bulk_action_bar()

    def update_button_states(self):
        """Update button states based on selection."""
        has_selection = len(self.table.selectedItems()) > 0
        self.edit_button.setEnabled(has_selection)
        self.delete_button.setEnabled(has_selection)
        
    def update_status(self, visible_count=None, total_count=None):
        """Update status label."""
        if visible_count is None:
            visible_count = sum(1 for row in range(self.table.rowCount()) 
                              if not self.table.isRowHidden(row))
            total_count = self.table.rowCount()
        self.status_label.setText(f"Hiển thị {visible_count} trong tổng số {total_count} đối tượng")
        self.pagination_label.setText(f"Hiển thị 1-{min(visible_count, 10)} của {visible_count} kết quả")
        
    def update_stats(self):
        """Update header statistics."""
        total = len(self.offenders)
        active = len([o for o in self.offenders if o.status == Status.ACTIVE])
        expiring = len([o for o in self.offenders if o.status == Status.EXPIRING_SOON])
        
        # Update header stats
        stats_text = f"Tổng: {total} | Đang chấp hành: {active} | Sắp hết hạn: {expiring}"
        
        # Find and update stats label in header
        for child in self.findChildren(QLabel):
            if "Tổng:" in child.text():
                child.setText(stats_text)
                break
        
    def get_selected_offender_id(self) -> Optional[int]:
        """Get ID of selected offender."""
        selected_rows = self.table.selectionModel().selectedRows()
        if selected_rows:
            row = selected_rows[0].row()
            id_item = self.table.item(row, 0)
            if id_item:
                return int(id_item.text())
        return None
        
    def add_new_offender(self):
        """Add new offender."""
        # This will be handled by main window
        pass
        
    def edit_selected_offender(self):
        """Edit selected offender."""
        offender_id = self.get_selected_offender_id()
        if offender_id:
            self.offender_selected.emit(offender_id)
        else:
            QMessageBox.warning(self, "Cảnh báo", "Vui lòng chọn một đối tượng để chỉnh sửa!")
            
    def delete_selected_offender(self):
        """Delete selected offender."""
        offender_id = self.get_selected_offender_id()
        if not offender_id:
            QMessageBox.warning(self, "Cảnh báo", "Vui lòng chọn một đối tượng để xóa!")
            return
            
        reply = QMessageBox.question(
            self, "Xác nhận", "Bạn có chắc chắn muốn xóa đối tượng này?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            try:
                success = self.offender_service.delete_offender(offender_id)
                if success:
                    self.offender_deleted.emit(offender_id)
                    self.refresh_data()
                    QMessageBox.information(self, "Thành công", "Đối tượng đã được xóa!")
                else:
                    QMessageBox.critical(self, "Lỗi", "Không thể xóa đối tượng!")
            except Exception as e:
                QMessageBox.critical(self, "Lỗi", f"Lỗi khi xóa đối tượng: {str(e)}")
                
    def import_from_excel(self):
        """Import offenders from Excel file."""
        try:
            from PyQt6.QtWidgets import QFileDialog
            
            filename, _ = QFileDialog.getOpenFileName(
                self, "Nhập Excel", "", "Excel Files (*.xlsx *.xls)"
            )
            
            if filename:
                from services.excel_service import ExcelService
                excel_service = ExcelService(self.offender_service)
                
                result = excel_service.import_from_excel(filename)
                
                if result['success']:
                    QMessageBox.information(
                        self, "Thành công", 
                        f"Đã nhập {result['imported_count']} đối tượng từ Excel!"
                    )
                    self.refresh_data()
                else:
                    error_msg = f"Lỗi nhập Excel: {result.get('error', '')}"
                    if result['errors']:
                        error_msg += f"\n\nChi tiết lỗi:\n" + "\n".join(result['errors'])
                    QMessageBox.warning(self, "Lỗi", error_msg)
                    
        except Exception as e:
            QMessageBox.critical(self, "Lỗi", f"Không thể nhập Excel: {str(e)}")
    
    def export_to_excel(self):
        """Export data to Excel."""
        try:
            from PyQt6.QtWidgets import QFileDialog
            filename, _ = QFileDialog.getSaveFileName(
                self, "Xuất Excel", "offenders.xlsx", "Excel Files (*.xlsx)"
            )
            
            if filename:
                from services.excel_service import ExcelService
                excel_service = ExcelService(self.offender_service)
                
                success = excel_service.export_to_excel(self.offenders, filename)
                if success:
                    QMessageBox.information(self, "Thành công", f"Dữ liệu đã được xuất đến {filename}")
                else:
                    QMessageBox.critical(self, "Lỗi", "Không thể xuất dữ liệu!")
        except Exception as e:
            QMessageBox.critical(self, "Lỗi", f"Lỗi khi xuất dữ liệu: {str(e)}")
            
    def export_to_json(self):
        """Export data to JSON."""
        try:
            from PyQt6.QtWidgets import QFileDialog
            filename, _ = QFileDialog.getSaveFileName(
                self, "Xuất JSON", "offenders.json", "JSON Files (*.json)"
            )
            
            if filename:
                import json
                offenders_data = []
                for offender in self.offenders:
                    offenders_data.append(offender.to_dict())
                
                with open(filename, 'w', encoding='utf-8') as f:
                    json.dump(offenders_data, f, ensure_ascii=False, indent=2)
                
                QMessageBox.information(self, "Thành công", "Xuất JSON thành công!")
                
        except Exception as e:
            QMessageBox.critical(self, "Lỗi", f"Không thể xuất JSON: {str(e)}")
            
    def show_context_menu(self, position):
        """Show context menu."""
        menu = QMenu()
        
        edit_action = QAction("Chỉnh sửa", self)
        edit_action.triggered.connect(self.edit_selected_offender)
        menu.addAction(edit_action)
        
        delete_action = QAction("Xóa", self)
        delete_action.triggered.connect(self.delete_selected_offender)
        menu.addAction(delete_action)
        
        menu.addSeparator()
        
        view_action = QAction("Xem chi tiết", self)
        view_action.triggered.connect(self.edit_selected_offender)
        menu.addAction(view_action)
        
        # Thêm mục in mẫu Word/PDF
        print_action = QAction("In mẫu Word/PDF", self)
        print_action.triggered.connect(self.print_selected_offender)
        menu.addAction(print_action)
        
        menu.exec(self.table.mapToGlobal(position)) 

    def print_selected_offender(self):
        """In mẫu Word/PDF cho đối tượng đang chọn."""
        offender_id = self.get_selected_offender_id()
        if not offender_id:
            QMessageBox.warning(self, "Cảnh báo", "Vui lòng chọn một đối tượng để in mẫu!")
            return
        # Lấy dữ liệu đối tượng
        offender = next((o for o in self.offenders if o.id == offender_id), None)
        if not offender:
            QMessageBox.warning(self, "Lỗi", "Không tìm thấy dữ liệu đối tượng!")
            return
        # Chuyển offender thành dict context
        context = offender.to_dict()
        # Mở dialog chọn mẫu in
        dialog = PrintTemplateDialog(context, self)
        dialog.exec() 

    def refresh_data(self):
        """Refresh offender data."""
        try:
            self.offenders = self.offender_service.get_all_offenders()
            # --- Populate area and case_type filter dynamically ---
            ward_set = set()
            for offender in self.offenders:
                if hasattr(offender, 'ward') and offender.ward:
                    ward_set.add(offender.ward)
            current_ward = self.ward_filter_combo.currentText()
            self.ward_filter_combo.blockSignals(True)
            self.ward_filter_combo.clear()
            self.ward_filter_combo.addItem("Tất cả")
            for ward in sorted(ward_set):
                self.ward_filter_combo.addItem(ward)
            if current_ward in ward_set:
                self.ward_filter_combo.setCurrentText(current_ward)
            self.ward_filter_combo.blockSignals(False)
            # --- End dynamic filter update ---
            self.populate_table_with_data(self.offenders) # Use self.offenders directly
            self.update_status()
            self.update_stats()
        except Exception as e:
            QMessageBox.critical(self, "Lỗi", f"Không thể tải dữ liệu: {str(e)}")

    def reset_all_filters(self):
        self.status_filter_combo.setCurrentIndex(0)
        self.risk_filter_combo.setCurrentIndex(0)
        self.ward_filter_combo.setCurrentIndex(0)
        self.case_type_filter_combo.setCurrentIndex(0)
        self.start_date_filter.setDate(QDate(2000, 1, 1))
        self.end_date_filter.setDate(QDate.currentDate())
        self.search_edit.clear()
        self.active_filter_btn.setChecked(False)
        self.expiring_filter_btn.setChecked(False) 

    def update_pagination_ui(self):
        from PyQt6.QtWidgets import QComboBox, QPushButton, QLabel
        # Clear old widgets
        while self.pagination_bar.count():
            item = self.pagination_bar.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()
        # Page size selector
        page_size_label = QLabel("Dòng/trang:")
        self.pagination_bar.addWidget(page_size_label)
        self.page_size_combo = QComboBox()
        self.page_size_combo.addItems([
            "10", "20", "50"
        ])
        self.page_size_combo.setCurrentText(str(self.page_size))
        self.page_size_combo.setFixedWidth(60)
        self.page_size_combo.currentTextChanged.connect(self.on_page_size_changed)
        self.pagination_bar.addWidget(self.page_size_combo)
        # Prev button
        prev_btn = QPushButton("◀")
        prev_btn.setFixedWidth(32)
        prev_btn.clicked.connect(self.goto_prev_page)
        prev_btn.setEnabled(self.current_page > 1)
        self.pagination_bar.addWidget(prev_btn)
        # Page buttons
        max_page_btns = 5
        start_page = max(1, self.current_page - 2)
        end_page = min(self.total_pages, start_page + max_page_btns - 1)
        for page in range(start_page, end_page + 1):
            btn = QPushButton(str(page))
            btn.setFixedWidth(32)
            btn.setCheckable(True)
            btn.setChecked(page == self.current_page)
            btn.clicked.connect(lambda checked, p=page: self.goto_page(p))
            self.pagination_bar.addWidget(btn)
        # Next button
        next_btn = QPushButton("▶")
        next_btn.setFixedWidth(32)
        next_btn.clicked.connect(self.goto_next_page)
        next_btn.setEnabled(self.current_page < self.total_pages)
        self.pagination_bar.addWidget(next_btn)
        # Info label
        total = len(self.filtered_offenders)
        start_idx = (self.current_page - 1) * self.page_size + 1 if total > 0 else 0
        end_idx = min(self.current_page * self.page_size, total)
        info_label = QLabel(f"Hiển thị {start_idx}-{end_idx} của {total} kết quả")
        self.pagination_bar.addWidget(info_label)
        self.pagination_bar.addStretch()

    def on_page_size_changed(self, text):
        self.page_size = int(text)
        self.current_page = 1
        self.update_pagination()

    def goto_prev_page(self):
        if self.current_page > 1:
            self.current_page -= 1
            self.update_pagination()

    def goto_next_page(self):
        if self.current_page < self.total_pages:
            self.current_page += 1
            self.update_pagination()

    def goto_page(self, page):
        self.current_page = page
        self.update_pagination() 

    def update_header_checkbox_state(self):
        checked = 0
        total = self.table.rowCount()
        for row in range(total):
            item = self.table.item(row, 0)
            if item and item.checkState() == Qt.CheckState.Checked:
                checked += 1
        if checked == total and total > 0:
            self.header_checkbox_state = True
            self.table.horizontalHeaderItem(0).setText("☑")
        elif checked == 0:
            self.header_checkbox_state = False
            self.table.horizontalHeaderItem(0).setText("☐")
        else:
            self.header_checkbox_state = False
            self.table.horizontalHeaderItem(0).setText("☒") 

    def update_bulk_action_bar(self):
        count = len(self.selected_ids)
        if count > 0:
            self.bulk_action_bar.setVisible(True)
            self.bulk_selected_label.setText(f"Đã chọn {count} đối tượng")
        else:
            self.bulk_action_bar.setVisible(False) 

    def bulk_delete_selected(self):
        if not self.selected_ids:
            return
        count = len(self.selected_ids)
        reply = QMessageBox.question(
            self, "Xác nhận xóa",
            f"Bạn có chắc chắn muốn xóa {count} đối tượng đã chọn?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        if reply == QMessageBox.StandardButton.Yes:
            self.bulk_delete_btn.setEnabled(False)
            failed = []
            for oid in list(self.selected_ids):
                try:
                    success = self.offender_service.delete_offender(int(oid))
                    if not success:
                        failed.append(oid)
                    else:
                        self.selected_ids.discard(oid)
                except Exception:
                    failed.append(oid)
            self.bulk_delete_btn.setEnabled(True)
            self.refresh_data()
            if failed:
                QMessageBox.warning(self, "Lỗi", f"Không thể xóa {len(failed)} đối tượng!")
            else:
                QMessageBox.information(self, "Thành công", "Đã xóa các đối tượng đã chọn!")

    def bulk_export_selected(self):
        if not self.selected_ids:
            return
        from PyQt6.QtWidgets import QFileDialog
        filename, _ = QFileDialog.getSaveFileName(
            self, "Xuất Excel", "offenders_selected.xlsx", "Excel Files (*.xlsx)"
        )
        if filename:
            from services.excel_service import ExcelService
            excel_service = ExcelService(self.offender_service)
            offenders_to_export = [o for o in self.offenders if str(o.id) in self.selected_ids]
            self.bulk_export_btn.setEnabled(False)
            success = excel_service.export_to_excel(offenders_to_export, filename)
            self.bulk_export_btn.setEnabled(True)
            if success:
                QMessageBox.information(self, "Thành công", f"Đã xuất {len(offenders_to_export)} đối tượng!")
            else:
                QMessageBox.critical(self, "Lỗi", "Không thể xuất dữ liệu!")

    def bulk_print_selected(self):
        if not self.selected_ids:
            return
        offenders_to_print = [o for o in self.offenders if str(o.id) in self.selected_ids]
        if not offenders_to_print:
            QMessageBox.warning(self, "Cảnh báo", "Không có đối tượng nào để in!")
            return
        self.bulk_print_btn.setEnabled(False)
        # Mở dialog in cho từng đối tượng (hoặc có thể mở dialog batch nếu có)
        for offender in offenders_to_print:
            context = offender.to_dict()
            dialog = PrintTemplateDialog(context, self)
            dialog.exec()
        self.bulk_print_btn.setEnabled(True)
        QMessageBox.information(self, "Thành công", f"Đã in báo cáo cho {len(offenders_to_print)} đối tượng!") 
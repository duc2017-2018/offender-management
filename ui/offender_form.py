#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Offender form for adding/editing offender information.
"""

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLineEdit, QComboBox, QDateEdit,
    QPushButton, QLabel, QGroupBox, QHBoxLayout, QSpinBox, 
    QTextEdit, QGridLayout, QMessageBox, QScrollArea, QFrame,
    QGraphicsDropShadowEffect, QSizePolicy, QCompleter, QFileDialog,
    QInputDialog
)
from PyQt6.QtCore import pyqtSignal, QDate, Qt, QStringListModel
from PyQt6.QtGui import QFont, QPixmap, QColor
import os
from typing import Dict, Any, Optional
import json
import pandas as pd
import pytesseract
from PIL import Image
import pdfplumber
import docx
from autocorrect import Speller
from underthesea import ner
from fuzzywuzzy import process

from constants import COMPONENT_SIZES
from models.offender import Offender, Gender, CaseType
from services.offender_service import OffenderService


class OffenderForm(QWidget):
    """Form for adding/editing offender information."""
    
    # Signals
    offender_saved = pyqtSignal(int)  # Emits offender ID when saved
    offender_cancelled = pyqtSignal()
    
    def __init__(self, offender_service: OffenderService, parent=None):
        """Initialize offender form."""
        super().__init__(parent)
        self.offender_service = offender_service
        self.current_offender_id: Optional[int] = None
        self.setup_ui()
        self.setup_connections()
        
    def setup_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(12, 12, 12, 12)
        main_layout.setSpacing(10)
        self.setup_header(main_layout)
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setFrameShape(QFrame.Shape.NoFrame)
        scroll_area.setVerticalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAsNeeded
        )
        scroll_area.setHorizontalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAlwaysOff
        )
        scroll_area.setSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding
        )
        form_widget = QWidget()
        form_widget.setSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding
        )
        form_layout = QVBoxLayout(form_widget)
        form_layout.setContentsMargins(12, 12, 12, 12)
        form_layout.setSpacing(10)
        self.setup_basic_info_section(form_layout)
        self.setup_case_info_section(form_layout)
        self.setup_sentence_info_section(form_layout)
        self.setup_calculation_section(form_layout)
        self.setup_notes_section(form_layout)
        form_layout.addStretch()  # Đảm bảo co giãn full chiều dọc
        scroll_area.setWidget(form_widget)
        main_layout.addWidget(scroll_area)
        self.setup_action_bar(main_layout)
        self.case_number_edit.setFocus()  # Auto-focus trường đầu tiên
        
    def setup_header(self, parent_layout):
        """Setup header section."""
        header_frame = QFrame()
        header_frame.setObjectName("header")
        header_layout = QHBoxLayout(header_frame)
        header_layout.setContentsMargins(30, 20, 30, 20)
        icon_label = QLabel()
        icon_pixmap = QPixmap("assets/logo_cand.png")
        if not icon_pixmap.isNull():
            icon_pixmap = icon_pixmap.scaled(40, 40, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
            icon_label.setPixmap(icon_pixmap)
        else:
            icon_label.setText("🏛️")
            icon_label.setFont(QFont("Segoe UI", 24))
        title_label = QLabel("NHẬP THÔNG TIN ĐỐI TƯỢNG THI HÀNH ÁN")
        title_label.setFont(QFont("Segoe UI", 18, QFont.Weight.Bold))
        title_label.setObjectName("headerTitle")  # Đảm bảo nhận QSS động
        header_layout.addWidget(icon_label)
        header_layout.addWidget(title_label)
        header_layout.addStretch()
        parent_layout.addWidget(header_frame)
        
    def setup_basic_info_section(self, parent_layout):
        """Setup basic information section."""
        section = self.create_section("👤 THÔNG TIN CƠ BẢN", parent_layout)
        layout = QGridLayout(section)
        layout.setSpacing(15)
        
        # Row 1
        layout.addWidget(self.create_label("Số hồ sơ *"), 0, 0)
        self.case_number_edit = self.create_input("VD: 40CE0625/405LF")
        layout.addWidget(self.case_number_edit, 0, 1)
        self.case_number_error = QLabel()
        self.case_number_error.setObjectName("errorLabel")
        self.case_number_error.setVisible(False)
        layout.addWidget(self.case_number_error, 1, 1)
        
        layout.addWidget(self.create_label("Họ và tên *"), 0, 2)
        self.full_name_edit = self.create_input(
            "Nhập họ và tên"
        )
        layout.addWidget(self.full_name_edit, 0, 3)
        self.full_name_error = QLabel()
        self.full_name_error.setObjectName("errorLabel")
        self.full_name_error.setVisible(False)
        layout.addWidget(self.full_name_error, 1, 3)
        
        # Row 2
        layout.addWidget(self.create_label("Giới tính *"), 1, 0)
        self.gender_combo = self.create_combo([
            gender.value for gender in Gender
        ])
        layout.addWidget(self.gender_combo, 1, 1)
        
        layout.addWidget(self.create_label("Ngày sinh *"), 1, 2)
        self.birth_date_edit = self.create_date_edit()
        layout.addWidget(self.birth_date_edit, 1, 3)
        
        # Row 3
        layout.addWidget(self.create_label("Nơi cư trú *"), 2, 0)
        self.address_edit = self.create_input(
            "VD: TDP 1, P. Bắc Hồng, TX. Hồng Lĩnh"
        )
        layout.addWidget(self.address_edit, 2, 1)
        
        layout.addWidget(self.create_label("Phường/xã *"), 2, 2)
        self.ward_edit = self.create_input("VD: Bắc Hồng")
        # Thêm autocomplete cho ward
        self.ward_completer = QCompleter()
        self.ward_completer.setCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)
        self.ward_edit.setCompleter(self.ward_completer)
        layout.addWidget(self.ward_edit, 2, 3)
        # Sự kiện tự động tách ward từ address
        self.address_edit.editingFinished.connect(self.auto_extract_ward_from_address)
        
        # Row 4
        layout.addWidget(self.create_label("Nghề nghiệp"), 3, 0)
        self.occupation_edit = self.create_input(
            "VD: Nông dân, Thợ may, Lao động tự do"
        )
        layout.addWidget(self.occupation_edit, 3, 1)
        
        layout.addWidget(self.create_label("Tội danh *"), 3, 2)
        self.crime_edit = self.create_input(
            "VD: Trộm cắp tài sản"
        )
        layout.addWidget(self.crime_edit, 3, 3)
        
    def setup_case_info_section(self, parent_layout):
        """Setup case information section."""
        section = self.create_section("📋 THÔNG TIN ÁN", parent_layout)
        layout = QGridLayout(section)
        layout.setSpacing(15)
        
        # Row 1
        layout.addWidget(self.create_label("Loại án *"), 0, 0)
        # Lấy giá trị mới nhất từ enum CaseType
        from models.offender import CaseType
        self.case_type_combo = self.create_combo([
            case_type.value for case_type in CaseType
        ])
        layout.addWidget(self.case_type_combo, 0, 1)
        
        layout.addWidget(self.create_label("Số bản án *"), 0, 2)
        self.sentence_number_edit = self.create_input("VD: Số 15/2025/HS-ST, ngày 15/5/2025")
        layout.addWidget(self.sentence_number_edit, 0, 3)
        
        # Row 2
        layout.addWidget(self.create_label("Quyết định THA *"), 1, 0)
        self.decision_number_edit = self.create_input("VD: Số 15/2025/QĐ-CA, ngày 29/5/2025")
        layout.addWidget(self.decision_number_edit, 1, 1, 1, 3)
        
    def setup_sentence_info_section(self, parent_layout):
        """Setup sentence information section."""
        section = self.create_section("⏰ THÔNG TIN THI HÀNH ÁN", parent_layout)
        layout = QGridLayout(section)
        layout.setSpacing(15)
        
        # Row 1
        layout.addWidget(self.create_label("Ngày bắt đầu *"), 0, 0)
        self.start_date_input = self.create_date_edit()
        layout.addWidget(self.start_date_input, 0, 1)
        
        layout.addWidget(self.create_label("Thời gian TT (tháng) *"), 0, 2)
        self.duration_months_spin = self.create_spinbox(1, 60, 6)
        layout.addWidget(self.duration_months_spin, 0, 3)
        
        # Row 2
        layout.addWidget(self.create_label("Được giảm (tháng)"), 1, 0)
        self.reduced_months_spin = self.create_spinbox(0, 12, 0)
        layout.addWidget(self.reduced_months_spin, 1, 1)
        
        layout.addWidget(self.create_label("Ngày được giảm"), 1, 2)
        self.reduction_date_input = self.create_date_edit()
        layout.addWidget(self.reduction_date_input, 1, 3)
        
        # Row 3
        layout.addWidget(self.create_label("Số lần giảm"), 2, 0)
        self.reduction_count_spin = self.create_spinbox(
            0, 10, 0
        )
        layout.addWidget(self.reduction_count_spin, 2, 1)
        
    def setup_calculation_section(self, parent_layout):
        """Setup calculation results section."""
        section = self.create_section("🧮 TÍNH TOÁN TỰ ĐỘNG", parent_layout)
        layout = QGridLayout(section)
        layout.setSpacing(15)
        
        # Row 1
        layout.addWidget(self.create_label("Ngày chấp hành xong:"), 0, 0)
        self.completion_date_label = self.create_result_label("Chưa tính")
        layout.addWidget(self.completion_date_label, 0, 1)
        
        layout.addWidget(self.create_label("Trạng thái:"), 0, 2)
        self.status_label = self.create_result_label("Chưa xác định")
        layout.addWidget(self.status_label, 0, 3)
        
        # Row 2
        layout.addWidget(self.create_label("Số ngày còn lại:"), 1, 0)
        self.days_remaining_label = self.create_result_label("Chưa tính")
        layout.addWidget(self.days_remaining_label, 1, 1)
        
        layout.addWidget(self.create_label("Mức độ nguy cơ:"), 1, 2)
        self.risk_level_label = self.create_result_label("Chưa đánh giá")
        layout.addWidget(self.risk_level_label, 1, 3)
        
        # Row 3 - Gợi ý đợt giảm án tiếp theo
        self.next_reduction_hint = QLabel()
        self.next_reduction_hint.setObjectName("hintLabel")
        self.next_reduction_hint.setVisible(False)
        layout.addWidget(self.next_reduction_hint, 2, 0, 1, 4)
        
    def setup_notes_section(self, parent_layout):
        """Setup notes section."""
        section = self.create_section("📝 GHI CHÚ", parent_layout)
        layout = QVBoxLayout(section)
        
        self.notes_edit = QTextEdit()
        self.notes_edit.setPlaceholderText("Nhập ghi chú về đối tượng...")
        self.notes_edit.setMaximumHeight(100)
        self.notes_edit.setObjectName("notesEdit")
        # Xóa setStyleSheet inline, dùng QSS cho QTextEdit#notesEdit
        layout.addWidget(self.notes_edit)
        
    def setup_action_bar(self, parent_layout):
        """Setup bottom action bar."""
        action_frame = QFrame()
        action_frame.setObjectName("actionBar")
        # Xóa setStyleSheet inline, dùng QSS
        # action_frame.setStyleSheet(...)
        action_layout = QHBoxLayout(action_frame)
        action_layout.setContentsMargins(30, 15, 30, 15)
        # Hiệu ứng bóng đổ
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(16)
        shadow.setOffset(0, -2)
        shadow.setColor(QColor(0,0,0,40))
        action_frame.setGraphicsEffect(shadow)
        
        # Left side - Info
        info_label = QLabel("💡 Lưu ý: Các trường có dấu * là bắt buộc")
        info_label.setObjectName("infoLabel")
        # Xóa setStyleSheet inline, dùng QSS cho QLabel#infoLabel
        action_layout.addWidget(info_label)
        
        action_layout.addStretch()
        
        # Right side - Buttons
        self.cancel_btn = self.create_button("HỦY", "secondary")
        self.save_btn = self.create_button("LƯU", "primary")
        self.save_btn.setMinimumWidth(120)
        self.paste_auto_btn = QPushButton("📋 Dán tự động")
        self.paste_auto_btn.setToolTip("Tự động nhận diện và điền dữ liệu từ clipboard")
        self.paste_auto_btn.clicked.connect(self.paste_auto_fill)
        self.import_file_btn = QPushButton("📂 Nhập từ file")
        self.import_file_btn.setToolTip("Chọn file Excel, Word, PDF, TXT để tự động điền dữ liệu")
        self.import_file_btn.clicked.connect(self.import_file_fill)
        self.import_image_btn = QPushButton("🖼️ Nhập từ ảnh")
        self.import_image_btn.setToolTip("Chọn ảnh giấy tờ để nhận diện và điền dữ liệu (OCR)")
        self.import_image_btn.clicked.connect(self.import_image_fill)
        action_layout.addWidget(self.cancel_btn)
        action_layout.addWidget(self.save_btn)
        action_layout.addWidget(self.paste_auto_btn)
        action_layout.addWidget(self.import_file_btn)
        action_layout.addWidget(self.import_image_btn)
        
        parent_layout.addWidget(action_frame)
        
    def create_section(self, title: str, parent_layout):
        """Create a form section."""
        section = QGroupBox(title)
        section.setFont(QFont("Segoe UI", 14, QFont.Weight.Bold))
        section.setSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed
        )
        section.setObjectName("formSection")
        # Xóa setStyleSheet inline, dùng QSS cho QGroupBox#formSection
        parent_layout.addWidget(section)
        return section
        
    def create_label(self, text: str) -> QLabel:
        label = QLabel(text)
        label.setMinimumWidth(COMPONENT_SIZES['label_width'])
        label.setFont(QFont("Segoe UI", 13))
        return label

    def create_input(self, placeholder: str) -> QLineEdit:
        edit = QLineEdit()
        edit.setPlaceholderText(placeholder)
        edit.setMinimumWidth(COMPONENT_SIZES['input_width'])
        edit.setMinimumHeight(COMPONENT_SIZES['input_height'])
        edit.setFont(QFont("Segoe UI", 13))
        edit.setClearButtonEnabled(True)  # Nút X nhỏ bên phải
        edit.setSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed
        )
        return edit

    def create_combo(self, items: list) -> QComboBox:
        combo = QComboBox()
        combo.addItems(items)
        combo.setMinimumWidth(COMPONENT_SIZES['input_width'])
        combo.setMinimumHeight(COMPONENT_SIZES['input_height'])
        combo.setFont(QFont("Segoe UI", 13))
        combo.setSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed
        )
        return combo

    def create_date_edit(self) -> QDateEdit:
        date_edit = QDateEdit()
        date_edit.setDisplayFormat("dd/MM/yyyy")
        date_edit.setMinimumWidth(COMPONENT_SIZES['input_width'])
        date_edit.setMinimumHeight(COMPONENT_SIZES['input_height'])
        date_edit.setFont(QFont("Segoe UI", 13))
        date_edit.setCalendarPopup(True)
        date_edit.setSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed
        )
        return date_edit

    def create_spinbox(self, min_val: int, max_val: int, default: int) -> QSpinBox:
        spin = QSpinBox()
        spin.setRange(min_val, max_val)
        spin.setValue(default)
        spin.setMinimumWidth(COMPONENT_SIZES['input_width'])
        spin.setMinimumHeight(COMPONENT_SIZES['input_height'])
        spin.setFont(QFont("Segoe UI", 13))
        spin.setSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed
        )
        return spin

    def create_result_label(self, text: str) -> QLabel:
        """Create a result label."""
        label = QLabel(text)
        label.setFont(QFont("Segoe UI", 13, QFont.Weight.Bold))
        label.setObjectName("resultLabel")
        # Xóa setStyleSheet inline, dùng QSS cho QLabel#resultLabel
        return label
        
    def create_button(self, text: str, style: str = "primary") -> QPushButton:
        btn = QPushButton(text)
        if style == "primary":
            btn.setMinimumWidth(COMPONENT_SIZES['primary_button_width'])
            btn.setMinimumHeight(COMPONENT_SIZES['primary_button_height'])
        elif style == "secondary":
            btn.setMinimumWidth(COMPONENT_SIZES['secondary_button_width'])
            btn.setMinimumHeight(COMPONENT_SIZES['secondary_button_height'])
        else:
            btn.setMinimumWidth(COMPONENT_SIZES['button_width'])
            btn.setMinimumHeight(COMPONENT_SIZES['button_height'])
        btn.setFont(QFont("Segoe UI", 13, QFont.Weight.Bold))
        return btn
        
    def setup_connections(self):
        """Setup signal connections."""
        self.save_btn.clicked.connect(self.save_offender)
        self.cancel_btn.clicked.connect(self.cancel_edit)
        
        # Auto-calculate when relevant fields change
        self.start_date_input.dateChanged.connect(self.calculate_fields)
        self.duration_months_spin.valueChanged.connect(self.calculate_fields)
        self.reduced_months_spin.valueChanged.connect(self.calculate_fields)
        
        # Keyboard navigation: Enter chuyển focus, Shift+Tab quay lại, Enter cuối form sẽ lưu
        self.case_number_edit.returnPressed.connect(lambda: self.full_name_edit.setFocus())
        self.full_name_edit.returnPressed.connect(lambda: self.gender_combo.setFocus())
        self.birth_date_edit.installEventFilter(self)
        self.address_edit.returnPressed.connect(lambda: self.ward_edit.setFocus())
        self.ward_edit.returnPressed.connect(lambda: self.occupation_edit.setFocus())
        self.occupation_edit.returnPressed.connect(lambda: self.crime_edit.setFocus())
        self.crime_edit.returnPressed.connect(lambda: self.case_type_combo.setFocus())
        self.sentence_number_edit.returnPressed.connect(lambda: self.decision_number_edit.setFocus())
        self.decision_number_edit.returnPressed.connect(lambda: self.start_date_input.setFocus())
        self.start_date_input.installEventFilter(self)
        self.duration_months_spin.installEventFilter(self)
        self.reduced_months_spin.installEventFilter(self)
        self.reduction_date_input.installEventFilter(self)
        self.reduction_count_spin.installEventFilter(self)
        self.notes_edit.installEventFilter(self)
        
        self.case_number_edit.editingFinished.connect(self.auto_fill_by_case_number)
        self.full_name_edit.editingFinished.connect(self.auto_fill_by_full_name)
        # Chuẩn hóa & sửa lỗi chính tả khi rời khỏi các trường text
        for edit in [self.full_name_edit, self.address_edit, self.ward_edit, self.occupation_edit, self.crime_edit]:
            edit.editingFinished.connect(lambda e=edit: self.normalize_and_autocorrect(e))
        
    def load_offender(self, offender_id: int):
        """Load offender data for editing."""
        try:
            offender = self.offender_service.get_offender(offender_id)
            if offender:
                self.current_offender_id = offender_id
                self.populate_form(offender)
                self.calculate_fields()
        except Exception as e:
            QMessageBox.critical(self, "Lỗi", f"Không thể tải dữ liệu: {str(e)}")
            
    def populate_form(self, offender: Offender):
        """Populate form with offender data."""
        # Basic info
        self.case_number_edit.setText(offender.case_number)
        self.full_name_edit.setText(offender.full_name)
        self.gender_combo.setCurrentText(offender.gender.value)
        
        if offender.birth_date:
            self.birth_date_edit.setDate(QDate(offender.birth_date.year, 
                                              offender.birth_date.month, 
                                              offender.birth_date.day))
        
        self.address_edit.setText(offender.address)
        self.ward_edit.setText(offender.ward)
        self.occupation_edit.setText(offender.occupation)
        self.crime_edit.setText(offender.crime)
        self.case_type_combo.setCurrentText(offender.case_type.value)
        
        # Case info
        self.sentence_number_edit.setText(offender.sentence_number)
        self.decision_number_edit.setText(offender.decision_number)
        
        if offender.start_date:
            self.start_date_input.setDate(QDate(offender.start_date.year, 
                                             offender.start_date.month, 
                                             offender.start_date.day))
        
        self.duration_months_spin.setValue(offender.duration_months)
        self.reduced_months_spin.setValue(offender.reduced_months)
        
        if offender.reduction_date:
            self.reduction_date_input.setDate(QDate(offender.reduction_date.year, 
                                                 offender.reduction_date.month, 
                                                 offender.reduction_date.day))
        
        self.reduction_count_spin.setValue(offender.reduction_count)
        self.notes_edit.setPlainText(offender.notes)
        
    def save_offender(self):
        """Save offender data."""
        try:
            if not self.validate_form():
                return
                
            data = self.collect_form_data()
            
            if self.current_offender_id:
                # Update existing offender
                success = self.offender_service.update_offender(self.current_offender_id, data)
                if success:
                    QMessageBox.information(self, "Thành công", "Cập nhật đối tượng thành công!")
                    self.offender_saved.emit(self.current_offender_id)
                else:
                    QMessageBox.critical(self, "Lỗi", "Không thể cập nhật đối tượng!")
            else:
                # Create new offender
                offender = self.offender_service.create_offender(data)
                QMessageBox.information(self, "Thành công", "Thêm đối tượng thành công!")
                self.offender_saved.emit(offender.id)
                
        except Exception as e:
            QMessageBox.critical(self, "Lỗi", f"Không thể lưu đối tượng: {str(e)}")
            
    def validate_form(self) -> bool:
        """Validate form data và hiển thị lỗi trực quan."""
        valid = True
        # Reset lỗi
        self.case_number_edit.setProperty("error", False)
        self.full_name_edit.setProperty("error", False)
        self.gender_combo.setProperty("error", False)
        self.birth_date_edit.setProperty("error", False)
        self.address_edit.setProperty("error", False)
        self.ward_edit.setProperty("error", False)
        self.occupation_edit.setProperty("error", False)
        self.crime_edit.setProperty("error", False)
        self.case_type_combo.setProperty("error", False)
        self.sentence_number_edit.setProperty("error", False)
        self.decision_number_edit.setProperty("error", False)
        self.start_date_input.setProperty("error", False)
        self.duration_months_spin.setProperty("error", False)
        self.reduced_months_spin.setProperty("error", False)
        self.reduction_date_input.setProperty("error", False)
        self.reduction_count_spin.setProperty("error", False)
        self.notes_edit.setProperty("error", False)
        self.case_number_error.setVisible(False)
        self.full_name_error.setVisible(False)
        
        # Validate từng trường
        if not self.case_number_edit.text().strip():
            self.case_number_edit.setProperty("error", True)
            self.case_number_error.setText("Số hồ sơ không được để trống")
            self.case_number_error.setVisible(True)
            valid = False
        if not self.full_name_edit.text().strip():
            self.full_name_edit.setProperty("error", True)
            self.full_name_error.setText("Họ tên không được để trống")
            self.full_name_error.setVisible(True)
            valid = False
        if not self.gender_combo.currentText():
            self.gender_combo.setProperty("error", True)
            self.gender_combo.setCurrentIndex(0) # Reset to default
            valid = False
        if not self.birth_date_edit.date().toPyDate():
            self.birth_date_edit.setProperty("error", True)
            valid = False
        if not self.address_edit.text().strip():
            self.address_edit.setProperty("error", True)
            valid = False
        if not self.ward_edit.text().strip():
            self.ward_edit.setProperty("error", True)
            valid = False
        if not self.occupation_edit.text().strip():
            self.occupation_edit.setProperty("error", True)
            valid = False
        if not self.crime_edit.text().strip():
            self.crime_edit.setProperty("error", True)
            valid = False
        if not self.case_type_combo.currentText():
            self.case_type_combo.setProperty("error", True)
            self.case_type_combo.setCurrentIndex(0) # Reset to default
            valid = False
        if not self.sentence_number_edit.text().strip():
            self.sentence_number_edit.setProperty("error", True)
            valid = False
        if not self.decision_number_edit.text().strip():
            self.decision_number_edit.setProperty("error", True)
            valid = False
        if self.duration_months_spin.value() <= 0:
            self.duration_months_spin.setProperty("error", True)
            valid = False
            
        if not valid:
            QMessageBox.warning(self, "Lỗi validation", "Vui lòng kiểm tra lại các trường có dấu * và nhập đầy đủ thông tin.")
            return False
            
        return True
        
    def collect_form_data(self) -> Dict[str, Any]:
        """Collect data from form."""
        return {
            'case_number': self.case_number_edit.text().strip(),
            'full_name': self.full_name_edit.text().strip(),
            'gender': Gender(self.gender_combo.currentText()),
            'birth_date': self.birth_date_edit.date().toPyDate(),
            'address': self.address_edit.text().strip(),
            'ward': self.ward_edit.text().strip(),
            'occupation': self.occupation_edit.text().strip(),
            'crime': self.crime_edit.text().strip(),
            'case_type': CaseType(self.case_type_combo.currentText()),
            'sentence_number': self.sentence_number_edit.text().strip(),
            'decision_number': self.decision_number_edit.text().strip(),
            'start_date': self.start_date_input.date().toPyDate(),
            'duration_months': self.duration_months_spin.value(),
            'reduced_months': self.reduced_months_spin.value(),
            'reduction_date': self.reduction_date_input.date().toPyDate(),
            'reduction_count': self.reduction_count_spin.value(),
            'notes': self.notes_edit.toPlainText().strip()
        }
        
    def calculate_fields(self):
        """Calculate derived fields."""
        try:
            # Create temporary offender for calculation
            temp_data = self.collect_form_data()
            temp_offender = Offender(**temp_data)
            # Update calculated fields
            if temp_offender.completion_date:
                self.completion_date_label.setText(temp_offender.completion_date.strftime("%d/%m/%Y"))
            else:
                self.completion_date_label.setText("Chưa tính")
            # Thay đổi trạng thái label bằng objectName để QSS nhận diện
            status_val = temp_offender.status.value if hasattr(temp_offender.status, 'value') else str(temp_offender.status)
            if status_val == "Sắp kết thúc":
                self.status_label.setObjectName("statusLabelWarning")
                self.status_label.setText("<img src='assets/icons/warning.svg' width='18' style='vertical-align:middle;'/> <b style='color:#FF9800'>Sắp kết thúc</b>")
            elif status_val == "Đã hoàn thành":
                self.status_label.setObjectName("statusLabelSuccess")
                self.status_label.setText("<b style='color:#4CAF50'>Đã hoàn thành</b>")
            elif status_val == "Vi phạm":
                self.status_label.setObjectName("statusLabelError")
                self.status_label.setText("<img src='assets/icons/violation.svg' width='18' style='vertical-align:middle;'/> <b style='color:#F44336'>Vi phạm</b>")
            else:
                self.status_label.setObjectName("statusLabelInfo")
                self.status_label.setText(status_val)
            self.days_remaining_label.setText(f"{temp_offender.days_remaining} ngày")
            risk_val = temp_offender.risk_level.value if hasattr(temp_offender.risk_level, 'value') else str(temp_offender.risk_level)
            self.risk_level_label.setText(risk_val)
            # Gợi ý đợt giảm án tiếp theo
            next_reduction = temp_offender.get_next_reduction_date()
            if next_reduction:
                # Gợi ý các mốc 30/4, 2/9, 25/12 nếu gần các mốc này (±7 ngày)
                import datetime
                mocs = [(30,4), (2,9), (25,12)]
                hint = ""
                for d,m in mocs:
                    try:
                        moc_date = next_reduction.replace(day=d, month=m)
                        delta = abs((next_reduction - moc_date).days)
                        if delta <= 7:
                            hint = f" (Gợi ý đợt: {moc_date.strftime('%d/%m')})"
                            break
                    except Exception:
                        continue
                self.next_reduction_hint.setText(f"🛈 Đợt giảm án tiếp theo: {next_reduction.strftime('%d/%m/%Y')}{hint}")
                self.next_reduction_hint.setVisible(True)
            else:
                self.next_reduction_hint.setVisible(False)
        except Exception:
            # If calculation fails, show default values
            self.completion_date_label.setText("Chưa tính")
            self.status_label.setText("Chưa xác định")
            self.status_label.setStyleSheet("color: #1976D2; background-color: #E3F2FD; border: 1px solid #BBDEFB; border-radius: 6px; padding: 8px 12px; min-height: 45px;")
            self.days_remaining_label.setText("Chưa tính")
            self.risk_level_label.setText("Chưa đánh giá")
            self.next_reduction_hint.setVisible(False)
            
    def cancel_edit(self):
        """Cancel editing."""
        self.offender_cancelled.emit()
        
    def clear_form(self):
        """Clear form for new entry."""
        self.current_offender_id = None
        
        # Clear all fields
        self.case_number_edit.clear()
        self.full_name_edit.clear()
        self.gender_combo.setCurrentIndex(0)
        self.birth_date_edit.setDate(QDate.currentDate())
        self.address_edit.clear()
        self.ward_edit.clear()
        self.occupation_edit.clear()
        self.crime_edit.clear()
        self.case_type_combo.setCurrentIndex(0)
        
        self.sentence_number_edit.clear()
        self.decision_number_edit.clear()
        self.start_date_input.setDate(QDate.currentDate())
        self.duration_months_spin.setValue(6)
        self.reduced_months_spin.setValue(0)
        self.reduction_date_input.setDate(QDate.currentDate())
        self.reduction_count_spin.setValue(0)
        self.notes_edit.clear()
        
        # Reset calculated fields
        self.completion_date_label.setText("Chưa tính")
        self.status_label.setText("Chưa xác định")
        self.status_label.setStyleSheet("color: #1976D2; background-color: #E3F2FD; border: 1px solid #BBDEFB; border-radius: 6px; padding: 8px 12px; min-height: 45px;")
        self.days_remaining_label.setText("Chưa tính")
        self.risk_level_label.setText("Chưa đánh giá")
        self.next_reduction_hint.setVisible(False) 

    def auto_extract_ward_from_address(self):
        """Tự động tách phường/xã từ địa chỉ nếu trường ward đang trống."""
        if self.ward_edit.text().strip():
            return
        address = self.address_edit.text().strip()
        import re
        # Regex tìm phường/xã phổ biến
        match = re.search(r"(?:P\.?|Phường|X\.?|Xã)\s*([\wÀ-ỹ\s]+)", address)
        if match:
            ward = match.group(1).strip()
            self.ward_edit.setText(ward)
        else:
            # Nếu không có, thử tách phần sau dấu phẩy cuối cùng
            parts = [p.strip() for p in address.split(',') if p.strip()]
            if parts:
                self.ward_edit.setText(parts[-1])
    def refresh_ward_completer(self):
        """Lấy danh sách ward từ database, file chuẩn (wards.json), và cập nhật completer (ưu tiên phổ biến nhất lên đầu)."""
        try:
            offenders = self.offender_service.get_all_offenders()
            ward_freq = {}
            for offender in offenders:
                if hasattr(offender, 'ward') and offender.ward:
                    w = offender.ward.strip()
                    if w:
                        ward_freq[w] = ward_freq.get(w, 0) + 1
            # Đọc danh sách chuẩn từ wards.json nếu có
            wards_file = os.path.join(os.path.dirname(__file__), '../assets/wards.json')
            wards_list = []
            if os.path.exists(wards_file):
                with open(wards_file, encoding='utf-8') as f:
                    wards_list = json.load(f)
            # Gộp danh sách, ưu tiên chuẩn, sau đó các ward đã nhập
            all_wards = list(wards_list)
            for w in ward_freq:
                if w not in all_wards:
                    all_wards.append(w)
            # Sắp xếp: phổ biến nhất lên đầu
            all_wards = sorted(all_wards, key=lambda x: -ward_freq.get(x, 0))
            self.ward_completer.setModel(QStringListModel(all_wards))
        except Exception:
            pass

    def showEvent(self, event):
        super().showEvent(event)
        self.refresh_ward_completer()

    def eventFilter(self, obj, event):
        from PyQt6.QtCore import QEvent, Qt
        if obj == self.ward_edit and event.type() == QEvent.Type.FocusOut:
            # Khi rời khỏi trường ward, kiểm tra gần đúng
            text = self.ward_edit.text().strip()
            if text:
                model = self.ward_completer.model()
                if model:
                    from difflib import get_close_matches
                    all_wards = [model.data(model.index(i)) for i in range(model.rowCount())]
                    matches = get_close_matches(text, all_wards, n=1, cutoff=0.85)
                    if matches:
                        self.ward_edit.setText(matches[0])
        # Bổ sung cho QComboBox, QDateEdit, QSpinBox: Enter chuyển focus
        if event.type() == QEvent.Type.KeyPress and event.key() == Qt.Key.Key_Return:
            if obj == self.gender_combo:
                self.birth_date_edit.setFocus()
                return True
            if obj == self.birth_date_edit:
                self.address_edit.setFocus()
                return True
            if obj == self.address_edit:
                self.ward_edit.setFocus()
                return True
            if obj == self.ward_edit:
                self.occupation_edit.setFocus()
                return True
            if obj == self.occupation_edit:
                self.crime_edit.setFocus()
                return True
            if obj == self.crime_edit:
                self.case_type_combo.setFocus()
                return True
            if obj == self.case_type_combo:
                self.sentence_number_edit.setFocus()
                return True
            if obj == self.sentence_number_edit:
                self.decision_number_edit.setFocus()
                return True
            if obj == self.decision_number_edit:
                self.start_date_input.setFocus()
                return True
            if obj == self.start_date_input:
                self.duration_months_spin.setFocus()
                return True
            if obj == self.duration_months_spin:
                self.reduced_months_spin.setFocus()
                return True
            if obj == self.reduced_months_spin:
                self.reduction_date_input.setFocus()
                return True
            if obj == self.reduction_date_input:
                self.reduction_count_spin.setFocus()
                return True
            if obj == self.reduction_count_spin:
                self.notes_edit.setFocus()
                return True
        return super().eventFilter(obj, event) 

    def paste_auto_fill(self):
        """Tự động nhận diện và điền dữ liệu từ clipboard (text)."""
        import pyperclip
        text = pyperclip.paste()
        self.smart_fill_from_text(text)
    def import_file_fill(self):
        """Chọn file (Excel, Word, PDF, TXT) và tự động điền dữ liệu."""
        file_path, _ = QFileDialog.getOpenFileName(self, "Chọn file dữ liệu", "", "All Files (*.xlsx *.xls *.csv *.docx *.pdf *.txt)")
        if not file_path:
            return
        ext = file_path.split('.')[-1].lower()
        text = ""
        try:
            if ext in ["xlsx", "xls", "csv"]:
                df = pd.read_excel(file_path) if ext != "csv" else pd.read_csv(file_path)
                text = "\n".join([str(val) for val in df.values.flatten() if pd.notnull(val)])
            elif ext == "docx":
                doc = docx.Document(file_path)
                text = "\n".join([p.text for p in doc.paragraphs])
            elif ext == "pdf":
                with pdfplumber.open(file_path) as pdf:
                    text = "\n".join(page.extract_text() or '' for page in pdf.pages)
            elif ext == "txt":
                with open(file_path, encoding='utf-8') as f:
                    text = f.read()
        except Exception as e:
            QMessageBox.critical(self, "Lỗi", f"Không thể đọc file: {e}")
            return
        self.smart_fill_from_text(text)
    def import_image_fill(self):
        """Chọn ảnh giấy tờ, dùng OCR nhận diện và điền dữ liệu."""
        file_path, _ = QFileDialog.getOpenFileName(self, "Chọn ảnh giấy tờ", "", "Image Files (*.png *.jpg *.jpeg *.bmp)")
        if not file_path:
            return
        try:
            img = Image.open(file_path)
            text = pytesseract.image_to_string(img, lang='vie')
        except Exception as e:
            QMessageBox.critical(self, "Lỗi", f"Không thể nhận diện ảnh: {e}")
            return
        self.smart_fill_from_text(text)
    def smart_fill_from_text(self, text):
        """Phân tích text, mapping thông minh vào các trường form, ưu tiên AI/NER và fuzzy matching."""
        # 1. Nhận diện thực thể bằng underthesea
        entities = ner(text)
        field_map = {
            'PERSON': 'full_name',
            'DATE': 'birth_date',
            'LOC': 'address',
            # ... có thể mở rộng mapping ...
        }
        mapped = {}
        for ent in entities:
            value = ent[0].strip()
            label = ent[3]
            field = field_map.get(label)
            if field:
                if field not in mapped:
                    mapped[field] = []
                mapped[field].append(value)
        # 2. Fuzzy matching cho các trường đặc thù
        # Ví dụ: mapping tội danh, loại án, phường/xã
        # Lấy danh sách chuẩn từ completer/model
        def fuzzy_field(field, value, model):
            if not value or not model:
                return value
            choices = [model.data(model.index(i)) for i in range(model.rowCount())]
            match, score = process.extractOne(value, choices)
            if score >= 85:
                return match
            # Nếu không chắc chắn, hỏi người dùng
            if score >= 60:
                chosen, ok = QInputDialog.getItem(self, f"Chọn {field}", f"AI nhận diện: '{value}'. Chọn giá trị đúng:", choices, editable=True)
                if ok:
                    return chosen
            return value
        # 3. Mapping vào form, ưu tiên xác suất cao, hỏi người dùng nếu nhiều khả năng
        for field, vals in mapped.items():
            val = vals[0]
            if len(vals) > 1:
                val, ok = QInputDialog.getItem(self, f"Chọn {field}", f"AI nhận diện nhiều giá trị cho {field}. Chọn đúng:", vals, editable=True)
                if not ok:
                    continue
            if field == 'full_name' and hasattr(self, 'full_name_edit'):
                self.full_name_edit.setText(val)
            elif field == 'birth_date' and hasattr(self, 'birth_date_edit'):
                # Chuẩn hóa ngày tháng
                import re
                from datetime import datetime
                date_val = val
                # Nhận diện dd/mm/yyyy hoặc yyyy-mm-dd
                m = re.search(r'(\d{1,2}[/-]\d{1,2}[/-]\d{2,4})', date_val)
                if m:
                    try:
                        d = m.group(1).replace('-', '/').replace('.', '/')
                        dt = datetime.strptime(d, '%d/%m/%Y') if len(d.split('/')[2]) == 4 else datetime.strptime(d, '%d/%m/%y')
                        self.birth_date_edit.setDate(QDate(dt.year, dt.month, dt.day))
                    except Exception:
                        pass
            elif field == 'address' and hasattr(self, 'address_edit'):
                self.address_edit.setText(val)
        # Fuzzy cho các trường đặc thù
        # Tội danh
        if hasattr(self, 'crime_edit'):
            model = getattr(self, 'crime_edit').completer().model() if getattr(self, 'crime_edit').completer() else None
            crime_val = fuzzy_field('Tội danh', self.crime_edit.text(), model)
            self.crime_edit.setText(crime_val)
        # Loại án
        if hasattr(self, 'case_type_combo'):
            model = self.case_type_combo.model() if self.case_type_combo else None
            case_type_val = fuzzy_field('Loại án', self.case_type_combo.currentText(), model)
            self.case_type_combo.setCurrentText(case_type_val)
        # Phường/xã
        if hasattr(self, 'ward_edit'):
            model = getattr(self, 'ward_edit').completer().model() if getattr(self, 'ward_edit').completer() else None
            ward_val = fuzzy_field('Phường/xã', self.ward_edit.text(), model)
            self.ward_edit.setText(ward_val)
    def auto_fill_by_case_number(self):
        """Nếu nhập số hồ sơ trùng với bản ghi cũ, tự động điền các trường còn lại."""
        case_number = self.case_number_edit.text().strip()
        if not case_number:
            return
        offenders = self.offender_service.get_all_offenders()
        for offender in offenders:
            if offender.case_number == case_number:
                self.populate_form(offender)
                break
    def auto_fill_by_full_name(self):
        """Nếu nhập họ tên trùng với bản ghi cũ, gợi ý điền các trường còn lại."""
        full_name = self.full_name_edit.text().strip()
        if not full_name:
            return
        offenders = self.offender_service.get_all_offenders()
        for offender in offenders:
            if offender.full_name.lower() == full_name.lower():
                # Gợi ý điền các trường còn lại (không ghi đè họ tên)
                self.gender_combo.setCurrentText(offender.gender.value if hasattr(offender.gender, 'value') else str(offender.gender))
                if offender.birth_date:
                    self.birth_date_edit.setDate(QDate(offender.birth_date.year, offender.birth_date.month, offender.birth_date.day))
                self.address_edit.setText(offender.address)
                self.ward_edit.setText(offender.ward)
                self.occupation_edit.setText(offender.occupation)
                self.crime_edit.setText(offender.crime)
                self.case_type_combo.setCurrentText(offender.case_type.value if hasattr(offender.case_type, 'value') else str(offender.case_type))
                self.sentence_number_edit.setText(offender.sentence_number)
                self.decision_number_edit.setText(offender.decision_number)
                break
    def normalize_and_autocorrect(self, edit):
        """Chuẩn hóa và sửa lỗi chính tả cho trường text khi rời khỏi trường."""
        text = edit.text().strip()
        if not text:
            return
        spell = Speller(lang='vi')
        # Viết hoa đầu dòng, loại bỏ ký tự thừa, sửa lỗi chính tả
        text = text.capitalize()
        text = spell(text)
        edit.setText(text)
    # Hướng dẫn cài đặt thư viện cần thiết
    '''
    # Để sử dụng tính năng tự động hóa nhập liệu thông minh, hãy cài các thư viện sau:
    pip install pandas openpyxl python-docx pdfplumber pillow pytesseract autocorrect pyperclip
    # Nếu dùng OCR tiếng Việt, cần cài thêm gói ngôn ngữ cho Tesseract:
    # https://github.com/tesseract-ocr/tessdata/blob/main/vie.traineddata
    ''' 
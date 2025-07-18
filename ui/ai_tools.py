#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AI Tools widget for risk prediction and analysis.
"""

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QGridLayout, QLabel, 
    QLineEdit, QComboBox, QPushButton, QTextEdit, QTabWidget,
    QGroupBox, QFrame, QScrollArea, QSizePolicy
)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont

from typing import List, Optional

from constants import UI_LAYOUT
from models.offender import Offender, RiskLevel
from services.offender_service import OffenderService
from services.ai_service import AIService


class AIToolsWidget(QWidget):
    """Widget for AI-powered tools and analysis."""
    
    def __init__(self, offender_service: OffenderService, 
                 ai_service: AIService, parent=None):
        """Initialize AI tools widget."""
        super().__init__(parent)
        self.offender_service = offender_service
        self.ai_service = ai_service
        self.setup_ui()
        self.setup_connections()
        
    def setup_ui(self):
        """Setup user interface."""
        # Main layout
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(12, 12, 12, 12)
        main_layout.setSpacing(10)
        
        # Title
        title_label = QLabel("🤖 AI TOOLS - CÔNG CỤ THÔNG MINH")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label.setFont(QFont("Segoe UI", 18, QFont.Weight.Bold))
        title_label.setObjectName("sectionTitle")  # Đảm bảo nhận QSS động
        main_layout.addWidget(title_label)
        
        # Tab widget
        self.tab_widget = QTabWidget()
        main_layout.addWidget(self.tab_widget)
        
        # Create tabs
        self.setup_risk_prediction_tab()
        self.setup_chatbot_tab()
        self.setup_trend_analysis_tab()
        main_layout.addStretch()  # Đảm bảo co giãn full chiều dọc
        
    def setup_risk_prediction_tab(self):
        """Setup risk prediction tab."""
        risk_widget = QWidget()
        risk_widget.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        risk_layout = QVBoxLayout(risk_widget)
        risk_layout.setContentsMargins(12, 12, 12, 12)
        risk_layout.setSpacing(10)
        
        # Offender selection
        selection_group = QGroupBox("Chọn đối tượng để dự đoán")
        selection_group.setFont(QFont("Segoe UI", 13, QFont.Weight.Bold))
        selection_layout = QHBoxLayout(selection_group)
        
        self.offender_combo = QComboBox()
        self.offender_combo.setMinimumHeight(35)
        self.offender_combo.addItem("Chọn đối tượng...")
        
        self.predict_button = QPushButton("DỰ ĐOÁN")
        self.predict_button.setMinimumHeight(35)
        self.predict_button.setFont(QFont("Segoe UI", 12, QFont.Weight.Bold))
        
        selection_layout.addWidget(QLabel("Đối tượng:"))
        selection_layout.addWidget(self.offender_combo)
        selection_layout.addWidget(self.predict_button)
        
        risk_layout.addWidget(selection_group)
        
        # Results
        results_group = QGroupBox("Kết quả dự đoán")
        results_group.setFont(QFont("Segoe UI", 13, QFont.Weight.Bold))
        results_layout = QVBoxLayout(results_group)
        
        self.risk_result_label = QLabel("Chưa có kết quả dự đoán")
        self.risk_result_label.setObjectName("riskResultLabel")
        
        self.risk_factors_label = QLabel("")
        self.risk_factors_label.setWordWrap(True)
        results_layout.addWidget(self.risk_factors_label)
        
        self.recommendations_label = QLabel("")
        self.recommendations_label.setWordWrap(True)
        results_layout.addWidget(self.recommendations_label)
        
        risk_layout.addWidget(results_group)
        
        self.tab_widget.addTab(risk_widget, "Dự đoán nguy cơ")
        
    def setup_chatbot_tab(self):
        """Setup chatbot tab."""
        chatbot_widget = QWidget()
        chatbot_widget.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        chatbot_layout = QVBoxLayout(chatbot_widget)
        chatbot_layout.setContentsMargins(12, 12, 12, 12)
        chatbot_layout.setSpacing(10)
        
        # Chat history
        history_group = QGroupBox("Lịch sử chat")
        history_group.setFont(QFont("Segoe UI", 13, QFont.Weight.Bold))
        history_layout = QVBoxLayout(history_group)
        
        self.chat_history = QTextEdit()
        self.chat_history.setReadOnly(True)
        self.chat_history.setMaximumHeight(300)
        self.chat_history.setObjectName("chatHistory")
        
        # Add initial message
        self.chat_history.append("Bot: Xin chào! Tôi có thể giúp gì cho bạn?")
        
        history_layout.addWidget(self.chat_history)
        chatbot_layout.addWidget(history_group)
        
        # Input area
        input_group = QGroupBox("Nhập câu hỏi")
        input_group.setFont(QFont("Segoe UI", 13, QFont.Weight.Bold))
        input_layout = QHBoxLayout(input_group)
        
        self.question_input = QLineEdit()
        self.question_input.setPlaceholderText("Nhập câu hỏi của bạn...")
        self.question_input.setMinimumHeight(35)
        
        self.send_button = QPushButton("GỬI")
        self.send_button.setMinimumHeight(35)
        self.send_button.setFont(QFont("Segoe UI", 12, QFont.Weight.Bold))
        
        self.voice_button = QPushButton("🎤")
        self.voice_button.setMinimumHeight(35)
        self.voice_button.setMaximumWidth(50)
        
        input_layout.addWidget(self.question_input)
        input_layout.addWidget(self.send_button)
        input_layout.addWidget(self.voice_button)
        
        chatbot_layout.addWidget(input_group)
        
        self.tab_widget.addTab(chatbot_widget, "Chatbot hỗ trợ")
        
    def setup_trend_analysis_tab(self):
        """Setup trend analysis tab."""
        trend_widget = QWidget()
        trend_widget.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        trend_layout = QVBoxLayout(trend_widget)
        trend_layout.setContentsMargins(12, 12, 12, 12)
        trend_layout.setSpacing(10)
        
        # Analysis controls
        controls_group = QGroupBox("Thiết lập phân tích")
        controls_group.setFont(QFont("Segoe UI", 13, QFont.Weight.Bold))
        controls_layout = QGridLayout(controls_group)
        
        self.time_period_combo = QComboBox()
        self.time_period_combo.addItems(["Tháng", "Quý", "Năm"])
        self.time_period_combo.setMinimumHeight(35)
        
        self.analyze_button = QPushButton("PHÂN TÍCH")
        self.analyze_button.setMinimumHeight(35)
        self.analyze_button.setFont(QFont("Segoe UI", 12, QFont.Weight.Bold))
        
        controls_layout.addWidget(QLabel("Thời gian:"), 0, 0)
        controls_layout.addWidget(self.time_period_combo, 0, 1)
        controls_layout.addWidget(self.analyze_button, 0, 2)
        
        trend_layout.addWidget(controls_group)
        
        # Analysis results
        results_group = QGroupBox("Kết quả phân tích")
        results_group.setFont(QFont("Segoe UI", 13, QFont.Weight.Bold))
        results_layout = QVBoxLayout(results_group)
        
        self.trend_result_label = QLabel("Chưa có kết quả phân tích")
        self.trend_result_label.setObjectName("trendResultLabel")
        
        trend_layout.addWidget(results_group)
        
        self.tab_widget.addTab(trend_widget, "Phân tích xu hướng")
        
    def setup_connections(self):
        """Setup signal connections."""
        self.predict_button.clicked.connect(self.predict_risk)
        self.send_button.clicked.connect(self.send_message)
        self.question_input.returnPressed.connect(self.send_message)
        self.analyze_button.clicked.connect(self.analyze_trends)
        
    def load_offenders(self):
        """Load offenders into combo box."""
        try:
            offenders = self.offender_service.get_all_offenders()
            self.offender_combo.clear()
            self.offender_combo.addItem("Chọn đối tượng...")
            
            for offender in offenders:
                display_text = f"{offender.case_number} - {offender.full_name}"
                self.offender_combo.addItem(display_text, offender.id)
                
        except Exception as e:
            print(f"Error loading offenders: {e}")
            
    def predict_risk(self):
        """Predict risk for selected offender."""
        try:
            current_index = self.offender_combo.currentIndex()
            if current_index <= 0:
                self.risk_result_label.setText("Vui lòng chọn một đối tượng")
                return
                
            offender_id = self.offender_combo.currentData()
            if not offender_id:
                return
                
            offender = self.offender_service.get_offender(offender_id)
            if not offender:
                self.risk_result_label.setText("Không tìm thấy đối tượng")
                return
                
            # Get AI prediction
            prediction = self.ai_service.predict_risk(offender)
            
            # Update results
            risk_val = prediction['risk_level'].value if hasattr(prediction['risk_level'], 'value') else str(prediction['risk_level'])
            risk_text = f"Nguy cơ: {risk_val} ({prediction['risk_percentage']:.1f}%)"
            self.risk_result_label.setText(risk_text)
            self.risk_result_label.setStyleSheet("color: #1976D2; font-weight: bold;")
            
            # Show risk factors
            factors_text = "Yếu tố ảnh hưởng:\n" + "\n".join([f"• {factor}" for factor in prediction['risk_factors']])
            self.risk_factors_label.setText(factors_text)
            self.risk_factors_label.setStyleSheet("color: #424242;")
            
            # Show recommendations
            recommendations_text = "Khuyến nghị:\n" + "\n".join([f"• {rec}" for rec in prediction['recommendations']])
            self.recommendations_label.setText(recommendations_text)
            self.recommendations_label.setStyleSheet("color: #1976D2; font-weight: bold;")
            
        except Exception as e:
            self.risk_result_label.setText(f"Lỗi dự đoán: {str(e)}")
            self.risk_result_label.setStyleSheet("color: #F44336;")
            
    def send_message(self):
        """Send message to chatbot."""
        question = self.question_input.text().strip()
        if not question:
            return
            
        # Add user message to chat
        self.chat_history.append(f"User: {question}")
        
        # Get AI response
        try:
            response = self.ai_service.chatbot_response(question)
            self.chat_history.append(f"Bot: {response}")
        except Exception as e:
            self.chat_history.append(f"Bot: Xin lỗi, tôi không thể trả lời câu hỏi này.")
            
        # Clear input
        self.question_input.clear()
        
        # Scroll to bottom
        scrollbar = self.chat_history.verticalScrollBar()
        scrollbar.setValue(scrollbar.maximum())
        
    def analyze_trends(self):
        """Analyze trends in offender data."""
        try:
            offenders = self.offender_service.get_all_offenders()
            trends = self.ai_service.analyze_trends(offenders)
            
            if not trends:
                self.trend_result_label.setText("Không có dữ liệu để phân tích")
                return
                
            # Format trend results
            trend_text = f"""
            Tổng số đối tượng: {trends.get('total_offenders', 0)}
            
            Phân bố trạng thái:
            • Đang chấp hành: {trends.get('status_distribution', {}).get('active', 0)}
            • Đã hoàn thành: {trends.get('status_distribution', {}).get('completed', 0)}
            • Vi phạm: {trends.get('status_distribution', {}).get('violations', 0)}
            
            Phân bố nguy cơ:
            • Cao: {trends.get('risk_distribution', {}).get('high', 0)}
            • Trung bình: {trends.get('risk_distribution', {}).get('medium', 0)}
            • Thấp: {trends.get('risk_distribution', {}).get('low', 0)}
            
            Tỷ lệ hoàn thành: {trends.get('completion_rate', 0):.1f}%
            Tỷ lệ vi phạm: {trends.get('violation_rate', 0):.1f}%
            """
            
            self.trend_result_label.setText(trend_text)
            self.trend_result_label.setStyleSheet("color: #1976D2; font-weight: bold;")
            
        except Exception as e:
            self.trend_result_label.setText(f"Lỗi phân tích: {str(e)}")
            self.trend_result_label.setStyleSheet("color: #F44336;")
            
    def refresh_data(self):
        """Refresh AI tools data."""
        self.load_offenders()
        
    def showEvent(self, event):
        """Handle show event."""
        super().showEvent(event)
        self.refresh_data() 
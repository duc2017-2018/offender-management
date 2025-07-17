"""
Global stylesheet for the application.
"""

STYLE_SHEET = """
/* Global Styles */
QWidget {
    font-family: 'Segoe UI', Arial, sans-serif;
    font-size: 13px;
}

/* Main Window */
QMainWindow {
    background-color: #F8FAFC;
}

/* Buttons */
QPushButton {
    background-color: #1976D2;
    color: white;
    border: none;
    border-radius: 8px;
    padding: 6px 12px;
    min-height: 32px;
    max-height: 40px;
    font-weight: bold;
}

QPushButton:hover {
    background-color: #1565C0;
}

QPushButton:pressed {
    background-color: #0D47A1;
}

QPushButton:disabled {
    background-color: #BDBDBD;
    color: #757575;
}

/* Secondary Button */
QPushButton[class="secondary"] {
    background-color: #F44336;
}

QPushButton[class="secondary"]:hover {
    background-color: #D32F2F;
}

/* Input Fields */
QLineEdit, QComboBox, QDateEdit, QSpinBox {
    padding: 4px 8px;
    border: 1px solid #ccc;
    border-radius: 6px;
    min-height: 32px;
    background-color: white;
}

QLineEdit:focus, QComboBox:focus, QDateEdit:focus, QSpinBox:focus {
    border: 1px solid #007ACC;
    outline: none;
}

QLineEdit:disabled, QComboBox:disabled, QDateEdit:disabled, QSpinBox:disabled {
    background-color: #F5F5F5;
    color: #757575;
}

/* ComboBox */
QComboBox::drop-down {
    border: none;
    width: 20px;
}

QComboBox::down-arrow {
    image: url(assets/arrow_down.png);
    width: 12px;
    height: 12px;
}

/* Table */
QTableWidget {
    background-color: white;
    alternate-background-color: #F5F5F5;
    gridline-color: #E0E0E0;
    border: 1px solid #E0E0E0;
    border-radius: 6px;
}

QTableWidget::item {
    padding: 8px;
    border-bottom: 1px solid #E0E0E0;
}

QTableWidget::item:selected {
    background-color: #E3F2FD;
    color: #1976D2;
}

QHeaderView::section {
    background-color: #F5F5F5;
    padding: 8px;
    border: none;
    border-bottom: 2px solid #E0E0E0;
    font-weight: bold;
    color: #424242;
}

/* Tab Widget */
QTabWidget::pane {
    border: 1px solid #E0E0E0;
    border-radius: 6px;
    background-color: white;
}

QTabBar::tab {
    background-color: #F5F5F5;
    padding: 6px 12px;
    border: 1px solid #E0E0E0;
    border-bottom: none;
    border-top-left-radius: 6px;
    border-top-right-radius: 6px;
    margin-right: 2px;
}

QTabBar::tab:selected {
    background-color: white;
    border-bottom: 2px solid #1976D2;
    font-weight: bold;
}

QTabBar::tab:hover {
    background-color: #E3F2FD;
}

/* Group Box */
QGroupBox {
    font-weight: bold;
    border: 2px solid #E0E0E0;
    border-radius: 8px;
    margin-top: 10px;
    padding-top: 10px;
}

QGroupBox::title {
    subcontrol-origin: margin;
    left: 10px;
    padding: 0 5px 0 5px;
    color: #424242;
}

/* Scroll Area */
QScrollArea {
    border: 1px solid #E0E0E0;
    border-radius: 6px;
    background-color: white;
}

QScrollBar:vertical {
    background-color: #F5F5F5;
    width: 12px;
    border-radius: 6px;
}

QScrollBar::handle:vertical {
    background-color: #BDBDBD;
    border-radius: 6px;
    min-height: 20px;
}

QScrollBar::handle:vertical:hover {
    background-color: #9E9E9E;
}

/* Menu Bar */
QMenuBar {
    background-color: white;
    border-bottom: 1px solid #E0E0E0;
}

QMenuBar::item {
    background-color: transparent;
    padding: 8px 12px;
}

QMenuBar::item:selected {
    background-color: #E3F2FD;
    color: #1976D2;
}

QMenu {
    background-color: white;
    border: 1px solid #E0E0E0;
    border-radius: 6px;
    padding: 5px;
}

QMenu::item {
    padding: 8px 20px;
    border-radius: 4px;
}

QMenu::item:selected {
    background-color: #E3F2FD;
    color: #1976D2;
}

/* Status Bar */
QStatusBar {
    background-color: #F5F5F5;
    border-top: 1px solid #E0E0E0;
    color: #424242;
}

/* Dialog */
QDialog {
    background-color: #F8FAFC;
}

/* Message Box */
QMessageBox {
    background-color: white;
}

QMessageBox QPushButton {
    min-width: 80px;
    min-height: 30px;
}

/* Tool Tips */
QToolTip {
    background-color: #424242;
    color: white;
    border: none;
    border-radius: 4px;
    padding: 5px;
}

/* Progress Bar */
QProgressBar {
    border: 1px solid #E0E0E0;
    border-radius: 6px;
    text-align: center;
    background-color: #F5F5F5;
}

QProgressBar::chunk {
    background-color: #1976D2;
    border-radius: 5px;
}

/* Check Box */
QCheckBox {
    spacing: 8px;
}

QCheckBox::indicator {
    width: 16px;
    height: 16px;
    border: 2px solid #E0E0E0;
    border-radius: 3px;
    background-color: white;
}

QCheckBox::indicator:checked {
    background-color: #1976D2;
    border-color: #1976D2;
}

/* Radio Button */
QRadioButton {
    spacing: 8px;
}

QRadioButton::indicator {
    width: 16px;
    height: 16px;
    border: 2px solid #E0E0E0;
    border-radius: 8px;
    background-color: white;
}

QRadioButton::indicator:checked {
    background-color: #1976D2;
    border-color: #1976D2;
}

/* Text Edit */
QTextEdit {
    border: 1px solid #E0E0E0;
    border-radius: 6px;
    padding: 8px;
    background-color: white;
}

QTextEdit:focus {
    border: 1px solid #007ACC;
}

/* Label */
QLabel {
    color: #424242;
}

QLabel[class="title"] {
    font-size: 18px;
    font-weight: bold;
    color: #1976D2;
}

QLabel[class="subtitle"] {
    font-size: 14px;
    font-weight: bold;
    color: #424242;
}

/* Frame */
QFrame {
    border: 1px solid #E0E0E0;
    border-radius: 6px;
    background-color: white;
}

QFrame[class="card"] {
    border: 2px solid #E0E0E0;
    border-radius: 8px;
    background-color: white;
}

/* Status Colors */
QLabel[status="active"] {
    color: #4CAF50;
    font-weight: bold;
}

QLabel[status="warning"] {
    color: #FF9800;
    font-weight: bold;
}

QLabel[status="error"] {
    color: #F44336;
    font-weight: bold;
}

QLabel[status="completed"] {
    color: #9E9E9E;
    font-weight: bold;
}

/* Risk Colors */
QLabel[risk="low"] {
    color: #4CAF50;
    font-weight: bold;
}

QLabel[risk="medium"] {
    color: #FF9800;
    font-weight: bold;
}

QLabel[risk="high"] {
    color: #F44336;
    font-weight: bold;
}
""" 
import pytest
from unittest.mock import MagicMock
from PyQt6.QtWidgets import QApplication
from ui.main_window import MainWindow

@pytest.fixture
def main_window(qtbot):
    user_service = MagicMock()
    ai_service = MagicMock()
    report_service = MagicMock()
    offender_service = MagicMock()
    # Truyền đủ các service theo đúng thứ tự constructor MainWindow
    window = MainWindow(user_service, ai_service, report_service, offender_service)
    qtbot.addWidget(window)
    return window

def test_sidebar_mini_mode(main_window, qtbot):
    main_window.sidebar.set_mini_mode(True)
    assert main_window.sidebar.is_mini_mode()
    main_window.sidebar.set_mini_mode(False)
    assert not main_window.sidebar.is_mini_mode()

def test_header_sticky(main_window):
    assert main_window.header.is_sticky() 
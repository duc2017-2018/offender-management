#!/usr/bin/env python3
"""
Main application entry point for the Offender Management System.
"""

import sys
import os
from pathlib import Path
import traceback

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from PyQt6.QtWidgets import QApplication, QMessageBox
from PyQt6.QtCore import Qt, QTranslator, QLocale
from PyQt6.QtGui import QFont, QIcon

from database.database_manager import DatabaseManager
from database.migrations import create_tables, create_default_admin
from services.offender_service import OffenderService
from services.user_service import UserService
from services.ai_service import AIService
from services.report_service import ReportService
from ui.login_dialog import LoginDialog
from ui.main_window import MainWindow
from constants import UI_LAYOUT, APP_INFO


class OffenderManagementApp:
    """Main application class."""
    
    def __init__(self):
        """Initialize the application."""
        self.app = QApplication(sys.argv)
        self.setup_application()
        
        # Initialize database
        self.initialize_database()
        
        # Initialize services
        self.db_manager = DatabaseManager()
        self.offender_service = OffenderService(self.db_manager)
        self.user_service = UserService(self.db_manager)
        self.ai_service = AIService()
        self.report_service = ReportService()
        
        # Initialize additional services
        from services.excel_service import ExcelService
        from services.document_service import DocumentService
        self.excel_service = ExcelService(self.offender_service)
        self.document_service = DocumentService()
        
        # Initialize UI
        self.login_dialog = None
        self.main_window = None
        
    def setup_application(self):
        """Setup application properties."""
        # Set application info
        self.app.setApplicationName(APP_INFO['name'])
        self.app.setApplicationVersion(APP_INFO['version'])
        self.app.setOrganizationName(APP_INFO['organization'])
        
        # Set application icon
        icon_path = Path("assets/logo_cand.png")
        if icon_path.exists():
            self.app.setWindowIcon(QIcon(str(icon_path)))
        
        # Set application style - LUÔN dùng style.qss
        try:
            with open("assets/styles/style.qss", "r", encoding="utf-8") as f:
                self.app.setStyleSheet(f.read())
        except Exception as e:
            print(f"Không thể load style.qss: {e}")
        
        # Set default font
        font = QFont("Segoe UI", 13)
        self.app.setFont(font)
        
        # Enable high DPI scaling (PyQt6 handles this automatically)
        pass
    
    def initialize_database(self):
        """Initialize database tables and default data."""
        try:
            # Create tables
            create_tables()
            
            # Create default admin user
            create_default_admin()
            
            print("✓ Database initialized successfully")
            
        except Exception as e:
            print(f"Error initializing database: {e}")
            QMessageBox.critical(None, "Database Error", 
                               f"Không thể khởi tạo database: {str(e)}")
            sys.exit(1)
        
    def show_login(self):
        """Show login dialog."""
        self.login_dialog = LoginDialog(self.user_service)
        if self.login_dialog.exec() == LoginDialog.DialogCode.Accepted:
            self.show_main_window()
        else:
            sys.exit(0)
    
    def show_main_window(self):
        """Show main window."""
        self.main_window = MainWindow(
            offender_service=self.offender_service,
            user_service=self.user_service,
            ai_service=self.ai_service,
            report_service=self.report_service
        )
        self.main_window.show()
    
    def run(self):
        """Run the application."""
        try:
            # Test database connection
            with self.db_manager:
                print("✓ Database connection successful")
            
            # Show login dialog
            self.show_login()
            
            # Start event loop
            return self.app.exec()
            
        except Exception as e:
            import traceback
            QMessageBox.critical(None, "Lỗi", f"Không thể khởi động ứng dụng: {str(e)}")
            traceback.print_exc()  # In ra stack trace chi tiết
            input("Ấn enter để thoát")
            return 1


def excepthook(type, value, tb):
    with open("error.log", "w", encoding="utf-8") as f:
        f.write("Uncaught exception: %s: %s\n" % (type.__name__, value))
        traceback.print_tb(tb, file=f)
    try:
        from PyQt6.QtWidgets import QMessageBox
        QMessageBox.critical(None, "Lỗi hệ thống", f"Đã ghi log lỗi vào error.log\n{type.__name__}: {value}")
    except Exception:
        pass
    sys.exit(1)

sys.excepthook = excepthook


def main():
    """Main function."""
    app = OffenderManagementApp()
    sys.exit(app.run())


if __name__ == "__main__":
    main() 
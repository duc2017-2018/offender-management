import pytest
from database.database_manager import DatabaseManager
from services.report_service import ReportService

def test_generate_report():
    db = DatabaseManager()
    service = ReportService()
    offenders = []  # Truyền danh sách offenders rỗng hoặc mock nếu cần
    try:
        report = service.generate_report(db, offenders)
        assert isinstance(report, dict)
    except Exception:
        assert False, "Report generation failed" 
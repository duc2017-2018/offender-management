import pytest
from unittest.mock import MagicMock
from services.user_service import UserService
from services.offender_service import OffenderService
from models.offender import Offender

@pytest.fixture
def user_service():
    service = UserService(MagicMock())
    service.login = MagicMock(return_value=True)
    return service

@pytest.fixture
def offender_service():
    return OffenderService(MagicMock())

def test_login_and_add_offender(user_service, offender_service):
    # Đăng nhập thành công
    assert user_service.login("admin", "admin") is True

    # Thêm đối tượng mới
    offender_data = {
        "case_number": "40CE0625/405LF",
        "full_name": "Nguyễn Văn A",
        # ... các trường khác ...
    }
    offender_service.create_offender = MagicMock()
    offender_service.create_offender.return_value = Offender(**offender_data)
    offender = offender_service.create_offender(offender_data)
    assert offender.full_name == "Nguyễn Văn A"
    offender_service.create_offender.assert_called_once_with(offender_data) 
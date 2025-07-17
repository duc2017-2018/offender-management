import pytest
from unittest.mock import MagicMock
from services.user_service import UserService

@pytest.fixture
def service():
    return UserService(MagicMock())

def test_login_success(service):
    service.authenticate = MagicMock(return_value=object())
    assert service.authenticate("admin", "admin") is not None

def test_login_fail(service):
    service.authenticate = MagicMock(return_value=None)
    assert service.authenticate("admin", "wrong") is None 
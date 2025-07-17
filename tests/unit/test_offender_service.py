import pytest
from unittest.mock import MagicMock
from services.offender_service import OffenderService
from models.offender import Offender, Gender, CaseType, Status, RiskLevel
from datetime import date, timedelta

@pytest.fixture
def mock_db():
    db = MagicMock()
    return db

@pytest.fixture
def service(mock_db):
    return OffenderService(mock_db)

def offender_data():
    return {
        'case_number': '40CE0625/405LF',
        'full_name': 'Nguyễn Văn A',
        'gender': Gender.MALE,
        'birth_date': date(1990, 5, 15),
        'address': 'TDP 1, P. Bắc Hồng',
        'occupation': 'Nông dân',
        'crime': 'Trộm cắp tài sản',
        'case_type': CaseType.SUSPENDED_SENTENCE,
        'start_date': date.today() - timedelta(days=60),
        'duration_months': 6,
        'reduced_months': 1,
        'reduction_count': 0,
        'status': Status.ACTIVE,
        'risk_level': RiskLevel.MEDIUM,
    }

def test_create_offender_success(service, mock_db):
    data = offender_data()
    mock_db.create_offender.return_value = 123
    offender = service.create_offender(data)
    assert offender.id == 123
    assert offender.full_name == data['full_name']
    assert offender.case_number == data['case_number']
    mock_db.create_offender.assert_called_once()

def test_create_offender_validation_error(service):
    data = offender_data()
    data['case_number'] = ''  # Bắt buộc phải có số hồ sơ
    with pytest.raises(Exception):
        service.create_offender(data)

def test_update_offender_success(service, mock_db):
    data = offender_data()
    offender = Offender(**data)
    mock_db.get_offender.return_value = offender
    mock_db.update_offender.return_value = True
    data['full_name'] = 'Nguyễn Văn B'
    result = service.update_offender(1, data)
    assert result is True
    mock_db.update_offender.assert_called_once()

def test_update_offender_not_found(service, mock_db):
    mock_db.get_offender.return_value = None
    with pytest.raises(ValueError):
        service.update_offender(999, offender_data())

def test_delete_offender(service, mock_db):
    mock_db.delete_offender.return_value = True
    result = service.delete_offender(1)
    assert result is True
    mock_db.delete_offender.assert_called_once_with(1)

def test_get_offender(service, mock_db):
    offender = Offender(**offender_data())
    mock_db.get_offender.return_value = offender
    result = service.get_offender(1)
    assert result.full_name == 'Nguyễn Văn A'
    mock_db.get_offender.assert_called_once_with(1)

def test_search_offenders(service, mock_db):
    offenders = [Offender(**offender_data())]
    mock_db.search_offenders.return_value = offenders
    result = service.search_offenders('Nguyễn')
    assert len(result) == 1
    assert result[0].full_name == 'Nguyễn Văn A'
    mock_db.search_offenders.assert_called_once()

def test_calculate_risk_assessment(service):
    offender = Offender(**offender_data())
    risk = service.calculate_risk_assessment(offender)
    assert 'risk_score' in risk
    assert 'risk_level' in risk
    assert 'risk_factors' in risk
    assert isinstance(risk['risk_percentage'], float)

def test_apply_sentence_reduction_eligible(service, mock_db):
    offender = Offender(**offender_data())
    offender.is_eligible_for_reduction = MagicMock(return_value=True)
    mock_db.get_offender.return_value = offender
    mock_db.update_offender.return_value = True
    result = service.apply_sentence_reduction(1, 1, 'Good behavior')
    assert result is True
    mock_db.update_offender.assert_called_once()

def test_apply_sentence_reduction_not_eligible(service, mock_db):
    offender = Offender(**offender_data())
    offender.is_eligible_for_reduction = MagicMock(return_value=False)
    mock_db.get_offender.return_value = offender
    result = service.apply_sentence_reduction(1, 1, 'Good behavior')
    assert result is False

def test_get_expiring_offenders(service, mock_db):
    today = date.today()
    # Tạo offender có completion_date = today + 3 ngày
    start = today - timedelta(days=27)
    data = offender_data()
    data.update({
        'start_date': start,
        'duration_months': 1,
        'reduced_months': 0
    })
    offender = Offender(**data)
    assert offender.completion_date is not None
    assert (offender.completion_date - today).days == 3
    mock_db.get_all_offenders.return_value = [offender]
    result = service.get_expiring_offenders(days=5)
    assert len(result) == 1
    assert result[0].completion_date is not None
    assert (result[0].completion_date - today).days == 3
    # Edge case: offender đã hoàn thành (completion_date < today)
    data2 = offender_data()
    data2.update({
        'start_date': today - timedelta(days=40),
        'duration_months': 1,
        'reduced_months': 0
    })
    completed = Offender(**data2)
    if completed.completion_date is not None:
        assert (completed.completion_date - today).days < 0
    mock_db.get_all_offenders.return_value = [completed]
    result = service.get_expiring_offenders(days=5)
    assert len(result) == 0 
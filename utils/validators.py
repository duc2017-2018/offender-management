def validate_not_empty(value, field_name):
    if not value.strip():
        return f"{field_name} không được để trống!"
    return None

def validate_min_length(value, min_length, field_name):
    if len(value.strip()) < min_length:
        return f"{field_name} phải có ít nhất {min_length} ký tự!"
    return None

def validate_date_not_future(date, field_name):
    from datetime import date as dt
    if date > dt.today():
        return f"{field_name} không được lớn hơn ngày hiện tại!"
    return None 
import pytest
from app.utils.models import UserData
from app.utils.validation import validate_user_data

def test_valid_user_data():
    user = UserData(first_name="John", last_name="Doe", user_id="123456789", phone="1234567890", email="john@example.com")
    result = validate_user_data(user)
    assert result.is_valid
    assert result.errors == []

def test_missing_first_name():
    user = UserData(first_name="", last_name="Doe", user_id="123456789", phone="1234567890")
    result = validate_user_data(user)
    assert not result.is_valid
    assert "first_name" in result.errors

def test_long_first_name():
    user = UserData(first_name="A"*36, last_name="Doe", user_id="123456789", phone="1234567890")
    result = validate_user_data(user)
    assert not result.is_valid
    assert "first_name" in result.errors

def test_missing_last_name():
    user = UserData(first_name="John", last_name="", user_id="123456789", phone="1234567890")
    result = validate_user_data(user)
    assert not result.is_valid
    assert "last_name" in result.errors

def test_long_last_name():
    user = UserData(first_name="John", last_name="B"*36, user_id="123456789", phone="1234567890")
    result = validate_user_data(user)
    assert not result.is_valid
    assert "last_name" in result.errors

def test_invalid_id():
    user = UserData(first_name="John", last_name="Doe", user_id="abc123", phone="1234567890")
    result = validate_user_data(user)
    assert not result.is_valid
    assert "user_id" in result.errors

def test_long_id():
    user = UserData(first_name="John", last_name="Doe", user_id="1"*13, phone="1234567890")
    result = validate_user_data(user)
    assert not result.is_valid
    assert "user_id" in result.errors

def test_invalid_phone():
    user = UserData(first_name="John", last_name="Doe", user_id="123456789", phone="abc123")
    result = validate_user_data(user)
    assert not result.is_valid
    assert "phone" in result.errors

def test_long_phone():
    user = UserData(first_name="John", last_name="Doe", user_id="123456789", phone="1"*16)
    result = validate_user_data(user)
    assert not result.is_valid
    assert "phone" in result.errors

def test_invalid_email():
    user = UserData(first_name="John", last_name="Doe", user_id="123456789", phone="1234567890", email="notanemail")
    result = validate_user_data(user)
    assert not result.is_valid
    assert "email" in result.errors

def test_empty_email_ok():
    user = UserData(first_name="John", last_name="Doe", user_id="123456789", phone="1234567890", email=None)
    result = validate_user_data(user)
    assert result.is_valid
    assert result.errors == [] 
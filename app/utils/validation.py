import re
from app.utils.models import ValidationResult

# Phone validation for Israeli numbers
def validate_israeli_phone(phone: str) -> bool:
    """Validate Israeli phone numbers"""
    if not phone:
        return False
    
    # Remove spaces, dashes, and plus signs
    clean_phone = re.sub(r'[\s\-\+\(\)]', '', phone)
    
    # Check if it's only digits
    if not clean_phone.isdigit():
        return False
    
    # Israeli phone number patterns:
    # Mobile: 05X-XXXXXXX (10 digits total)
    # Landline: 0X-XXXXXXX (9-10 digits)
    # International format: +972-5X-XXXXXXX or 972-5X-XXXXXXX
    
    # Handle international format
    if clean_phone.startswith('972'):
        clean_phone = '0' + clean_phone[3:]  # Convert +972 to 0
    
    # Now validate Israeli format
    if len(clean_phone) == 10:
        # Mobile numbers: 050, 051, 052, 053, 054, 055, 058
        if clean_phone.startswith(('050', '051', '052', '053', '054', '055', '058')):
            return True
    
    if len(clean_phone) == 9:
        # Landline numbers: 02 (Jerusalem), 03 (Tel Aviv), 04 (Haifa), 08 (South), 09 (Sharon)
        if clean_phone.startswith(('02', '03', '04', '08', '09')):
            return True
    
    if len(clean_phone) == 10:
        # Some landline numbers with 10 digits
        if clean_phone.startswith(('02', '03', '04', '08', '09')):
            return True
    
    return False

# Update the main validation function:
def validate_user_data(user_data):
    """Validate user input data. Returns ValidationResult."""
    errors = []
    # First name
    if not user_data.first_name or len(user_data.first_name) > 35:
        errors.append("first_name")
    # Last name
    if not user_data.last_name or len(user_data.last_name) > 35:
        errors.append("last_name")
    # ID (optional) - Israeli ID is 9 digits
    if user_data.user_id and (not user_data.user_id.isdigit() or len(user_data.user_id) != 9):
        errors.append("user_id")
    # Phone - Use Israeli validation
    if not validate_israeli_phone(user_data.phone):
        errors.append("phone")
    # Email (optional)
    if user_data.email:
        email_regex = r"^[\w\.-]+@[\w\.-]+\.\w+$"
        if not re.match(email_regex, user_data.email):
            errors.append("email")
    return ValidationResult(is_valid=len(errors) == 0, errors=errors) 
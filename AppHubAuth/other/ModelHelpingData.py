from django.core.validators import RegexValidator
import re

PakistaniPhoneNumberRegex = RegexValidator(r'03\d{0,9}', '03xxxxxxxxx format required')


def validate_password(password):
    if re.search(r'[A-Za-z]', password) is None or re.search(r'[0-9]', password) is None:
        return False
    if len(password) < 8:
        return False
    return True

from django.core.validators import RegexValidator
import re
PakistaniPhoneNumberRegex = RegexValidator(r'03\d{0,9}', '03xxxxxxxxx format required')





def validate_password(password):

    return  bool(re.match("^(?=.*\d)(?=.*[a-z])[a-zA-Z0-9]{8,118}$", password))



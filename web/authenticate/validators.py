from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator

# Checks if string and if it contains only letters, hyphens and spaces
def validate_is_name(value):
    if not isinstance(value, str):
        raise ValidationError('Not a string')
    if not value.replace("-", "").replace(" ","").isalpha():
        raise ValidationError('A name can only contain letters, hyphens and spaces')


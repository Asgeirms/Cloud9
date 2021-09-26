from django.core.exceptions import ValidationError

def validate_only_letters(value):
    if not isinstance(value, str):
        raise ValidationError('Not a string')
    if not value.isalpha():
        raise ValidationError('Can only contain letters')
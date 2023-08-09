from django.core.exceptions import ValidationError

def validate_name(value):
    if value.strip() != value:
        raise ValidationError('Tag cannot be empty or contain whitespaces at the ends')
    
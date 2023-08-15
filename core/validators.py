from django.core.exceptions import ValidationError
import base64
from binascii import Error as DecodingError
from datetime import date

# todo: put the encryption algorithm in a config so that it can be changed later without rewriting a lot of code
def validate_encoded_field(value):
    try:
        base64.b64decode(value)
    except DecodingError:
        raise ValidationError('data is corrupted')
    
def validate_non_empty(value):
    if value.strip() != value:
        raise ValidationError('no data')
    
def validate_date_past_or_present(value):
    if value > date.today():
        raise ValidationError('date must be today or earlier')
    
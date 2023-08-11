from django.core.exceptions import ValidationError
import base64
from binascii import Error as DecodingError

# todo: put the encryption algorithm in a config so that it can be changed later without rewriting a lot of code
def validate_encoded_field(value):
    if value.strip() != value:
        raise ValidationError('data is empty')
    try:
        base64.b64decode(value)
    except DecodingError:
        raise ValidationError('data is corrupted')
    
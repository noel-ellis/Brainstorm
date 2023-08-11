from django.db import models
from .validators import validate_encoded_field

class Folder(models.Model):
    name = models.CharField(max_length=256, blank=False, validators=[validate_encoded_field])
    account = models.ForeignKey('account.Account', on_delete=models.CASCADE, limit_choices_to={"is_active": True})
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, default=None)
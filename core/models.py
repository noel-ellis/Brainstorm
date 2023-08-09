from django.db import models
from .validators import validate_name

class Tag(models.Model):
    name = models.CharField(max_length=30, unique=True, validators=[validate_name])

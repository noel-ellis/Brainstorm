from django.db import models
from .validators import validate_encoded_field, validate_non_empty

class Folder(models.Model):
    name = models.CharField(max_length=256, blank=False, validators=[validate_encoded_field, validate_non_empty])
    account = models.ForeignKey('account.Account', on_delete=models.CASCADE, limit_choices_to={"is_active": True})
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, default=None)

class Note(models.Model):
    name = models.CharField(max_length=256, blank=False, validators=[validate_encoded_field, validate_non_empty])
    content = models.TextField(blank=True, validators=[validate_encoded_field])
    pinned = models.BooleanField(default=False)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    folder = models.ForeignKey('Folder', on_delete=models.CASCADE)

    
class TodoList(models.Model):
    HIGH = 'h'
    MEDIUM = 'm'
    LOW = 'l'
    NONE = 'n'
    TODOLIST_PRIORITY_CHOICES = [
        (HIGH, "High"),
        (MEDIUM, "Medium"),
        (LOW, "Low"),
        (NONE, "None"),
    ]

    name = models.CharField(max_length=256, blank=False, validators=[validate_encoded_field, validate_non_empty])
    priority = models.CharField(max_length=1, choices=TODOLIST_PRIORITY_CHOICES, default=NONE)
    due_date = models.DateField(null=True, blank=True, default=None)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    folder = models.ForeignKey('Folder', on_delete=models.CASCADE)
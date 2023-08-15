from django.db import models
from django.core.exceptions import ValidationError

from .validators import validate_encoded_field, validate_non_empty, validate_date_past_or_present


class Folder(models.Model):
    name = models.CharField(max_length=256, blank=False, validators=[validate_encoded_field, validate_non_empty])
    account = models.ForeignKey('account.Account', on_delete=models.CASCADE, limit_choices_to={"is_active": True})
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, default=None)

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)


class Note(models.Model):
    name = models.CharField(max_length=256, blank=False, validators=[validate_encoded_field, validate_non_empty])
    content = models.TextField(blank=True, validators=[validate_encoded_field])
    pinned = models.BooleanField(default=False)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    folder = models.ForeignKey('Folder', on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)


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

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)


class Task(models.Model):
    HIGH = 'h'
    MEDIUM = 'm'
    LOW = 'l'
    NONE = 'n'
    TASK_PRIORITY_CHOICES = [
        (HIGH, "High"),
        (MEDIUM, "Medium"),
        (LOW, "Low"),
        (NONE, "None"),
    ]

    name = models.CharField(max_length=256, blank=False, validators=[validate_encoded_field, validate_non_empty])
    priority = models.CharField(max_length=1, choices=TASK_PRIORITY_CHOICES, default=NONE)
    failed = models.BooleanField(default=False)
    date_created = models.DateTimeField(auto_now_add=True)
    due_date = models.DateField(null=True, blank=True, default=None)
    date_closed = models.DateField(null=True, blank=True, default=None, validators=[validate_date_past_or_present])

    parent_task = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, default=None)
    note = models.ForeignKey('Note', on_delete=models.CASCADE, null=True, blank=True, default=None)
    # allows for checkboxes in notes to lose their attached tasks, if original todo_list is deleted
    todo_list = models.ForeignKey('TodoList', on_delete=models.CASCADE)

    def clean(self):
        if self.failed and self.date_closed == None:
            raise ValidationError("a task can't be open and failed at the same time")
        
        super().clean()

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

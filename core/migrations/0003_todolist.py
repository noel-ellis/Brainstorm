# Generated by Django 4.2.2 on 2023-08-14 18:55

import core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_note'),
    ]

    operations = [
        migrations.CreateModel(
            name='TodoList',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=256, validators=[core.validators.validate_encoded_field, core.validators.validate_non_empty])),
                ('priority', models.CharField(choices=[('h', 'High'), ('m', 'Medium'), ('l', 'Low'), ('n', 'None')], default='n', max_length=1)),
                ('due_date', models.DateField(blank=True, default=None, null=True)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_updated', models.DateTimeField(auto_now=True)),
                ('folder', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.folder')),
            ],
        ),
    ]

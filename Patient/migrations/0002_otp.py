# Generated by Django 5.1 on 2024-08-12 12:14

import django.db.models.deletion
import django.utils.timezone
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Patient', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Otp',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('email', models.EmailField(max_length=32)),
                ('otp', models.CharField(max_length=6)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('patient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Patient.patient')),
            ],
        ),
    ]

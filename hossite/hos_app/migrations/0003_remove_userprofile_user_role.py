# Generated by Django 5.1.6 on 2025-02-18 16:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hos_app', '0002_rename_price_doctor_appointment_price'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='user_role',
        ),
    ]

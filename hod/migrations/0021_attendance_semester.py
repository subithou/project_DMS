# Generated by Django 3.2.9 on 2022-04-25 17:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hod', '0020_attendance_attendance_record'),
    ]

    operations = [
        migrations.AddField(
            model_name='attendance',
            name='semester',
            field=models.BigIntegerField(default=1, max_length=255),
            preserve_default=False,
        ),
    ]
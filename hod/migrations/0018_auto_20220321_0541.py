# Generated by Django 3.2.9 on 2022-03-21 00:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hod', '0017_remove_subject_to_staff_subject_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='subject_to_staff',
            name='batch_id',
            field=models.BigIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='subject_to_staff',
            name='semester',
            field=models.BigIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='subject_to_staff',
            name='staff_id',
            field=models.BigIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='subject_to_staff',
            name='subject_id',
            field=models.BigIntegerField(default=0, max_length=255),
        ),
    ]

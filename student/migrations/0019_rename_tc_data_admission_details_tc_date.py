# Generated by Django 4.0.4 on 2022-07-10 18:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0018_alter_qualification_date_of_course'),
    ]

    operations = [
        migrations.RenameField(
            model_name='admission_details',
            old_name='tc_data',
            new_name='tc_date',
        ),
    ]

# Generated by Django 4.0.4 on 2022-07-07 05:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0013_alter_qualification_mark_percentage'),
    ]

    operations = [
        migrations.AddField(
            model_name='local_guardian',
            name='occupation',
            field=models.CharField(max_length=256, null=True),
        ),
    ]

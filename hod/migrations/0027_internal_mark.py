# Generated by Django 3.2.9 on 2022-04-26 02:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hod', '0026_delete_internal_mark'),
    ]

    operations = [
        migrations.CreateModel(
            name='Internal_mark',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('student_id', models.BigIntegerField()),
                ('subject_id', models.BigIntegerField()),
                ('exam_type', models.CharField(choices=[('Assignment 1', 'Assignment 1'), ('Assignment 2', 'Assignment 2'), ('Internal 1', 'Internal 1'), ('Internal 2', 'Internal 2')], max_length=255)),
                ('semester', models.BigIntegerField()),
                ('mark', models.FloatField()),
            ],
        ),
    ]

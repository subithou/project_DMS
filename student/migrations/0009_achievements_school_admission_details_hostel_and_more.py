# Generated by Django 4.0.4 on 2022-06-30 06:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0008_qualifications_parents'),
    ]

    operations = [
        migrations.CreateModel(
            name='achievements_school',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('student_id', models.BigIntegerField()),
                ('event', models.CharField(max_length=256, null=True)),
                ('prize', models.CharField(max_length=256, null=True)),
                ('category', models.CharField(max_length=256, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='admission_details',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('student_id', models.BigIntegerField()),
                ('joined_semester', models.BigIntegerField()),
                ('admission_quota', models.CharField(max_length=256, null=True)),
                ('last_studied_institution', models.CharField(max_length=256, null=True)),
                ('reason_for_leaving', models.CharField(max_length=256, null=True)),
                ('tc_no', models.CharField(max_length=256, null=True)),
                ('tc_data', models.DateField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='hostel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('student_id', models.BigIntegerField()),
                ('hostel_address', models.CharField(max_length=256, null=True)),
                ('reason_for_leaving', models.CharField(max_length=512, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='local_guardian',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('student_id', models.BigIntegerField()),
                ('name', models.CharField(max_length=256, null=True)),
                ('address', models.CharField(max_length=256, null=True)),
                ('number', models.BigIntegerField(null=True)),
                ('relationship', models.CharField(max_length=256, null=True)),
                ('email_id', models.EmailField(max_length=254, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='qualification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('student_id', models.BigIntegerField()),
                ('name_of_exam', models.CharField(max_length=256, null=True)),
                ('name_of_institution', models.CharField(max_length=256, null=True)),
                ('date_of_course', models.DateTimeField(null=True)),
                ('register_number', models.CharField(max_length=256, null=True)),
                ('mark_percentage', models.BigIntegerField(null=True)),
                ('no_of_chances', models.BigIntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='siblings',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('student_id', models.BigIntegerField()),
                ('name', models.CharField(max_length=256, null=True)),
                ('qualification', models.CharField(max_length=256, null=True)),
                ('occupation', models.CharField(max_length=256, null=True)),
                ('address', models.CharField(max_length=256, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='sslc_plustwo_mark',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('qualification_id', models.BigIntegerField()),
                ('mal', models.CharField(max_length=256, null=True)),
                ('english', models.CharField(max_length=256, null=True)),
                ('physics', models.CharField(max_length=256, null=True)),
                ('chemistry', models.CharField(max_length=256, null=True)),
                ('biology', models.CharField(max_length=256, null=True)),
                ('maths', models.CharField(max_length=256, null=True)),
                ('hindi', models.CharField(max_length=256, null=True)),
                ('computer', models.CharField(max_length=256, null=True)),
            ],
        ),
        migrations.AlterField(
            model_name='parents',
            name='student_id',
            field=models.BigIntegerField(),
        ),
        migrations.DeleteModel(
            name='qualifications',
        ),
    ]

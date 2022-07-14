import email
from django.db import models

# Create your models here.
from login.models import MyUser


class profile_student(models.Model):
    register_no = models.CharField(max_length=255)
    university_no = models.CharField(max_length=255, null=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255, null=True)
    roll_no = models.BigIntegerField(unique=False, null=True)
    branch = models.CharField(max_length=255, null=True)
    aadhar_no = models.BigIntegerField(unique=True, null=True)
    address = models.CharField(max_length=255, null=True)
    phone_no = models.BigIntegerField(unique=True, null=True)
    email = models.EmailField(unique=True, null=True)
    sex = models.CharField(max_length=10, null=True,
                           choices=[('Female', 'Female'), ('Male', 'Male'), ('Others', 'Others')])
    date_of_birth = models.DateField(unique=False, null=True)
    nationality = models.CharField(max_length=255, null=True)
    religion = models.CharField(max_length=255, null=True)
    caste = models.CharField(max_length=255, null=True)
    native_place = models.CharField(max_length=255, null=True)
    batch = models.BigIntegerField(unique=False, null=False)
    scheme_id = models.BigIntegerField(unique=False, null=False)
    joined_semester = models.BigIntegerField(null=False)

    blood_groups = [
        ('A+', 'A+'),
        ('A-', 'A-'),
        ('B+', 'B+'),
        ('B-', 'B-'),
        ('AB+', 'AB+'),
        ('AB-', 'AB-'),
        ('O+', 'O+'),
        ('O-', 'O-'),
    ]
    blood_group = models.CharField(max_length=10, choices=blood_groups, null=True)
    hobbies = models.CharField(max_length=100, null=True)
    photo = models.ImageField(upload_to='images/', null=True, default='images/user_default_image.png')
    sign = models.ImageField(upload_to='images/', null=True)
    is_edit = models.BooleanField(default=False)

    def __str__(self):
        name = self.first_name + " " + self.last_name
        return name


class parents(models.Model):
    student_id = models.BigIntegerField(null=False)
    fathers_name = models.CharField(max_length=256, null=True)
    fathers_occupation = models.CharField(max_length=256, null=True)
    mothers_name = models.CharField(max_length=256, null=True)
    mothers_occupation = models.CharField(max_length=256, null=True)
    fathers_address = models.CharField(max_length=256, null=True)
    mothers_address = models.CharField(max_length=256, null=True)
    official_address = models.CharField(max_length=256, null=True)
    fathers_email_id = models.EmailField(null=True)
    mothers_email_id = models.EmailField(null=True)
    fathers_number = models.BigIntegerField(null=True)
    mothers_number = models.BigIntegerField(null=True)


class local_guardian(models.Model):
    student_id = models.BigIntegerField(null=False)
    name = models.CharField(max_length=256, null=True)
    occupation = models.CharField(max_length=256, null=True)
    address = models.CharField(max_length=256, null=True)
    number = models.BigIntegerField(null=True)
    relationship = models.CharField(max_length=256, null=True)
    email_id = models.EmailField(null=True)


class siblings(models.Model):
    student_id = models.BigIntegerField(null=False)
    name = models.CharField(max_length=256, null=True)
    qualification = models.CharField(max_length=256, null=True)
    occupation = models.CharField(max_length=256, null=True)
    address = models.CharField(max_length=256, null=True)


class hostel(models.Model):
    student_id = models.BigIntegerField(null=False)
    year = models.BigIntegerField(null=True)
    hostel_address = models.CharField(max_length=256, null=True)
    reason_for_leaving = models.CharField(max_length=512, null=True)


class qualification(models.Model):
    student_id = models.BigIntegerField(null=False)
    exam_type = [
        ('SSLC', 'SSLC'),
        ('PLUS TWO', 'PLUS TWO'),
    ]
    name_of_exam = models.CharField(max_length=256, choices=exam_type, null=True)
    name_of_institution = models.CharField(max_length=256, null=True)
    date_of_course = models.DateField(null=True)
    register_number = models.CharField(max_length=256, null=True)
    mark_percentage = models.FloatField(null=True)
    no_of_chances = models.BigIntegerField(null=True)
    mal = models.CharField(max_length=256, null=True)
    english = models.CharField(max_length=256, null=True)
    physics = models.CharField(max_length=256, null=True)
    chemistry = models.CharField(max_length=256, null=True)
    biology = models.CharField(max_length=256, null=True)
    maths = models.CharField(max_length=256, null=True)
    hindi = models.CharField(max_length=256, null=True)
    computer = models.CharField(max_length=256, null=True)


class achievements_school(models.Model):
    student_id = models.BigIntegerField(null=False)
    event = models.CharField(max_length=256, null=True)
    prize = models.CharField(max_length=256, null=True)
    category = models.CharField(max_length=256, null=True)


class admission_details(models.Model):
    student_id = models.BigIntegerField(null=False)
    admission_quota = models.CharField(max_length=256, null=True)
    last_studied_institution = models.CharField(max_length=256, null=True)
    reason_for_leaving = models.CharField(max_length=256, null=True)
    tc_no = models.CharField(max_length=256, null=True)
    tc_date = models.DateField(null=True)

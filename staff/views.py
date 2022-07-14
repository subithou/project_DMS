from calendar import month
from cgitb import text
from datetime import date, datetime
from email import message
from functools import total_ordering
from re import T
import re

from django.contrib.auth.hashers import check_password, make_password
from django.forms import Form
from django.db.models import Sum, Max

from psycopg2 import Date
from pyparsing import line
from pytest import mark
import urllib3
import login
from django.contrib.auth import logout
from django.shortcuts import render, redirect
from django.contrib import messages

from hod.models import Internal_mark, attendance_record, scheme, semester_result, subject, subject_to_staff, batch, \
    attendance
from staff.models import profile
from login.models import MyUser
from student.models import profile_student, parents, local_guardian, qualification, admission_details


def staff_index(request):
    current_user = request.user
    user_id = current_user.username

    staff_details = profile.objects.get(Faculty_unique_id=user_id)
    fullname = staff_details.First_name + " " + staff_details.Last_name
    context = {'name': fullname}

    # return render(request, 'staff_index.html', {'context': context})
    return redirect(view_subjects)


# Staff profile

def staff_profile(request):
    # name = request.session['staff_name']
    current_user = request.user
    user_id = current_user.username

    staff_details = profile.objects.get(Faculty_unique_id=user_id)
    fullname = staff_details.First_name + " " + staff_details.Last_name

    context = {'name': fullname}

    date = str(staff_details.Date_of_Joining)
    dob = str(staff_details.Date_of_Birth)

    # Please check the gender is valid or not

    if 'edit_profile' in request.POST:
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        # faculty_unique_id = request.POST.get('faulty_unique_id')
        # print(faculty_unique_id)
        gender = request.POST.get('gender')

        if gender == '0':
            messages.error(request, 'Please select the valid gender')

        else:

            dob = request.POST.get('date_of_birth')
            phone_no = request.POST.get('phone_no')
            email = request.POST.get('email')
            aadhaar_no = request.POST.get('aadhaar_no')
            caste = request.POST.get('caste')
            religion = request.POST.get('religion')
            category = request.POST.get('category')
            pan = request.POST.get('pan')

            # date_of_joining = request.POST.get('date_of_joining')
            # aicte_unique_id = request.POST.get('aicte_unique_id')

            appointment_type = request.POST.get('appointment_type')
            cadre = request.POST.get('cadre')
            designation = request.POST.get('designation')
            specialisation = request.POST.get('specialisation')
            department_of_program = request.POST.get('department_of_program')
            examiner_institution = request.POST.get('examiner_institution')
            area_of_research = request.POST.get('area_of_research')

            # print(name, gender,faculty_unique_id, dob, phone_no,email, aadhaar_no, caste, religion, category, cadre)

            staff_details.First_name = first_name
            staff_details.Last_name = last_name
            staff_details.Gender = gender
            staff_details.Date_of_Birth = dob
            staff_details.Aadhar_No = aadhaar_no
            staff_details.Caste = caste
            staff_details.Religion = religion
            staff_details.category = category
            staff_details.PAN = pan

            #   staff.Date_of_Joining = date_of_joining
            #   staff.AICTE_unique_Id = aicte_unique_id

            staff_details.Appointment_type = appointment_type
            staff_details.Cadre = cadre
            staff_details.Designation = designation
            staff_details.Specialisation = specialisation
            staff_details.Department_of_program = department_of_program
            staff_details.Examiner_institution = examiner_institution
            staff_details.Area_of_Research = area_of_research
            staff_details.email = email
            staff_details.phone_no = phone_no
            staff_details.save()
            messages.error(request, "Successfully updated profile")
            return redirect(staff_profile)

    if 'change_password' in request.POST:
        current_password = request.POST.get('current_password')
        new_password = request.POST.get('new_password')
        renew_password = request.POST.get('renew_password')

        user_data = MyUser.objects.get(username=user_id)
        user_password = user_data.password

        if new_password != renew_password:
            messages.error(request, "Password mismatch")

        elif check_password(current_password, user_password) is False :
            messages.error(request, "incorrect old password")

        else:
            new_hashed = make_password(new_password)
            user_data.password = new_hashed
            user_data.save()
            messages.error(request, "Successfully changed password")
            return redirect(staff_profile)
    return render(request, 'staff_profile.html',
                  {
                      'context': context,
                      'staff_details': staff_details,
                      'date': date,
                      'date_dob': dob,


                  })


def view_subjects(request):
    current_user = request.user
    user_id = current_user.username

    staff_details = profile.objects.get(Faculty_unique_id=user_id)
    fullname = staff_details.First_name + " " + staff_details.Last_name
    context = {'name': fullname}

    scheme_data = scheme.objects.all()
    view_subject_all = subject.objects.all()
    assign_subject_data = subject_to_staff.objects.all()
    none = "None"
    staff_data = profile.objects.all()
    batch_data = batch.objects.all()

    assigned_subject_to_this_staff = subject_to_staff.objects.filter(staff_id=staff_details.id)

    return render(request, 'view_subjects.html',

                  {
                      'scheme_data': scheme_data,
                      "view_subject": view_subject_all,
                      'assign_subject_data': assign_subject_data,
                      'none': none,
                      'staff_data': staff_data,
                      'batch_data': batch_data,
                      'context': context,
                      'subject_to_this_staff': assigned_subject_to_this_staff,
                      'staff_details': staff_details,
                  })


# view each class and assign the marks and attendance

def update_class(request, batch_id, subject_id):
    current_user = request.user
    user_id = current_user.username
    staff_details = profile.objects.get(Faculty_unique_id=user_id)
    fullname = staff_details.First_name + " " + staff_details.Last_name
    context = {'name': fullname}

    # print(batch_id, subject_id)
    batch_id = int(batch_id)
    subject_id = int(subject_id)

    staff_id = staff_details.id
    check_subject_exist = subject_to_staff.objects.filter(batch_id=batch_id, staff_id=staff_id, subject_id=subject_id)

    subject_data = subject.objects.all()
    student_data = profile_student.objects.all()
    batch_data = batch.objects.all()
    staff_data = profile.objects.all()
    att_record = attendance_record.objects.filter(batch_id=batch_id, subject_id=subject_id)
    subject_to_staff_data = subject_to_staff.objects.filter(batch_id=batch_id, subject_id=subject_id)

    from datetime import date
    today = date.today()

    check_today_attendance_marked = attendance_record.objects.filter(batch_id=batch_id, subject_id=subject_id,
                                                                     date=today)
    if check_today_attendance_marked:
        marked = True
    else:
        marked = False

    for i in batch_data:
        # Join date
        date = str(i.date_of_join)

    if 'assign' in request.POST:
        # request.session['batch_id'] = batch_id
        # request.session['subject_id'] = subject_id
        return redirect(add_attendance, batch_id, subject_id)

    if 'internal' in request.POST:
        # request.session['batch_id'] = batch_id
        # request.session['subject_id'] = subject_id
        return redirect(add_internal, batch_id, subject_id)

    if 'result' in request.POST:
        # request.session['batch_id'] = batch_id
        # request.session['subject_id'] = subject_id
        return redirect(view_internal_result, batch_id, subject_id)

    # if 'view_attendance' in request.POST:
    #    return redirect(view_attendance, batch_id, subject_id, )

    return render(request, 'update_class.html', {
        'context': context,
        'check_subject_exist': check_subject_exist,
        'subject_data': subject_data,
        'student_data': student_data,
        'batch_data': batch_data,
        'staff_data': staff_data,
        'date': date,
        'attendance_record': att_record,
        'marked': marked,
        'subject_to_staff_data': subject_to_staff_data,
        'staff_details': staff_details,

    })


# Attendance

def add_attendance(request, batch_id, subject_id):
    current_user = request.user
    user_id = current_user.username

    staff_details = profile.objects.get(Faculty_unique_id=user_id)
    fullname = staff_details.First_name + " " + staff_details.Last_name
    context = {'name': fullname}

    # batch_id = request.session['batch_id'] 
    # subject_id = request.session['subject_id'] 

    student_data = profile_student.objects.filter(batch=batch_id).order_by('roll_no')
    subject_data = subject.objects.filter(id=subject_id)
    batch_data = batch.objects.filter(id=batch_id)

    staff_id = staff_details.id
    check_subject_exist = subject_to_staff.objects.filter(batch_id=batch_id, staff_id=staff_id, subject_id=subject_id)
    for i in check_subject_exist:
        sem = i.semester

    if request.method == 'POST':
        today = date.today()
        from_time = request.POST.get('from_time')
        end_time = request.POST.get('end_time')
        no_of_hours = request.POST.get('no_of_hours')

        from_time = datetime.strptime(from_time, '%H:%M')
        end_time = datetime.strptime(end_time, '%H:%M')
        print(from_time, end_time, type(from_time), type(end_time))
        no_of_hours = int(no_of_hours)

        att_record = attendance_record.objects.filter(date=today, from_time=from_time, subject_id=subject_id,
                                                      batch_id=batch_id)

        if att_record:
            messages.error(request, "Attendance already Marked")
            return redirect(add_attendance, batch_id, subject_id)
        else:

            attendance_record.objects.create(date=today, marked=True, subject_id=subject_id, batch_id=batch_id,
                                             from_time=from_time, end_time=end_time, no_of_hours=no_of_hours)
            record_id = attendance_record.objects.get(date=today, marked=True, subject_id=subject_id, batch_id=batch_id,
                                                      from_time=from_time, end_time=end_time, no_of_hours=no_of_hours)

            for i in student_data:
                x = i.register_no
                att_mark = request.POST.get(str(x))
                # print(att_mark, type(att_mark))

                attendance.objects.create(attendance_record_id=record_id.id, student_id=i.id, subject_id=subject_id,
                                          batch_id=batch_id, present=att_mark, semester=sem)
            messages.error(request, "Attendance successfully added")
            return redirect('update_class', batch_id, subject_id)

    return render(request, 'attendance.html',
                  {
                      'context': context,
                      'student_data': student_data,
                      'subject_data': subject_data,
                      'batch_data': batch_data,
                      'check_subject_exist': check_subject_exist,
                      'staff_details': staff_details,
                  })


def view_attendance(request, record_id, batch_id, subject_id):
    current_user = request.user
    user_id = current_user.username

    staff_details = profile.objects.get(Faculty_unique_id=user_id)
    fullname = staff_details.First_name + " " + staff_details.Last_name
    context = {'name': fullname}

    record_id = int(record_id)
    batch_id = int(batch_id)
    subject_id = int(subject_id)
    print(record_id, batch_id, subject_id)

    attendance_data = attendance.objects.filter(attendance_record_id=record_id)
    for i in attendance_data:
        print(i.present, type(i.present))
    attendance_record_data = attendance_record.objects.filter(id=record_id)
    student_data = profile_student.objects.filter(batch=batch_id).order_by('roll_no')
    subject_data = subject.objects.filter(id=subject_id)
    batch_data = batch.objects.filter(id=batch_id)

    staff_id = staff_details.id
    check_subject_exist = subject_to_staff.objects.filter(batch_id=batch_id, staff_id=staff_id, subject_id=subject_id)

    return render(request, 'view_attendance.html',
                  {
                      'context': context,
                      'attendance_data': attendance_data,
                      'student_data': student_data,
                      'subject_data': subject_data,
                      'batch_data': batch_data,
                      'check_subject_exist': check_subject_exist,
                      'attendance_record_data': attendance_record_data,
                      'staff_details': staff_details,
                  })


# Internal 

def add_internal(request, batch_id, subject_id):
    current_user = request.user
    user_id = current_user.username

    staff_details = profile.objects.get(Faculty_unique_id=user_id)
    fullname = staff_details.First_name + " " + staff_details.Last_name
    context = {'name': fullname}

    # batch_id = request.session['batch_id']
    # subject_id = request.session['subject_id'] 

    student_data = profile_student.objects.filter(batch=batch_id).order_by('roll_no')
    subject_data = subject.objects.filter(id=subject_id)
    batch_data = batch.objects.filter(id=batch_id)

    staff_id = staff_details.id
    check_subject_exist = subject_to_staff.objects.filter(batch_id=batch_id, staff_id=staff_id, subject_id=subject_id)
    internal_mark = Internal_mark.objects.filter()

    for i in check_subject_exist:
        sem = i.semester

    if 'internal' in request.POST:
        for i in student_data:
            x = i.roll_no
            mark = request.POST.getlist(str(x))
            print(mark)

            exist_ass1 = Internal_mark.objects.filter(student_id=i.id, subject_id=subject_id, semester=sem,
                                                      exam_type='Assignment 1').count()
            exist_ass2 = Internal_mark.objects.filter(student_id=i.id, subject_id=subject_id, semester=sem,
                                                      exam_type='Assignment 2').count()
            exist_internal1 = Internal_mark.objects.filter(student_id=i.id, subject_id=subject_id, semester=sem,
                                                           exam_type='Internal 1').count()
            exist_internal2 = Internal_mark.objects.filter(student_id=i.id, subject_id=subject_id, semester=sem,
                                                           exam_type='Internal 2').count()
            print(exist_ass1, exist_ass2, exist_internal1, exist_internal2)
            if exist_ass1 > 0:
                update_ass1 = Internal_mark.objects.get(student_id=i.id, subject_id=subject_id, semester=sem,
                                                        exam_type='Assignment 1')
                update_ass1.mark = mark[0]
                update_ass1.save()

            if exist_ass2 > 0:
                update_ass2 = Internal_mark.objects.get(student_id=i.id, subject_id=subject_id, semester=sem,
                                                        exam_type='Assignment 2')
                update_ass2.mark = mark[1]
                update_ass2.save()

            if exist_internal1 > 0:
                update_internal1 = Internal_mark.objects.get(student_id=i.id, subject_id=subject_id, semester=sem,
                                                             exam_type='Internal 1')
                update_internal1.mark = mark[2]
                update_internal1.save()

            if exist_internal2 > 0:
                update_internal2 = Internal_mark.objects.get(student_id=i.id, subject_id=subject_id, semester=sem,
                                                             exam_type='Internal 2')
                update_internal2.mark = mark[3]
                update_internal2.save()

            if exist_ass1 == 0 and exist_ass2 == 0 and exist_internal1 == 0 and exist_internal2 == 0:
                Internal_mark.objects.create(student_id=i.id, subject_id=subject_id, semester=sem, mark=mark[0],
                                             exam_type='Assignment 1')
                Internal_mark.objects.create(student_id=i.id, subject_id=subject_id, semester=sem, mark=mark[1],
                                             exam_type='Assignment 2')
                Internal_mark.objects.create(student_id=i.id, subject_id=subject_id, semester=sem, mark=mark[2],
                                             exam_type='Internal 1')
                Internal_mark.objects.create(student_id=i.id, subject_id=subject_id, semester=sem, mark=mark[3],
                                             exam_type='Internal 2')

        return redirect('update_class', batch_id, subject_id)

    return render(request, 'internal.html',
                  {
                      'context': context,
                      'student_data': student_data,
                      'subject_data': subject_data,
                      'batch_data': batch_data,
                      'check_subject_exist': check_subject_exist,
                      'internal_mark': internal_mark,
                      'staff_details': staff_details,

                  })


# view_internal_result
def view_internal_result(request, batch_id, subject_id):
    current_user = request.user
    user_id = current_user.username

    staff_details = profile.objects.get(Faculty_unique_id=user_id)
    fullname = staff_details.First_name + " " + staff_details.Last_name
    context = {'name': fullname}

    # batch_id = request.session['batch_id']
    # subject_id = request.session['subject_id'] 

    student_data = profile_student.objects.filter(batch=batch_id).order_by('roll_no')
    subject_data = subject.objects.filter(id=subject_id)
    batch_data = batch.objects.filter(id=batch_id)

    staff_id = staff_details.id
    check_subject_exist = subject_to_staff.objects.filter(batch_id=batch_id, staff_id=staff_id, subject_id=subject_id)
    internal_mark = Internal_mark.objects.filter()

    total_attendance = attendance_record.objects.filter(batch_id=batch_id, subject_id=subject_id).aggregate(
        Sum('no_of_hours'))

    attendance_record_data = attendance_record.objects.filter(batch_id=batch_id, subject_id=subject_id)
    total_hour = total_attendance['no_of_hours__sum']
    if total_hour == None:
        messages.error(request, "Attendance not entered ")
        return redirect(update_class, batch_id, subject_id)
    # print(total_attendance, total_hour, type(total_hour))

    attendance_data = attendance.objects.filter(batch_id=batch_id, subject_id=subject_id)

    attenance_list = []
    for i in student_data:
        hour = 0
        for j in attendance_data:
            if i.id == j.student_id:
                if j.present == True:
                    id1 = j.attendance_record_id
                    # print('id',id1, type(id1))
                    no_of_hours_taken = attendance_record.objects.get(id=id1)

                    hour = hour + no_of_hours_taken.no_of_hours
        percentage_attendance = (hour / total_hour) * 100
        # print(i.first_name, hour)
        att_tuple = (i.register_no, percentage_attendance)
        attenance_list.append(att_tuple)

    mark_data = Internal_mark.objects.filter(subject_id=subject_id)

    total_mark_list = []
    for i in student_data:
        for j in mark_data:
            if i.id == j.student_id:
                sum_of_mark = Internal_mark.objects.filter(student_id=i.id, subject_id=subject_id).aggregate(
                    Sum('mark'))
                total_internal = sum_of_mark['mark__sum']
                mark_tupple = (i.register_no, total_internal)
                # x print(mark_tupple)
        total_mark_list.append(mark_tupple)
        # total_mark_list.append(mark_tupple)

    print(total_mark_list)

    return render(request, 'internal_result.html',
                  {
                      'context': context,
                      'student_data': student_data,
                      'subject_data': subject_data,
                      'batch_data': batch_data,
                      'check_subject_exist': check_subject_exist,
                      'internal_mark': internal_mark,
                      'attendance_data': attendance_data,
                      'attendance_record_data': attendance_record_data,
                      'attendance_list': attenance_list,
                      'total_mark_list': total_mark_list,
                      'staff_details': staff_details,

                  })


# View the classes if tutor

def view_classes(request):
    current_user = request.user
    user_id = current_user.username

    staff_details = profile.objects.get(Faculty_unique_id=user_id)
    fullname = staff_details.First_name + " " + staff_details.Last_name
    context = {'name': fullname}

    staff_id = staff_details.id
    batch_data = batch.objects.filter(tutor_id=staff_id)
    scheme_data = scheme.objects.all()

    return render(request, 'view_classes.html',

                  {

                      'context': context,
                      'batch_data': batch_data,
                      'scheme_data': scheme_data,
                      'staff_details': staff_details,

                  })


# Class details if tutor

def update_class_of_tutor(request, batch_id):
    current_user = request.user
    user_id = current_user.username

    staff_details = profile.objects.get(Faculty_unique_id=user_id)
    fullname = staff_details.First_name + " " + staff_details.Last_name
    context = {'name': fullname}

    batch_data = batch.objects.get(id=batch_id)
    staff_data = profile.objects.all()
    scheme_data = scheme.objects.all()
    join_date = str(batch_data.date_of_join)
    student_data = profile_student.objects.filter(batch=batch_id).order_by('roll_no')
    subject_data = subject.objects.all()
    assign_subject_data = subject_to_staff.objects.filter(batch_id=batch_id)
    sem_result = semester_result.objects.filter(batch_id=batch_id)

    subject_in_sem = subject_to_staff.objects.filter(batch_id=batch_id)
    # all_subject = subject.objects.all()

    if 'update_semester' in request.POST:
        sem = request.POST.get('semester')
        batch_data_update = batch.objects.get(id=batch_id)
        sem = int(sem)
        batch_data_update.semester = sem
        batch_data_update.save()
        messages.error(request, 'Successfully Updated the semester')
        return redirect(update_class_of_tutor, batch_id)

    return render(request, 'update_class_of_tutor.html',
                  {

                      'context': context,
                      'staff_data': staff_data,
                      'batch_data': batch_data,
                      'scheme_data': scheme_data,
                      'date': join_date,
                      'student_data': student_data,
                      'assign_subject_data': assign_subject_data,
                      'subject_data': subject_data,
                      'semester_result': sem_result,

                      'subject_in_sem': subject_in_sem,
                      'staff_details': staff_details,

                  })


# Subject Wise mark and attendance report

def tutor_subject_wise_report(request, subject_id, batch_id, ):
    print(subject_id)
    current_user = request.user
    user_id = current_user.username

    staff_details = profile.objects.get(Faculty_unique_id=user_id)
    fullname = staff_details.First_name + " " + staff_details.Last_name
    context = {'name': fullname}

    student_data = profile_student.objects.filter(batch=batch_id).order_by('roll_no')
    subject_data = subject.objects.filter(id=subject_id)
    batch_data = batch.objects.filter(id=batch_id)

    # staff_id = staff_details.id
    # check_subject_exist = subject_to_staff.objects.filter(batch_id=batch_id, staff_id=staff_id, subject_id=subject_id)
    internal_mark = Internal_mark.objects.filter()

    total_attendance = attendance_record.objects.filter(batch_id=batch_id, subject_id=subject_id).aggregate(
        Sum('no_of_hours'))

    attendance_record_data = attendance_record.objects.filter(batch_id=batch_id, subject_id=subject_id)
    total_hour = total_attendance['no_of_hours__sum']
    if total_hour == None:
        messages.error(request, "Attendance not entered ")
        return redirect(update_class_of_tutor, batch_id)
    print(total_attendance, total_hour, type(total_hour))

    attendance_data = attendance.objects.filter(batch_id=batch_id, subject_id=subject_id)

    attenance_list = []
    for i in student_data:
        hour = 0
        for j in attendance_data:
            if i.id == j.student_id:
                if j.present == True:
                    id1 = j.attendance_record_id
                    # print('id',id1, type(id1))
                    no_of_hours_taken = attendance_record.objects.get(id=id1)

                    hour = hour + int(no_of_hours_taken.no_of_hours)

        percentage_attendance = (hour / total_hour) * 100
        # print(i.first_name, hour)
        att_tuple = (i.register_no, percentage_attendance)
        attenance_list.append(att_tuple)

    mark_data = Internal_mark.objects.filter(subject_id=subject_id)

    total_mark_list = []
    for i in student_data:
        for j in mark_data:
            if i.id == j.student_id:
                sum_of_mark = Internal_mark.objects.filter(student_id=i.id, subject_id=subject_id).aggregate(
                    Sum('mark'))
                total_internal = sum_of_mark['mark__sum']
                mark_tupple = (i.register_no, total_internal)
        total_mark_list.append(mark_tupple)

    return render(request, 'subject_wise_report.html',
                  {
                      'context': context,
                      'student_data': student_data,
                      'subject_data': subject_data,
                      'batch_data': batch_data,
                      # 'check_subject_exist': check_subject_exist,
                      'internal_mark': internal_mark,
                      'attendance_data': attendance_data,
                      'attendance_record_data': attendance_record_data,
                      'attendance_list': attenance_list,
                      'total_mark_list': total_mark_list,
                      'staff_details': staff_details,
                  })


# University Result

def university_result(request, batch_id):
    current_user = request.user
    user_id = current_user.username

    staff_details = profile.objects.get(Faculty_unique_id=user_id)
    fullname = staff_details.First_name + " " + staff_details.Last_name
    context = {'name': fullname}

    student_data = profile_student.objects.filter(batch=batch_id)

    if 'semester' in request.POST:
        sem = request.POST.get('semester')
        print(sem, type(sem))
        sem = int(sem)
        subject_data = subject.objects.all()

        subject_this_sem = subject_to_staff.objects.filter(semester=sem, batch_id=batch_id)

        return render(request, 'university_result.html',
                      {
                          'context': context,
                          'student_data': student_data,
                          'subject_data': subject_data,
                          'subject_this_sem': subject_this_sem,
                          'staff_details': staff_details,
                      })

    return render(request, 'university_result.html',
                  {
                      'context': context,
                      'student_data': student_data,
                      'staff_details': staff_details,
                  })


# View and update Student Profile
def update_student_profile(request, student_id):
    current_user = request.user
    user_id = current_user.username

    staff_details = profile.objects.get(Faculty_unique_id=user_id)
    fullname = staff_details.First_name + " " + staff_details.Last_name
    context = {'name': fullname}

    print(student_id)
    id = int(student_id)
    student_data = profile_student.objects.filter(id=id)

    for i in student_data:
        batch_id = i.batch
        date_of_birth = i.date_of_birth
        name_first = i.first_name
        name_last = i.last_name

    batch_data = batch.objects.get(id=batch_id)
    tutor_id = batch_data.tutor_id
    tutor_data = profile.objects.filter(id=tutor_id)
    for tutor_data in tutor_data:
        tutor_name = tutor_data.First_name + " " +tutor_data.Last_name

    scheme_id = batch_data.scheme
    scheme_data = scheme.objects.get(id=scheme_id)
    assign_subject_data = subject_to_staff.objects.filter(batch_id=batch_id)
    subject_data = subject.objects.all()
    date_dob = str(date_of_birth)  # dob can only display in html only as string type
    internal_mark_data = Internal_mark.objects.filter(student_id=student_id)

    for i in internal_mark_data:
        print(i.exam_type, i.mark)
    total_mark_list = []
    attendance_list = []
    sem_result_list = []

    for i in assign_subject_data:

        sum_of_mark = Internal_mark.objects.filter(student_id=id, subject_id=i.subject_id).aggregate(Sum('mark'))
        total_internal = sum_of_mark['mark__sum']
        st_data = profile_student.objects.get(id=id)
        mark_tupple = (i.subject_id, st_data.register_no, i.semester, total_internal)
        # x print(mark_tupple)
        total_mark_list.append(mark_tupple)

        total_attendance = attendance_record.objects.filter(batch_id=batch_id, subject_id=i.subject_id).aggregate(
            Sum('no_of_hours'))
        attendance_record_data = attendance_record.objects.filter(batch_id=batch_id, subject_id=i.subject_id)
        total_hour = total_attendance['no_of_hours__sum']
        print('total_hour', total_hour, type(total_hour))
        attendance_data = attendance.objects.filter(batch_id=batch_id, subject_id=i.subject_id)

        if total_hour == None:
            att_tuple = (i.subject_id, st_data.register_no, i.semester, 0)
            attendance_list.append(att_tuple)

        else:
            hour = 0
            for j in attendance_data:
                if st_data.id == j.student_id:
                    if j.present == True:
                        id1 = j.attendance_record_id
                        # print('id',id1, type(id1))
                        no_of_hours_taken = attendance_record.objects.get(id=id1)

                        hour = hour + no_of_hours_taken.no_of_hours
            percentage_attendance = round((hour / total_hour) * 100, 2)
            print(st_data.first_name, hour)
            att_tuple = (i.subject_id, st_data.register_no, i.semester, percentage_attendance)
            attendance_list.append(att_tuple)

        max_chances = semester_result.objects.filter(subject_id=i.subject_id,
                                                     university_no=st_data.university_no).aggregate(
            Max('no_of_chances'))

        sem_result_data = semester_result.objects.filter(subject_id=i.subject_id, university_no=st_data.university_no,
                                                         no_of_chances=max_chances['no_of_chances__max'])

        print(max_chances['no_of_chances__max'])
        for result in sem_result_data:
            print(result)
            sem_result_tuple = (i.subject_id, st_data.register_no, i.semester, result.grade_point, result.no_of_chances)
            sem_result_list.append(sem_result_tuple)
    # print(attendance_list)
    # print(total_mark_list)

    if 'edit_profile' in request.POST:

        f_name = request.POST.get('first_name')
        l_name = request.POST.get('last_name')
        gender = request.POST.get('gender')
        dob = request.POST.get('date_of_birth')
        ph_no = request.POST.get('phone_no')
        email = request.POST.get('email')
        address = request.POST.get('address')
        aadhaar_no = request.POST.get('aadhaar_no')
        caste = request.POST.get('caste')
        religion = request.POST.get('religion')
        nationality = request.POST.get('nationality')
        native_place = request.POST.get('native_place')
        blood_group = request.POST.get('blood_group')
        university_no = request.POST.get('university_no')
        roll_no = request.POST.get('roll_no')

        # parents details

        # Father
        father_name = request.POST.get('father_name')
        father_occupation = request.POST.get('father_occupation')
        father_address = request.POST.get('father_address')
        father_phn = request.POST.get('father_phn')
        father_email = request.POST.get('father_email')

        # Mother
        mother_name = request.POST.get('mother_name')
        mother_occupation = request.POST.get('mother_occupation')
        mother_address = request.POST.get('mother_address')
        mother_phn = request.POST.get('mother_phn')
        mother_email = request.POST.get('mother_email')

        # Guardian
        guardian_name = request.POST.get('guardian_name')
        guardian_relationship = request.POST.get('guardian_relationship')
        guardian_occupation = request.POST.get('guardian_occupation')
        guardian_address = request.POST.get('guardian_address')
        guardian_phn = request.POST.get('guardian_phn')
        guardian_email = request.POST.get('guardian_email')

        # Hostel Accommodation
        '''hostel_add_1styear = request.POST.get('hostel_add_1styear')
        reason_for_leave_1styear = request.POST.get('reason_for_leave_1styear')

        hostel_add_2ndyear = request.POST.get('hostel_add_2ndyear')
        reason_for_leave_2ndyear = request.POST.get('reason_for_leave_2ndyear')

        hostel_add_3rdyear = request.POST.get('hostel_add_3rdyear')
        reason_for_leave_3rdyear = request.POST.get('reason_for_leave_3rdyear')

        hostel_add_4thyear = request.POST.get('hostel_add_4thyear')
        reason_for_leave_4thyear = request.POST.get('reason_for_leave_4thyear')'''

        # SSLC
        sslc_name_of_institution = request.POST.get('sslc_name_of_institution')
        sslc_passed_date = request.POST.get('sslc_passed_date')
        sslc_regno = request.POST.get('sslc_regno')
        sslc_percentage = float(request.POST.get('sslc_percentage'))
        sslc_chances = request.POST.get('sslc_chances')

        # SSLC Marks
        sslc_mal = request.POST.get('sslc_mal')
        sslc_hindi = request.POST.get('sslc_hindi')
        sslc_english = request.POST.get('sslc_english')
        sslc_physics = request.POST.get('sslc_physics')
        sslc_chemistry = request.POST.get('sslc_chemistry')
        sslc_maths = request.POST.get('sslc_maths')
        sslc_biology = request.POST.get('sslc_biology')

        # PLUS TWO
        plus_two_name_of_institution = request.POST.get('plus_two_name_of_institution')
        plus_two_passed_date = request.POST.get('plus_two_passed_date')
        plus_two_regno = request.POST.get('plus_two_regno')
        plus_two_percentage = request.POST.get('plus_two_percentage')
        plus_two_chances = request.POST.get('plus_two_chances')

        # PLUS TWO Marks
        plus_two_mal = request.POST.get('plus_two_mal')
        plus_two_hindi = request.POST.get('plus_two_hindi')
        plus_two_english = request.POST.get('plus_two_english')
        plus_two_physics = request.POST.get('plus_two_physics')
        plus_two_chemistry = request.POST.get('plus_two_chemistry')
        plus_two_maths = request.POST.get('plus_two_maths')
        plus_two_biology = request.POST.get('plus_two_biology')
        plus_two_computer_science = request.POST.get('plus_two_computer_science')

        if gender == '0':
            messages.error(request, "Please select a valid Gender")
            return redirect(update_student_profile, student_id)
        elif blood_group == '0':
            messages.error(request, "Please select a valid blood Group")
            return redirect(update_student_profile, student_id)
        else:

            student_data1 = profile_student.objects.get(id=id)
            st_dt = profile_student.objects.filter(~Q(register_no=student_data1.register_no), aadhar_no=aadhaar_no).count()

            if st_dt == 0:

                student_data1 = profile_student.objects.get(id=id)
                username = student_data1.register_no
                user_data = MyUser.objects.get(username=username)
                student_login_id = user_data.id

                user_data.first_name = f_name
                user_data.last_name = l_name
                user_data.save()  # update the first and second name in login table

                student_data1.university_no = university_no
                student_data1.roll_no = roll_no
                student_data1.first_name = f_name
                student_data1.first_name = f_name
                student_data1.last_name = l_name
                student_data1.aadhar_no = aadhaar_no
                student_data1.address = address
                student_data1.phone_no = ph_no
                student_data1.email = email
                student_data1.sex = gender
                student_data1.date_of_birth = dob
                student_data1.nationality = nationality
                student_data1.religion = religion
                student_data1.caste = caste
                student_data1.native_place = native_place
                student_data1.blood_group = blood_group

                student_data1.save()

                if parents.objects.filter(student_id=student_login_id):
                    update_parent = parents.objects.get(student_id=student_login_id)
                    update_parent.fathers_name = father_name
                    update_parent.fathers_occupation = father_occupation
                    update_parent.fathers_number = father_phn
                    update_parent.fathers_email_id = father_email
                    update_parent.fathers_address = father_address

                    update_parent.mothers_name = mother_name
                    update_parent.mothers_occupation = mother_occupation
                    update_parent.mothers_number = mother_phn
                    update_parent.mothers_email_id = mother_email
                    update_parent.mothers_address = mother_address
                    update_parent.save()

                if local_guardian.objects.filter(student_id=student_login_id):
                    update_guardian = local_guardian.objects.get(student_id=student_login_id)
                    update_guardian.name = guardian_name
                    update_guardian.address = guardian_address
                    update_guardian.number = guardian_phn
                    update_guardian.email_id = guardian_email
                    update_guardian.occupation = guardian_occupation
                    update_guardian.relationship = guardian_relationship
                    update_guardian.save()

                if qualification.objects.filter(student_id=student_login_id, name_of_exam='SSLC'):
                    sslc_data = qualification.objects.get(student_id=student_login_id, name_of_exam='SSLC')

                    sslc_data.name_of_institution = sslc_name_of_institution
                    sslc_data.date_of_course = sslc_passed_date
                    sslc_data.register_number = sslc_regno
                    sslc_data.mark_percentage = sslc_percentage
                    sslc_data.no_of_chances = sslc_chances
                    sslc_data.biology = sslc_biology
                    sslc_data.chemistry = sslc_chemistry
                    sslc_data.computer = 'Nil'
                    sslc_data.english = sslc_english
                    sslc_data.hindi = sslc_hindi
                    sslc_data.mal = sslc_mal
                    sslc_data.maths = sslc_maths
                    sslc_data.physics = sslc_physics
                    sslc_data.save()

                if qualification.objects.filter(student_id=student_login_id, name_of_exam='PLUS TWO'):
                    plus_two_data = qualification.objects.get(student_id=student_login_id, name_of_exam='PLUS TWO')

                    plus_two_data.name_of_institution = plus_two_name_of_institution
                    plus_two_data.date_of_course = plus_two_passed_date
                    plus_two_data.register_number = plus_two_regno
                    plus_two_data.mark_percentage = plus_two_percentage
                    plus_two_data.no_of_chances = plus_two_chances
                    plus_two_data.biology = plus_two_biology
                    plus_two_data.chemistry = plus_two_chemistry
                    plus_two_data.computer = plus_two_computer_science
                    plus_two_data.english = plus_two_english
                    plus_two_data.hindi = plus_two_hindi
                    plus_two_data.mal = plus_two_mal
                    plus_two_data.maths = plus_two_maths
                    plus_two_data.physics = plus_two_physics
                    plus_two_data.save()

                admission_quota = request.POST.get('admission_quota')
                last_institution = request.POST.get('last_institution')
                reason_for_leaving = request.POST.get('reason_for_leaving')
                tc_number = request.POST.get('tc_number')
                tc_date = request.POST.get('tc_date')

                admission_data = admission_details.objects.get(student_id=student_login_id)
                admission_data.admission_quota = admission_quota
                admission_data.last_studied_institution = last_institution
                admission_data.reason_for_leaving = reason_for_leaving
                admission_data.tc_no = tc_number
                admission_data.tc_date = tc_date
                admission_data.save()
                messages.error(request, "Successfully updated")
                return redirect(update_student_profile, student_id)
            else:
                messages.error(request, "Please enter correct aadhar number")
                return redirect(update_student_profile, student_id)

    if 'is_edit_true' in request.POST:
        student_data1 = profile_student.objects.get(id=id)
        student_data1.is_edit = True
        student_data1.save()
        messages.error(request, "Student can edit profile")
        return redirect(update_student_profile, student_id)

    if 'is_edit_false' in request.POST:
        student_data1 = profile_student.objects.get(id=id)
        student_data1.is_edit = False
        student_data1.save()
        messages.error(request, "Student cannot edit profile")
        return redirect(update_student_profile, student_id)

    if 'change_password' in request.POST:
        # current_password = request.POST.get('current_password')
        new_password = request.POST.get('new_password')
        renew_password = request.POST.get('renew_password')
        student_data1 = profile_student.objects.get(id=id)

        user_data = MyUser.objects.get(username=student_data1.register_no)
        user_password = user_data.password

        if new_password != renew_password:
            messages.error(request, "Password mismatch")
            return redirect(update_student_profile, student_id)
        # elif current_password != user_password:
        #    messages.error(request, "incorrect old password")
        else:
            new_hashed = make_password(new_password)
            user_data.password = new_hashed
            user_data.save()
            messages.error(request, "Successfully changed password")
            return redirect(update_student_profile, student_id)

    std_profile_data_login = profile_student.objects.get(id=id)
    login_details = MyUser.objects.get(username=std_profile_data_login.register_no)

    student_login_id = login_details.id

    parents_data = parents.objects.filter(student_id=student_login_id)
    guardian_data = local_guardian.objects.filter(student_id=student_login_id)
    sslc_data = qualification.objects.filter(student_id=student_login_id, name_of_exam='SSLC')
    plus_two_data = qualification.objects.filter(student_id=student_login_id, name_of_exam='PLUS TWO')
    ad_data = admission_details.objects.filter(student_id=student_login_id)

    tc_date_ = '00-00-0000'
    for i in ad_data:
        tc_date_ = str(i.tc_date)
    # print('student_id', student_id, id)

    sslc_data_date = '00-00-0000'
    plus_two_data_date = '00-00-0000'
    for i in sslc_data:
        sslc_data_date = str(i.date_of_course)

    for i in plus_two_data:
        plus_two_data_date = str(i.date_of_course)
    return render(request, 'update_student_profile.html',
                  {
                      'student_data': student_data,
                      'scheme_data': scheme_data,
                      'batch_data': batch_data,
                      'date_dob': date_dob,
                      'context': context,
                      'assign_subject_data': assign_subject_data,
                      'subject_data': subject_data,
                      'internal_mark_data': internal_mark_data,
                      'total_mark_list': total_mark_list,
                      'attendance_list': attendance_list,
                      'sem_result_list': sem_result_list,
                      'parents_data': parents_data,
                      'guardian_data': guardian_data,
                      'sslc_data': sslc_data,
                      'plus_two_data': plus_two_data,
                      'ad_data': ad_data,

                      'sslc_data_date': sslc_data_date,
                      'plus_two_data_date': plus_two_data_date,
                      'tc_date_': tc_date_,
                      'tutor_name': tutor_name,
                      'staff_details': staff_details,
                  })


# Selecting the sem, month and year for add sem result
def add_result(request, batch_id):
    current_user = request.user
    user_id = current_user.username

    staff_details = profile.objects.get(Faculty_unique_id=user_id)
    fullname = staff_details.First_name + " " + staff_details.Last_name
    context = {'name': fullname}

    batch_id = int(batch_id)
    sem_result = semester_result.objects.filter(batch_id=batch_id).order_by('semester')

    if 'select_sem_and_year' in request.POST:
        month_year = request.POST.get('month_and_year')
        semester = request.POST.get('sem')
        month_year = month_year.split('-')

        print(month_year, type(month_year))
        print(semester, type(semester))
        month = int(month_year[1])
        year = int(month_year[0])
        print(month, year)
        return redirect(add_sem_result, batch_id, int(month), year, semester)
    return render(request, 'add_result.html', {
        'context': context,
        'sem_result': sem_result,
        'staff_details': staff_details,
    })


# Adding the sem result

def add_sem_result(request, batch_id, month, year, semester):
    current_user = request.user
    user_id = current_user.username

    staff_details = profile.objects.get(Faculty_unique_id=user_id)
    fullname = staff_details.First_name + " " + staff_details.Last_name
    context = {'name': fullname}

    student_data = profile_student.objects.filter(batch=batch_id)
    subject_in_sem = subject_to_staff.objects.filter(batch_id=batch_id, semester=semester)
    all_subject = subject.objects.all()
    sem_result = semester_result.objects.filter(semester=semester, batch_id=batch_id)

    batch_data = batch.objects.get(id=batch_id)
    batch_scheme_id = batch_data.scheme
    batch_scheme_data = scheme.objects.get(id=batch_scheme_id)
    batch_scheme = batch_scheme_data.scheme
    print(batch_scheme)

    if request.method == 'POST':
        mark_list = []
        for j in student_data:
            for i in subject_in_sem:
                name_of_tag = str(j.university_no) + '-' + str(i.subject_id)
                print(name_of_tag)
                x = request.POST.getlist(name_of_tag)
                print(x)

                mark_tuple = (j.university_no, i.subject_id, float(x[0]))
                mark_list.append(mark_tuple)
                # print(type(int(month)))
                print(month)
                month_int = month
                year_int = year
                already_exist = semester_result.objects.filter(university_no=j.university_no, subject_id=i.subject_id,
                                                               grade_point=float(x[0]))
                if already_exist:
                    pass
                else:
                    chance_count = semester_result.objects.filter(university_no=j.university_no,
                                                                  subject_id=i.subject_id).count()
                    if chance_count == 0:
                        semester_result.objects.create(university_no=j.university_no, subject_id=i.subject_id,
                                                       grade_point=float(x[0]), semester=semester, month=month_int,
                                                       year=year_int, batch_id=batch_id, no_of_chances=1)
                    else:
                        chance_count += 1
                        semester_result.objects.create(university_no=j.university_no, subject_id=i.subject_id,
                                                       grade_point=float(x[0]), semester=semester, month=month_int,
                                                       year=year_int, batch_id=batch_id, no_of_chances=chance_count)

                # print(x)
        print(mark_list)

        return redirect(report, batch_id, semester)
        # return redirect(update_class_of_tutor, batch_id=batch_id)
    return render(request, 'add_sem_result.html',
                  {
                      'context': context,
                      'student_data': student_data,
                      'subject_in_sem': subject_in_sem,
                      'all_subject': all_subject,
                      'semester_result': sem_result,
                      'batch_scheme': batch_scheme,
                      'staff_details': staff_details,
                  })


# Generate report

def report(request, batch_id, semester):
    current_user = request.user
    user_id = current_user.username

    staff_details = profile.objects.get(Faculty_unique_id=user_id)
    fullname = staff_details.First_name + " " + staff_details.Last_name
    context = {'name': fullname}

    batch_data = batch.objects.filter(id=batch_id)
    student_data = profile_student.objects.filter(batch=batch_id)
    result_data = semester_result.objects.filter(batch_id=batch_id, semester=semester)
    subject_data = subject.objects.all()
    subject_in_sem_id = subject_to_staff.objects.filter(semester=semester, batch_id=batch_id)

    previous_sem = range(1, semester)
    print(previous_sem)

    mark_report = []

    total_credit = 0
    for j in subject_in_sem_id:
        for subj in subject_data:
            if subj.id == j.subject_id:
                total_credit += subj.credit

    print('credit', total_credit)
    for i in student_data:
        arrears_in_current_sem = 0
        absent = 0
        sgpa = 0
        for j in subject_in_sem_id:
            for subj in subject_data:
                if subj.id == j.subject_id:
                    for result in result_data:
                        if i.university_no == result.university_no:
                            if result.subject_id == subj.id:
                                if result.no_of_chances == 1:
                                    if result.grade_point == 0:
                                        arrears_in_current_sem += 1
                                    if result.grade_point == -1:
                                        absent += 1
                                    gpi = result.grade_point
                                    if result.grade_point == -1:
                                        gpi = 0
                                    sgpa = sgpa + (subj.credit * gpi)
        print(i.first_name, sgpa)
        tuple_data = (i.university_no, arrears_in_current_sem, absent, round(sgpa / total_credit, 2))
        mark_report.append(tuple_data)
    print(mark_report)

    prev_sem_arrears = []
    for i in range(1, semester+1):
        for j in student_data:
            count = 0
            subject_in_sem = subject_to_staff.objects.filter(semester=i)
            for subject_in_sem in subject_in_sem:
                if semester_result.objects.filter(subject_id=subject_in_sem.subject_id, semester=i,
                                                  university_no=j.university_no).count() > 1:
                    chance = semester_result.objects.filter(subject_id=subject_in_sem.subject_id, semester=i,
                                                            university_no=j.university_no).count()
                    supply = semester_result.objects.filter(subject_id=subject_in_sem.subject_id, semester=i,
                                                            university_no=j.university_no, no_of_chances=chance,
                                                            grade_point__lte=0)
                    if supply:
                        count += 1
                else:
                    # chance = semester_result.objects.filter(subject_id = subject_in_sem.subject_id, semester=i,
                    # university_no=j.university_no).count()
                    supply = semester_result.objects.filter(subject_id=subject_in_sem.subject_id, semester=i,
                                                            university_no=j.university_no, no_of_chances=1,
                                                            grade_point__lte=0)
                    if supply:
                        count += 1
            arrear_tuple = (j.university_no, i, count)
            prev_sem_arrears.append(arrear_tuple)

    print(prev_sem_arrears)

    absent_in_each_subject = []
    no_of_students_passed = []
    no_of_students_failed = []
    no_of_o_grade = []
    failed_only_this_subj = []
    students_appeared = []
    total_students = profile_student.objects.filter(batch=batch_id).count()
    for i in subject_in_sem_id:
        for j in subject_data:
            if i.subject_id == j.id:
                no_of_absent = semester_result.objects.filter(subject_id=j.id, no_of_chances=1, semester=semester,
                                                              grade_point=-1).count()
                absent_subject_tuple = (j.code, no_of_absent)
                absent_in_each_subject.append(absent_subject_tuple)

    for i in subject_in_sem_id:
        for j in subject_data:
            if i.subject_id == j.id:
                no_of_passed = semester_result.objects.filter(subject_id=j.id, no_of_chances=1, semester=semester,
                                                              grade_point__gte=5.5).count()
                passed = (j.code, no_of_passed)
                no_of_students_passed.append(passed)

    for i in subject_in_sem_id:
        for j in subject_data:
            if i.subject_id == j.id:
                no_of_failed = semester_result.objects.filter(subject_id=j.id, no_of_chances=1, semester=semester,
                                                              grade_point__lte=0).count()
                failed = (j.code, no_of_failed)
                no_of_students_failed.append(failed)
    print('subj', no_of_students_failed)
    for i in no_of_students_failed:
        print(i)

    for i in subject_in_sem_id:
        for j in subject_data:
            if i.subject_id == j.id:
                no_of_o_gr = semester_result.objects.filter(subject_id=j.id, no_of_chances=1, semester=semester,
                                                            grade_point=10).count()
                no_o_grade = (j.code, no_of_o_gr)
                no_of_o_grade.append(no_o_grade)

    print('grade', no_of_o_grade)
    for i in subject_in_sem_id:
        for j in subject_data:
            if i.subject_id == j.id:
                no_of_absent = semester_result.objects.filter(subject_id=j.id, no_of_chances=1, semester=semester,
                                                              grade_point=-1).count()
                appeared_subject_tuple = (j.code, total_students - no_of_absent)
                students_appeared.append(appeared_subject_tuple)

    pass_per_by_total = []
    for i in subject_in_sem_id:
        for j in subject_data:
            if i.subject_id == j.id:
                no_of_passed = semester_result.objects.filter(subject_id=j.id, no_of_chances=1, semester=semester,
                                                              grade_point__gte=5).count()
                passed_perc = (j.code, round((no_of_passed / total_students * 100), 2))
                pass_per_by_total.append(passed_perc)

    appeared_perc = []
    for i in students_appeared:
        for j in no_of_students_passed:
            if i[0] == j[0]:
                pass_perc_by_appear = round((j[1] / i[1]) * 100, 2)
                tple = (i[0], pass_perc_by_appear)
                appeared_perc.append(tple)
    print(appeared_perc)

    return render(request, 'report.html',
                  {
                      'context': context,
                      'student_data': student_data,
                      'result_data': result_data,
                      'subject_data': subject_data,
                      'batch_data': batch_data,
                      'semester': semester,
                      'subject_in_sem_id': subject_in_sem_id,
                      'previous_sem': previous_sem,
                      'mark_report': mark_report,
                      'prev_sem_arrears': prev_sem_arrears,
                      'absent_in_each_subject': absent_in_each_subject,
                      'no_of_students_passed': no_of_students_passed,
                      'no_of_students_failed': no_of_students_failed,
                      'no_of_o_grade': no_of_o_grade,
                      'failed_only_this_subj': failed_only_this_subj,
                      'total_students': total_students,
                      'students_appeared': students_appeared,
                      'pass_per_by_total': pass_per_by_total,
                      'appeared_perc': appeared_perc,
                      'staff_details': staff_details,

                  })


def performance_analysis(request, batch_id):
    current_user = request.user
    user_id = current_user.username

    staff_details = profile.objects.get(Faculty_unique_id=user_id)
    fullname = staff_details.First_name + " " + staff_details.Last_name
    context = {'name': fullname}

    student_data = profile_student.objects.filter(batch=batch_id)

    if request.method == 'POST':
        sem = int(request.POST.get('semester'))
        student_id = int(request.POST.get('student'))
        print(sem, type(sem), student_id, type(student_id))
        batch_data = batch.objects.get(id=batch_id)
        scheme_id = batch_data.scheme
        scheme_data = scheme.objects.get(id=scheme_id)

        # date_dob = str(date_of_birth)  # dob can only display in html only as string type
        assign_subject_data = subject_to_staff.objects.filter(batch_id=batch_id, semester=sem)
        internal_mark_data = Internal_mark.objects.filter(student_id=student_id)
        subject_data = subject.objects.all()
        for i in internal_mark_data:
            print(i.exam_type, i.mark)
        total_mark_list = []
        attendance_list = []
        sem_result_list = []

        st_id = student_id
        for i in assign_subject_data:

            sum_of_mark = Internal_mark.objects.filter(student_id=st_id, subject_id=i.subject_id).aggregate(Sum('mark'))
            print(sum_of_mark['mark__sum'])
            total_internal = sum_of_mark['mark__sum']
            print(total_internal)
            st_data = profile_student.objects.get(id=student_id)
            mark_tupple = (i.subject_id, st_data.register_no, i.semester, total_internal)
            # x print(mark_tupple)
            total_mark_list.append(mark_tupple)

            total_attendance = attendance_record.objects.filter(batch_id=batch_id, subject_id=i.subject_id).aggregate(
                Sum('no_of_hours'))
            attendance_record_data = attendance_record.objects.filter(batch_id=batch_id, subject_id=i.subject_id)
            total_hour = total_attendance['no_of_hours__sum']
            print('total_hour', total_hour, type(total_hour))
            attendance_data = attendance.objects.filter(batch_id=batch_id, subject_id=i.subject_id)

            if total_hour == None:
                att_tuple = (i.subject_id, st_data.register_no, i.semester, 0)
                attendance_list.append(att_tuple)

            else:
                hour = 0
                for j in attendance_data:
                    if st_data.id == j.student_id:
                        if j.present == True:
                            id1 = j.attendance_record_id
                            # print('id',id1, type(id1))
                            no_of_hours_taken = attendance_record.objects.get(id=id1)

                            hour = hour + no_of_hours_taken.no_of_hours
                percentage_attendance = round((hour / total_hour) * 100, 2)
                print(st_data.first_name, hour)
                att_tuple = (i.subject_id, st_data.register_no, i.semester, percentage_attendance)
                attendance_list.append(att_tuple)

            max_chances = semester_result.objects.filter(subject_id=i.subject_id,
                                                         university_no=st_data.university_no).aggregate(
                Max('no_of_chances'))

            sem_result_data = semester_result.objects.filter(subject_id=i.subject_id,
                                                             university_no=st_data.university_no,
                                                             no_of_chances=max_chances['no_of_chances__max'])

            print(max_chances['no_of_chances__max'])
            for result in sem_result_data:
                print(result)
                sem_result_tuple = (
                    i.subject_id, st_data.register_no, i.semester, result.grade_point, result.no_of_chances)
                sem_result_list.append(sem_result_tuple)
        print('attendance', attendance_list)
        print('mark', total_mark_list)
        print('sem_result', sem_result_list)

        sub_name = []
        data = []
        for i in assign_subject_data:
            for j in subject_data:
                if i.subject_id == j.id:
                    sub_name.append(str(j.code))
                    for k in sem_result_list:
                        if k[0] == j.id:
                            if k[3] < 5:
                                data.append(0)
                            else:
                                data.append(k[3])

        print(sub_name, data)

    return render(request, 'performance.html',
                  {
                      'context': context,
                      'student_data': student_data,
                      'data': data,
                      'sub_name': sub_name,
                      'staff_details': staff_details,
                  })


# logout

def log_out(request):
    logout(request)
    return redirect(login.views.login)

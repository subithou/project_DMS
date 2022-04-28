from datetime import date, datetime
from functools import total_ordering
from django.forms import Form
from django.db.models import Sum

from psycopg2 import Date
from pytest import mark
import urllib3
import login
from django.contrib.auth import logout
from django.shortcuts import render, redirect
from django.contrib import messages

from hod.models import  Internal_mark, attendance_record, scheme, subject, subject_to_staff, batch, attendance
from staff.models import profile
from login.models import User
from student.models import profile_student


def staff_index(request):
    user_id = request.session['id']
    staff_details = profile.objects.get(Faculty_unique_id=user_id)
    fullname = staff_details.First_name + " " + staff_details.Last_name
    context = {'name': fullname}

    return render(request, 'staff_index.html', {'context': context})


# Staff profile

def staff_profile(request):
    # name = request.session['staff_name']
    user_id = request.session['id']

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

    if 'change_password' in request.POST:
        current_password = request.POST.get('current_password')
        new_password = request.POST.get('new_password')
        renew_password = request.POST.get('renew_password')

        user_data = User.objects.get(username=user_id)
        user_password = user_data.password

        if new_password != renew_password:
            messages.error(request, "Password mismatch")

        elif current_password != user_password:
            messages.error(request, "incorrect old password")

        else:
            user_data.password = new_password
            user_data.save()
            messages.error(request, "Successfully changed password")

    return render(request, 'staff_profile.html',
                  {
                      'context': context, 
                      'staff_details': staff_details, 
                      'date': date, 
                      'date_dob': dob
                  })


def view_subjects(request):
    user_id = request.session['id']
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
                      'subject_to_this_staff': assigned_subject_to_this_staff
                  })


# view each class and assign the marks and attendance

def update_class(request, batch_id, subject_id):
    user_id = request.session['id']
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

    check_today_attendance_marked = attendance_record.objects.filter(batch_id=batch_id, subject_id=subject_id, date=today)
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
    
    #if 'view_attendance' in request.POST:
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
        'subject_to_staff_data': subject_to_staff_data
        
    })


# Attendance

def add_attendance(request, batch_id, subject_id):
    user_id = request.session['id']
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

        att_record = attendance_record.objects.filter(date=today, from_time=from_time, subject_id=subject_id, batch_id=batch_id)
        
        if att_record:
            messages.error(request, "Attendance already Marked")
            return redirect(add_attendance, batch_id, subject_id)
        else:

            attendance_record.objects.create(date=today, marked=True, subject_id=subject_id, batch_id=batch_id, from_time=from_time,end_time=end_time, no_of_hours=no_of_hours)
            record_id = attendance_record.objects.get(date=today, marked=True, subject_id=subject_id, batch_id=batch_id, from_time=from_time,end_time=end_time, no_of_hours=no_of_hours)
        
            for i in student_data:
                x= i.roll_no
                att_mark = request.POST.get(str(x))
                # print(att_mark, type(att_mark))

                attendance.objects.create(attendance_record_id=record_id.id, student_id=i.id, subject_id=subject_id, batch_id=batch_id, present=att_mark, semester=sem)
            messages.error(request, "Attendance successfully added")
            return redirect('update_class', batch_id, subject_id)
        


    return render(request, 'attendance.html', 
    {
        'context':context,
        'student_data':student_data,
        'subject_data':subject_data,
        'batch_data':batch_data,
        'check_subject_exist': check_subject_exist
    })


def view_attendance(request, record_id, batch_id, subject_id):
    user_id = request.session['id']
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
        'context':context,
        'attendance_data' : attendance_data,
        'student_data':student_data,
        'subject_data':subject_data,
        'batch_data':batch_data,
        'check_subject_exist': check_subject_exist,
        'attendance_record_data': attendance_record_data
    })
    


# Internal 

def add_internal(request, batch_id, subject_id):
    user_id = request.session['id']
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
                x= i.roll_no
                mark = request.POST.getlist(str(x))
                print(mark)

                exist_ass1 = Internal_mark.objects.filter(student_id=i.id, subject_id=subject_id, semester=sem, exam_type='Assignment 1')
                exist_ass2 = Internal_mark.objects.filter(student_id=i.id, subject_id=subject_id, semester=sem, exam_type='Assignment 2')
                exist_internal1 = Internal_mark.objects.filter(student_id=i.id, subject_id=subject_id, semester=sem, exam_type='Internal 1')
                exist_internal2 = Internal_mark.objects.filter(student_id=i.id, subject_id=subject_id, semester=sem, exam_type='Internal 2')
                
                if exist_ass1:
                    update_ass1 = Internal_mark.objects.get(student_id=i.id, subject_id=subject_id, semester=sem, exam_type='Assignment 1')
                    update_ass1.mark = mark[0]
                    update_ass1.save()

                if exist_ass2:
                    update_ass2 = Internal_mark.objects.get(student_id=i.id, subject_id=subject_id, semester=sem, exam_type='Assignment 2')
                    update_ass2.mark = mark[1]
                    update_ass2.save()

                if exist_internal1:
                    update_internal1 = Internal_mark.objects.get(student_id=i.id, subject_id=subject_id, semester=sem, exam_type='Internal 1')
                    update_internal1.mark = mark[2]
                    update_internal1.save()
                
                if exist_internal2:
                    update_internal2 = Internal_mark.objects.get(student_id=i.id, subject_id=subject_id, semester=sem, exam_type='Internal 2')
                    update_internal2.mark = mark[3]
                    update_internal2.save()

                if exist_ass1 == None and exist_ass2 == None and exist_internal2 == None and exist_internal1 == None:
                    Internal_mark.objects.create(student_id=i.id, subject_id=subject_id, semester=sem, mark=mark[0], exam_type='Assignment 1')
                    Internal_mark.objects.create(student_id=i.id, subject_id=subject_id, semester=sem, mark=mark[1], exam_type='Assignment 2')
                    Internal_mark.objects.create(student_id=i.id, subject_id=subject_id, semester=sem, mark=mark[2], exam_type='Internal 1')
                    Internal_mark.objects.create(student_id=i.id, subject_id=subject_id, semester=sem, mark=mark[3], exam_type='Internal 2')

        return redirect('update_class', batch_id, subject_id)

    return render(request, 'internal.html',
    {
        'context':context,
        'student_data':student_data,
        'subject_data':subject_data,
        'batch_data':batch_data,
        'check_subject_exist': check_subject_exist,
        'internal_mark':internal_mark

    })


# view_internal_result
def view_internal_result(request, batch_id, subject_id):
    user_id = request.session['id']
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

    total_attendance = attendance_record.objects.filter(batch_id=batch_id, subject_id=subject_id).aggregate(Sum('no_of_hours'))
    attendance_record_data = attendance_record.objects.filter(batch_id=batch_id, subject_id=subject_id)
    total_hour = total_attendance['no_of_hours__sum']
    # print(total_attendance, total_hour, type(total_hour))
    
    

    
    attendance_data = attendance.objects.filter(batch_id=batch_id, subject_id=subject_id)

    attenance_list = []
    for i in student_data:
        hour = 0
        for j in attendance_data:
            if i.id == j.student_id:
                if j.present == True:
                    id1 =j.attendance_record_id
                    # print('id',id1, type(id1))
                    no_of_hours_taken = attendance_record.objects.get(id=id1)
                    
                    hour = hour +  no_of_hours_taken.no_of_hours
        percentage_attendance = (hour/total_hour)*100
        # print(i.first_name, hour)
        att_tuple = (i.register_no, percentage_attendance)
        attenance_list.append(att_tuple)   

    mark_data = Internal_mark.objects.filter(subject_id=subject_id)

    total_mark_list = []
    for i in student_data:
        for j in mark_data:
            if i.id == j.student_id:
                sum_of_mark = Internal_mark.objects.filter(student_id=i.id, subject_id=subject_id).aggregate(Sum('mark'))
                total_internal = sum_of_mark['mark__sum']
                mark_tupple = (i.register_no, total_internal)
        total_mark_list.append(mark_tupple)


    print(total_mark_list)

    return render(request, 'internal_result.html',
    {
        'context':context,
        'student_data':student_data,
        'subject_data':subject_data,
        'batch_data':batch_data,
        'check_subject_exist': check_subject_exist,
        'internal_mark':internal_mark,
        'attendance_data':attendance_data,
        'attendance_record_data':attendance_record_data,
        'attendance_list':attenance_list,
        'total_mark_list':total_mark_list

    })
# logout

def log_out(request):
    logout(request)
    return redirect(login.views.login)

from atexit import register

import matplotlib as matplotlib
from autoscraper import AutoScraper
from django.contrib.auth.hashers import make_password, check_password
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.contrib import messages
from hod.models import Internal_mark, attendance, attendance_record, batch, scheme, semester_result, subject, \
    subject_to_staff
from staff.models import profile
from student.models import profile_student, parents, local_guardian, qualification, admission_details
from login.models import MyUser
import login
from django.db.models import Q

from django.db.models import Sum, Max

# %matplotlib inline
import matplotlib.pyplot as plt
import numpy as np


def student_index(request):
    # Create your views here.

    url = 'https://ktu.edu.in/eu/core/announcements.htm'

    try:
        # url = 'https://ktu.edu.in/home.htm'

        wanted_list = ['ANNOUNCEMENTS', 'Dec 24, 2021', 'Exam Registration opened - B.Tech S3 and S5 (supplementary) '
                                                        'Jan 2022']
        scraper = AutoScraper()
        result = scraper.build(url, wanted_list)
        data1 = result[0]
        data2 = result[1]
        data3 = result[2]

        notif = {'data1': data1,
                 'data2': data2,
                 'data3': data3
                 }
        # request.session['notif'] = notif


    except:

        notif = {'data1': "KTU site cannot reach"}
    current_user = request.user
    user_id = current_user.username

    student_details_1 = profile_student.objects.get(register_no=user_id)
    name = student_details_1.first_name + " " + student_details_1.last_name
    # id = request.session['student_id']
    context = {'name': name}

    credit = 0
    subject_data = subject.objects.all()
    result_data_for_credit = semester_result.objects.filter(university_no=student_details_1.university_no,
                                                            grade_point__gte=5)
    for i in result_data_for_credit:
        for j in subject_data:
            if j.id == i.subject_id:
                credit += j.credit

    supply = 0
    for i in subject_data:
        max_chance = semester_result.objects.filter(university_no=student_details_1.university_no,
                                                    subject_id=i.id).aggregate(Max('no_of_chances'))
        result_data_for_supply = semester_result.objects.filter(university_no=student_details_1.university_no,
                                                                subject_id=i.id,
                                                                no_of_chances=max_chance['no_of_chances__max'])
        for j in result_data_for_supply:
            if j.grade_point < 5:
                supply += 1

    max_sem = semester_result.objects.filter(university_no=student_details_1.university_no).aggregate(Max('semester'))
    highest_sem = max_sem['semester__max']

    if highest_sem is not None:
        data = []
        sem = []

        sgpa = 0
        for i in range(1, highest_sem + 1):
            sem_sgpa = 0
            sem_credit = 0
            for j in subject_data:
                max_chance = semester_result.objects.filter(university_no=student_details_1.university_no,
                                                            subject_id=j.id, semester=i).aggregate(Max('no_of_chances'))
                result_data = semester_result.objects.filter(university_no=student_details_1.university_no,
                                                             subject_id=j.id, semester=1,
                                                             no_of_chances=max_chance['no_of_chances__max'])
                for k in result_data:
                    if k.subject_id == j.id:
                        if k.grade_point == -1:
                            sem_sgpa += (j.credit * 0)
                        else:
                            sem_sgpa += (j.credit * k.grade_point)
                        sem_credit += j.credit

            sgpa += (sem_sgpa / sem_credit)
            data.append(sgpa)
            sem.append(i)
        cgpa = sgpa / highest_sem
    else:
        data = [0]
        sem = [0]
        cgpa = 0

    x = np.array(data)
    y = np.array(sem)
    x = x.reshape(len(x), 1)

    from sklearn.linear_model import LinearRegression
    model = LinearRegression()

    model.fit(x, y)
    ypred = model.predict(x)

    if highest_sem is not None:
        if highest_sem < 8:
            sem.append(highest_sem + 1)
            predict_sem = highest_sem + 1
            y = (model.coef_[0] * predict_sem) + model.intercept_
            predicted_sem = highest_sem + 1
            data.append(y)
    else:
        predicted_sem = 0
    return render(request, 'student_index.html', {
        'context': context,
        'credit': credit,
        'supply': supply,
        'cgpa': cgpa,
        'notif': notif,
        'data': data,
        'sem': sem,
        'predicted_sem': predicted_sem,
        'student_details_1': student_details_1
    })
    # return redirect(student_profile)


def student_profile(request):
    # name = request.session['student_name']
    current_user = request.user
    user_id = current_user.username
    student_login_id = current_user.id
    print(student_login_id)

    student_details_1 = profile_student.objects.get(register_no=user_id)
    name = student_details_1.first_name + " " + student_details_1.last_name

    id = user_id
    student_data = profile_student.objects.filter(register_no=id)

    for i in student_data:
        print('student', i.id)
        student_id = i.id
        batch_id = i.batch
        date_of_birth = i.date_of_birth
        name_first = i.first_name
        name_last = i.last_name

    print(student_id)
    name = name_first + " " + name_last
    context = {'name': name}  # display the name

    batch_data = batch.objects.get(id=batch_id)

    tutor_id = batch_data.tutor_id
    tutor_data = profile.objects.filter(id=tutor_id)
    for tutor_data in tutor_data:
        tutor_name = tutor_data.First_name + " " +tutor_data.Last_name

    scheme_id = batch_data.scheme
    scheme_data = scheme.objects.get(id=scheme_id)

    date_dob = str(date_of_birth)  # dob can only display in html only as string type
    assign_subject_data = subject_to_staff.objects.filter(batch_id=batch_id)
    internal_mark_data = Internal_mark.objects.filter(student_id=student_id)
    subject_data = subject.objects.all()
    for i in internal_mark_data:
        print(i.exam_type, i.mark)
    total_mark_list = []
    attendance_list = []
    sem_result_list = []

    st_id = student_details_1.id
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

        sem_result_data = semester_result.objects.filter(subject_id=i.subject_id, university_no=st_data.university_no,
                                                         no_of_chances=max_chances['no_of_chances__max'])

        print(max_chances['no_of_chances__max'])
        for result in sem_result_data:
            print(result)
            sem_result_tuple = (i.subject_id, st_data.register_no, i.semester, result.grade_point, result.no_of_chances)
            sem_result_list.append(sem_result_tuple)
    # print(attendance_list)
    print(total_mark_list)

    '''if 'profile_pic' in request.POST:
        myfile = request.POST.get['file']
        fs = FileSystemStorage()
        filename = fs.save(myfile.name, myfile)'''

    if 'edit_profile' in request.POST and student_details_1.is_edit:

        current_user = request.user
        student_login_id = current_user.id

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
            return redirect(student_profile)
        elif blood_group == '0':
            messages.error(request, "Please select a valid blood Group")
            return redirect(student_profile)
        else:

            st_dt = profile_student.objects.filter(~Q(register_no=id), aadhar_no=aadhaar_no).count()
            if st_dt == 0:
                student_data1 = profile_student.objects.get(register_no=id)
                user_data = MyUser.objects.get(username=id)

                user_data.first_name = f_name
                user_data.last_name = l_name
                user_data.save()  # update the first and second name in login table

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
                student_data1.is_edit = False
                # student_data1.photo = profile_photo
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

                else:
                    parents.objects.create(student_id=student_login_id,
                                           fathers_name=father_name, fathers_occupation=father_occupation,
                                           fathers_number=father_phn, fathers_address=father_address,
                                           fathers_email_id=father_email,
                                           mothers_name=mother_name, mothers_occupation=mother_occupation,
                                           mothers_number=mother_phn, mothers_email_id=mother_email,
                                           mothers_address=mother_address)

                if local_guardian.objects.filter(student_id=student_login_id):
                    update_guardian = local_guardian.objects.get(student_id=student_login_id)
                    update_guardian.name = guardian_name
                    update_guardian.address = guardian_address
                    update_guardian.number = guardian_phn
                    update_guardian.email_id = guardian_email
                    update_guardian.occupation = guardian_occupation
                    update_guardian.relationship = guardian_relationship
                    update_guardian.save()

                else:
                    local_guardian.objects.create(student_id=student_login_id,
                                                  name=guardian_name,
                                                  address=guardian_address,
                                                  number=guardian_phn,
                                                  relationship=guardian_relationship,
                                                  email_id=guardian_email,
                                                  occupation=guardian_occupation)

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

                else:
                    qualification.objects.create(student_id=student_login_id,
                                                 name_of_exam='SSLC',
                                                 name_of_institution=sslc_name_of_institution,
                                                 date_of_course=sslc_passed_date,
                                                 register_number=sslc_regno,
                                                 mark_percentage=sslc_percentage,
                                                 no_of_chances=sslc_chances,
                                                 biology=sslc_biology,
                                                 chemistry=sslc_chemistry,
                                                 computer='Nil',
                                                 english=sslc_english,
                                                 hindi=sslc_hindi,
                                                 mal=sslc_mal,
                                                 maths=sslc_maths,
                                                 physics=sslc_physics)

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

                else:
                    qualification.objects.create(student_id=student_login_id,
                                                 name_of_exam='PLS TWO',
                                                 name_of_institution=plus_two_name_of_institution,
                                                 date_of_course=plus_two_passed_date,
                                                 register_number=plus_two_regno,
                                                 mark_percentage=plus_two_percentage,
                                                 no_of_chances=plus_two_chances,
                                                 biology=plus_two_biology,
                                                 chemistry=plus_two_chemistry,
                                                 computer=plus_two_computer_science,
                                                 english=plus_two_english,
                                                 hindi=plus_two_hindi,
                                                 mal=plus_two_mal,
                                                 maths=plus_two_maths,
                                                 physics=plus_two_physics)

                # Admission details
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

                # return render(request, 'student_profile.html',
                #              {'student_data': student_data, 'scheme_data': scheme_data, 'batch_data': batch_data,
                #               'date_dob': date_dob, 'context': context})

                return redirect(student_profile)
            else:
                messages.error(request, "Please enter correct aadhar number")
                return redirect(student_profile)
    if 'change_password' in request.POST:
        current_password = request.POST.get('current_password')
        new_password = request.POST.get('new_password')
        renew_password = request.POST.get('renew_password')

        user_data = MyUser.objects.get(username=id)
        user_password = user_data.password
        # user_data.set_password(new_password)
        # current_hased = make_password(current_password)
        user_decrypted = check_password(current_password, user_password)

        if new_password != renew_password:
            messages.error(request, "Password mismatch")

        elif user_decrypted is False:
            messages.error(request, "incorrect old password")
        else:
            new_hased = make_password(new_password)
            user_data.password = new_hased
            user_data.save()
            messages.error(request, "Successfully changed password")
            return redirect(student_profile)

    print(student_login_id)
    parents_data = parents.objects.filter(student_id=student_login_id)
    guardian_data = local_guardian.objects.filter(student_id=student_login_id)
    sslc_data = qualification.objects.filter(student_id=student_login_id, name_of_exam='SSLC')
    plus_two_data = qualification.objects.filter(student_id=student_login_id, name_of_exam='PLUS TWO')
    ad_data = admission_details.objects.filter(student_id=student_login_id)
    edit_exist = profile_student.objects.filter(register_no=id, is_edit=True).exists()

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

    if edit_exist:
        edit_data = 1
    else:
        edit_data = 0
    return render(request, 'student_profile.html',
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
                      'edit_data': edit_data,
                      'sslc_data_date': sslc_data_date,
                      'plus_two_data_date': plus_two_data_date,
                      'tc_date_': tc_date_,
                      'student_details_1': student_details_1,
                      'tutor_name': tutor_name
                  })


def check_profile_edit(request):
    # username = request.POST.get('username')
    # print(username, type(username))
    edit_exist = profile_student.objects.filter(register_no='2018100', is_edit=True).exists()

    # subject_exist = MyUser.objects.filter(username=username).exists()
    if edit_exist:
        return HttpResponse(True)
    else:
        return HttpResponse(False)


# logout
def log_out(request):
    logout(request)
    return redirect(login.views.login)

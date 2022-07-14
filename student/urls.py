from django.urls import path, include
from hod.views import log_out
from student.views import student_index, student_profile, check_profile_edit

urlpatterns = [
 
    path('', student_index, name='student_index'),
    path('log_out/', log_out, name='log_out'),
    path('student_profile/', student_profile, name='student_profile'),
    path('check_profile_edit', check_profile_edit, name='check_profile_edit'),

]
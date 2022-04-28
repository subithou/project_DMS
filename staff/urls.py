from django.urls import path, include
from staff.views import add_attendance, add_internal,  staff_index, log_out, staff_profile, update_class, view_attendance, view_internal_result, view_subjects

urlpatterns = [
    path('', staff_index, name='staff_index'),
    path('log_out/', log_out, name='log_out'),
    path('staff_profile/', staff_profile, name='staff_profile' ),
    path('view_subjects/', view_subjects, name='view_subjects' ),
    path('update_class/<int:batch_id>/<int:subject_id>/', update_class, name='update_class' ),
    path('attendance/<int:batch_id>/<int:subject_id>/', add_attendance, name='attendance' ),
    path('internal/<int:batch_id>/<int:subject_id>/', add_internal, name='internal' ),
    path('internal_result/<int:batch_id>/<int:subject_id>/', view_internal_result, name='view_internal_result' ),
    path('view_attendance/<int:record_id>/<int:batch_id>/<int:subject_id>/', view_attendance, name='view_attendance' ),

]
from django.contrib import admin

from hod.models import batch, scheme, subject, subject_to_staff

# Register your models here.
@admin.register(batch)
class Batches(admin.ModelAdmin):
    list_display = ('class_name', 'date_of_join','semester','scheme','tutor_id')

@admin.register(subject)
class Subject(admin.ModelAdmin):
    pass

@admin.register(scheme)
class Scheme(admin.ModelAdmin):
    list_display = ('scheme')

@admin.register(subject_to_staff)
class Scheme(admin.ModelAdmin):
    pass

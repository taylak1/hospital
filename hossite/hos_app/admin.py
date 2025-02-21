from django.contrib import admin
from .models import *
from modeltranslation.admin import TranslationAdmin

@admin.register(Department, Specialty, MedicalRecord, Feedback)
class CourseReviewAdmin(TranslationAdmin):

    class Media:
        js = (
            'http://ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min.js',
            'http://ajax.googleapis.com/ajax/libs/jqueryui/1.10.2/jquery-ui.min.js',
            'modeltranslation/js/tabbed_translation_fields.js',
        )
        css = {
            'screen': ('modeltranslation/css/tabbed_translation_fields.css',),
        }


admin.site.register(UserProfile)
admin.site.register(Doctor)
admin.site.register(Patient)
admin.site.register(Appointment)

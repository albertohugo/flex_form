from django.contrib import admin
from .models import Form, Object

class FormAdmin(admin.ModelAdmin):
    model = Form
    list_display = ['title','status',]

class ObjectAdmin(admin.ModelAdmin):
    model = Object
    list_display = ['form','label', 'type']

admin.site.register(Form, FormAdmin)
admin.site.register(Object, ObjectAdmin)
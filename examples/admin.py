from django.contrib import admin
from .models import Form, Object, Result

class FormAdmin(admin.ModelAdmin):
    model = Form
    list_display = ['title','status',]

class ObjectAdmin(admin.ModelAdmin):
    model = Object
    list_display = ['form','label', 'type']

class ResultAdmin(admin.ModelAdmin):
    model = Result
    list_display = ['form','object', 'value']

admin.site.register(Form, FormAdmin)
admin.site.register(Object, ObjectAdmin)
admin.site.register(Result, ResultAdmin)
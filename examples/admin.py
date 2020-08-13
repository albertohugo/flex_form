from django.contrib import admin
from .models import Form, Object, Result, IdResult

class FormAdmin(admin.ModelAdmin):
    model = Form
    list_display = ['title','status',]

class ObjectAdmin(admin.ModelAdmin):
    model = Object
    list_display = ['form','label', 'type']

class ResultAdmin(admin.ModelAdmin):
    model = Result
    list_display = ['form','object', 'id_result','value']

class IdResultAdmin(admin.ModelAdmin):
    model = IdResult
    list_display = ['id','form']

admin.site.register(Form, FormAdmin)
admin.site.register(Object, ObjectAdmin)
admin.site.register(Result, ResultAdmin)
admin.site.register(IdResult, IdResultAdmin)
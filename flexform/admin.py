from django.contrib import admin
from .models import Form, Object, Result, IdResult, FormMember
from django.utils.html import format_html

class FormAdmin(admin.ModelAdmin):
    model = Form
    list_display = ['title','status',]

class FormMemberAdmin(admin.ModelAdmin):
    model = FormMember
    list_display = ['form','role','user']

class ObjectAdmin(admin.ModelAdmin):
    model = Object
    list_display = ['form','label', 'type']

class ResultAdmin(admin.ModelAdmin):
    model = Result
    def image(self, obj):
        return format_html('<img src="{}" />'.format(obj.image))
    image.short_description = 'Image'

    list_display = ['form','object', 'id_result','value', 'image']

class IdResultAdmin(admin.ModelAdmin):
    model = IdResult
    list_display = ['id','form']

admin.site.register(Form, FormAdmin)
admin.site.register(FormMember, FormMemberAdmin)
admin.site.register(Object, ObjectAdmin)
admin.site.register(Result, ResultAdmin)
admin.site.register(IdResult, IdResultAdmin)
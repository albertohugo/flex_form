from django.contrib import admin
from .models import Form

class FormAdmin(admin.ModelAdmin):
    model = Form
    list_display = ['form_title','created_at',]

admin.site.register(Form, FormAdmin)


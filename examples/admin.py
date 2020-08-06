from django.contrib import admin
from .models import Form

class FormAdmin(admin.ModelAdmin):
    model = Form
    list_display = ['title','status',]

admin.site.register(Form, FormAdmin)
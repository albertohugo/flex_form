from django.db import models

class Form(models.Model):
    form_title = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now=True)
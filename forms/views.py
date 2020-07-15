from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views import generic
from django.http import HttpResponseRedirect
from django.shortcuts import render

from .forms import FormTitle
from django import forms

class SignUp(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'signup.html'

class FormTitle(forms.Form):
    form_title = forms.CharField(label='Form Title', max_length=100)
    template_name = 'new_form.html'

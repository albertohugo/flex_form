from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views import generic
from django.http import HttpResponseRedirect
from django.shortcuts import render

from .forms import NameForm
from django import forms

class SignUp(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'signup.html'

def get_name(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = NameForm(request.POST)
        if form.is_valid():
            print(form.cleaned_data['your_name'])
            return HttpResponseRedirect('../..')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = NameForm()

    return render(request, 'new_form.html', {'form': form})

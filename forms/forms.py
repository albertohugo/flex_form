from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views import generic
from django import forms
from bootstrap_modal_forms.forms import BSModalModelForm
from .models import Book

class BookModelForm(BSModalModelForm):
    class Meta:
        model = Book
        fields = ['title', 'author', 'price']

class NameForm(forms.Form):
    your_name = forms.CharField(label='Your name', max_length=100)
    template_name = 'new_form.html'

class SignUp(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'signup.html'
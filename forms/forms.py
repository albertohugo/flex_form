from django.contrib.auth.models import UserCreationForm
from django.urls import reverse_lazy
from django.views import generic
from .forms import PostForm

class SignUp(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'signup.html'
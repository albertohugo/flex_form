from django.urls import path

from . import views


urlpatterns = [
    path('signup/', views.SignUp.as_view(), name='signup'),
    path('new_form/', views.get_name, name='form'),
]
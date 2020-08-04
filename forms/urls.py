from django.urls import path

from . import views


urlpatterns = [
    path('signup/', views.SignUp.as_view(), name='signup'),
    path('new_form/', views.get_name, name='form'),
    path('create/', views.BookCreateView.as_view(), name='create_book'),
]
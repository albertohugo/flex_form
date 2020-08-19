from django.urls import path
from django.views.generic import RedirectView
from django.conf.urls import url

from . import views


urlpatterns = [
    path('', views.Index.as_view(), name='index'),
    path('forms_page/', views.Forms.as_view(), name='forms_page'),
    path('forms/', views.forms, name='forms'),
    path('objects/', views.objects, name='objects'),
    path('open_form/', views.open_form, name='open_form'),
    path('open_list/', views.open_list, name='open_list'),
    path('create_form/', views.FormCreateView.as_view(), name='create_form'),
    path('update_form/<int:pk>', views.FormUpdateView.as_view(), name='update_form'),
    path('read_form/<int:pk>', views.FormReadView.as_view(), name='read_form'),
    path('delete_form/<int:pk>', views.FormDeleteView.as_view(), name='delete_form'),
    path('create_object/<int:pk>', views.ObjectCreateView.as_view(), name='create_object'),
    path('update_object/<int:pk>', views.ObjectUpdateView.as_view(), name='update_object'),
    path('read_object/<int:pk>', views.ObjectReadView.as_view(), name='read_object'),
    path('delete_object/<int:pk>', views.ObjectDeleteView.as_view(), name='delete_object'),
    path('filter/', views.BookFilterView.as_view(), name='filter_book'),
    path('create/', views.BookCreateView.as_view(), name='create_book'),
    path('update/<int:pk>', views.BookUpdateView.as_view(), name='update_book'),
    path('read/<int:pk>', views.BookReadView.as_view(), name='read_book'),
    path('delete/<int:pk>', views.BookDeleteView.as_view(), name='delete_book'),
    path('books/', views.books, name='books'),
    path('signup/', views.SignUpView.as_view(), name='signup'),
    path('login/', views.CustomLoginView.as_view(), name='login'),
    url(r'^favicon\.ico$',RedirectView.as_view(url='static/images/favicon.ico')),
]

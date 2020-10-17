from django.conf.urls import include, url
from django.contrib import admin
from django.urls import path
from flexform import urls, views
from django.views.generic import RedirectView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('flexform.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    #path('', include('flexform.urls')),
    path('', views.Index.as_view(), name='index'),
    path('forms_page/', views.Forms.as_view(), name='forms_page'),
    path('developer/', views.Developer.as_view(), name='developer'),
    path('forms/', views.forms, name='forms'),
    path('objects/', views.objects, name='objects'),
    path('api/insert', views.send_object, name='insert'),
    path('api/update', views.update_object, name='update'),
    path('api/delete', views.delete_object, name='detele'),
    path('open_form/', views.open_form, name='open_form'),
    path('open_list/', views.open_list, name='open_list'),
    path('create_form/', views.FormCreateView.as_view(), name='create_form'),
    path('update_form/<int:pk>', views.FormUpdateView.as_view(), name='update_form'),
    path('read_form/<int:pk>', views.FormReadView.as_view(), name='read_form'),
    path('delete_form/<int:pk>', views.FormDeleteView.as_view(), name='delete_form'),
    path('create_member/<int:pk>', views.MemberCreateView.as_view(), name='create_member'),
    path('read_member/<int:pk>', views.MemberReadView.as_view(), name='read_member'),
    path('update_member/<int:pk>', views.MemberUpdateView.as_view(), name='update_member'),
    path('delete_member/<int:pk>', views.MemberDeleteView.as_view(), name='delete_member'),
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
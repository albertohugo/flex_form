from django.urls import path
from django.views.generic import RedirectView
from django.conf.urls import url, include
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register(r'form',views.FormViewSet)

from . import views


urlpatterns = [
    url(r'^', include (router.urls)),
    url(r'^favicon\.ico$',RedirectView.as_view(url='static/images/favicon.ico')),
]

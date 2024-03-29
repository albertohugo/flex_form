from django.urls import path
from django.views.generic import RedirectView
from django.conf.urls import url, include
from rest_framework import routers
from . import views
from django.conf import settings
from django.conf.urls.static import static

router = routers.DefaultRouter()
#router.register(r'form',views.FormViewSet)
#router.register(r'object',views.ObjectViewSet)
#router.register(r'member',views.FormMemberViewSet)
#router.register(r'result',views.ResultViewSet)
router.register(r'flexform',views.FlexFormGetViewGet)
#router.register(r'set',views.FlexFormSetViewSet)
#router.register(r'set',views.send_object, basename='send_object')
urlpatterns = [
    url(r'^', include (router.urls)),
    url(r'^favicon\.ico$',RedirectView.as_view(url='static/images/favicon.ico')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^led/$', views.led, name='led'),
    url(r'^camera/$', views.camera, name='camera'),
]

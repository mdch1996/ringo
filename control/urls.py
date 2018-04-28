from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^led/$', views.led, name='led'),
    url(r'^temp/$', views.read_temp, name='temp'),
]

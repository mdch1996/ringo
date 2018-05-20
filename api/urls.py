from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^switch/$', views.switch, name='switch'),
    url(r'^read_sensor/$', views.read_sensor, name='read_sensor'),
    # url(r'^set_sensor/$', views.set_sensor, name='set_sensor'),
    # url(r'^temp/$', views.read_temp, name='temp'),
]

from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^switch/$', views.switch, name='switch'),
    # url(r'^temp/$', views.read_temp, name='temp'),
]

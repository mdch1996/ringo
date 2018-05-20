from django.contrib import admin
from . import models


@admin.register(models.Device)
class DeviceAdmin(admin.ModelAdmin):
    list_display = ('id', 'raspberry_pi_code')


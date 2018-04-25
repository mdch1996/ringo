from django.db import models


class Device(models.Model):
    raspberry_pi_code = models.PositiveIntegerField(unique=True, blank=True, null=True)


class Traffic(models.Model):
    uploaded = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    # image = models.ImageField(upload_to='products/%Y/%m/%d', blank=True)

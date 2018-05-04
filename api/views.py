from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.core.exceptions import ObjectDoesNotExist
import RPi.GPIO as GPIO
from datetime import datetime

from . import serializers
from control.models import Device


@api_view(['POST'])
def switch(request):
    serializer = serializers.SwitchSerializer(data=request.data)

    # Pin Definitons:
    led_pin = 40

    # Pin Definitons:
    GPIO.setmode(GPIO.BOARD)  # programming the GPIO by BOARD pin numbers, GPIO21 is called as PIN40
    GPIO.setup(led_pin, GPIO.OUT)  # initialize digital pin40 as an output.

    # Initial state for LEDs:
    GPIO.output(led_pin, GPIO.LOW)

    if serializer.is_valid():
        device = serializer.data.get('device')
        key = serializer.data.get('key')
        # raspberry_pi_code = Device.objects.get(pk=1)
        raspberry_pi_code = 12345

        if device == raspberry_pi_code:
            if key:
                GPIO.output(led_pin, GPIO.HIGH)
            elif not switch:
                GPIO.output(led_pin, GPIO.LOW)

            datetime_now = str(datetime.now())
            data = {
                "date_of_switch": datetime_now,
                "raspberry_pi_code": raspberry_pi_code
            }
            return Response(data=data, status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)

    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.core.exceptions import ObjectDoesNotExist
import RPi.GPIO as GPIO
from datetime import datetime

from . import serializers
from control import models

#thermomeer
import os                                                  # import os module
import glob                                                # import glob module
import time                                                # import time module
os.system('modprobe w1-gpio')                              # load one wire communication device kernel modules
os.system('modprobe w1-therm')
base_dir = '/sys/bus/w1/devices/'                          # point to the address
device_folder = glob.glob(base_dir + '28*')[0]             # find device with address starting from 28*
device_file = device_folder + '/w1_slave'                  # store the details


def read_temp_raw():
    f = open(device_file, 'r')
    lines = f.readlines()                                   # read the device details
    f.close()
    return lines


@api_view(['POST'])
def switch(request):

    # Pin Definitons:
    led_pin = 40

    # Pin Definitons:
    GPIO.setmode(GPIO.BOARD)  # programming the GPIO by BOARD pin numbers, GPIO21 is called as PIN40
    GPIO.setup(led_pin, GPIO.OUT)  # initialize digital pin40 as an output.

    # Initial state for LEDs:
    GPIO.output(led_pin, GPIO.LOW)

    serializer = serializers.SwitchSerializer(data=request.data)
    if serializer.is_valid():
        device = serializer.data.get('device')
        key = serializer.data.get('key')
        raspberry_pi_code = models.Device.objects.get(pk=1).raspberry_pi_code
        # raspberry_pi_code = 12345

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


@api_view(['POST'])
def read_sensor(request):
    serializer = serializers.ReadSensorSerializer(data=request.data)
    if serializer.is_valid():
        device = serializer.validated_data['device']
        raspberry_pi_code = models.Device.objects.get(pk=1).raspberry_pi_code
        # raspberry_pi_code = 12345

        if device == raspberry_pi_code:

            lines = read_temp_raw()

            while lines[0].strip()[-3:] != 'YES':                   # ignore first line
                time.sleep(0.2)
                lines = read_temp_raw()
            equals_pos = lines[1].find('t=')                        # find temperature in the details

            if equals_pos != -1:
                temp_string = lines[1][equals_pos+2:]
                temp_c = float(temp_string) / 1000.0                 # convert to Celsius
                # temp_f = temp_c * 9.0 / 5.0 + 32.0                   # convert to Fahrenheit
                data = {
                    'device': raspberry_pi_code,
                    'temp': temp_c
                }

                return Response(data=data, status=status.HTTP_200_OK)

        else:
            return Response(status=status.HTTP_404_NOT_FOUND)

    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

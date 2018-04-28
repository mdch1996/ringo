from django.shortcuts import render, HttpResponse
from .forms import SwitchForm

import RPi.GPIO as GPIO
from .utils import take_pic

#thermomeer
import os                                                  # import os module
import glob                                                # import glob module
import time                                                # import time module
os.system('modprobe w1-gpio')                              # load one wire communication device kernel modules
os.system('modprobe w1-therm')
base_dir = '/sys/bus/w1/devices/'                          # point to the address
device_folder = glob.glob(base_dir + '28*')[0]             # find device with address starting from 28*
device_file = device_folder + '/w1_slave'                  # store the details


def led(request):
    # Pin Definitons:
    led_pin = 40

    # Pin Definitons:
    GPIO.setmode(GPIO.BOARD)  # programming the GPIO by BOARD pin numbers, GPIO21 is called as PIN40
    GPIO.setup(led_pin, GPIO.OUT)  # initialize digital pin40 as an output.

    # Initial state for LEDs:
    GPIO.output(led_pin, GPIO.LOW)

    if request.method == 'POST':
        switch_form = SwitchForm(data=request.POST)
        if switch_form.is_valid():
            cd = switch_form.cleaned_data
            switch = cd['switch']
            if switch > 0:
                GPIO.output(led_pin, GPIO.HIGH)  # turn the LED on (making the voltage level HIGH)
                take_pic()
            elif switch == 0:
                GPIO.cleanup()  # turn the LED off (making all the output pins LOW)
    else:
        switch_form = SwitchForm()

    return render(request, "base.html", {'switch_form': switch_form})


def read_temp_raw():
    f = open(device_file, 'r')
    lines = f.readlines()                                   # read the device details
    f.close()
    return lines


def read_temp(request):
    lines = read_temp_raw()

    while lines[0].strip()[-3:] != 'YES':                   # ignore first line
        time.sleep(0.2)
        lines = read_temp_raw()
    equals_pos = lines[1].find('t=')                        # find temperature in the details

    if equals_pos != -1:
        temp_string = lines[1][equals_pos+2:]
        temp_c = float(temp_string) / 1000.0                 # convert to Celsius
        # temp_f = temp_c * 9.0 / 5.0 + 32.0                   # convert to Fahrenheit
        return render(request, "temp.html", {'temp_c': temp_c})


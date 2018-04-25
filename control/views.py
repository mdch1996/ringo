from django.shortcuts import render, HttpResponse
from .forms import SwitchForm

import RPi.GPIO as GPIO
from .utils import take_pic


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


def camera(request):
    print('----device_ip-------')
    return HttpResponse("<html><body>It is now %s.</body></html>")



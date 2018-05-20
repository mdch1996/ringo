from requests import get, patch, post, exceptions
import RPi.GPIO as GPIO
from datetime import datetime
from . import models


# global variable
server_address = 'http://192.168.1.35:8000'
ip = ''

# GPIO for ring
GPIO.setmode(GPIO.BOARD)
GPIO.setup(36, GPIO.IN, pull_up_down=GPIO.PUD_UP)


def my_callback(channel):
    print("pushed")
    datetime_now = str(datetime.now())
    raspberry_pi_code = models.Device.objects.get(pk=1)
    # raspberry_pi_code = 12345

    data = {
        "date_of_ring": datetime_now,
        "raspberry_pi_code": raspberry_pi_code,
    }
    print("------send_ring------", data)
    send_ring(data)
    take_pic()


GPIO.add_event_detect(36, GPIO.RISING, callback=my_callback, bouncetime=400)


def check_ip():
    global ip
    new_ip = get_ip()
    if ip != new_ip:
        data = {
            "ip": str(new_ip),
            "raspberry_pi_code": 12345,
        }
        response = send_ip(data)
        if response == 204:
            ip = new_ip


def get_ip():
    url_get = "https://api.ipify.org/?format=json"
    try:
        r = get(url=url_get)
        data = r.json()
        new_ip = data['ip']
        return new_ip
    except exceptions.RequestException:
        pass


def send_ip(data):
    url_patch = server_address + "/api/ip/"
    try:
        r = patch(url=url_patch, data=data)
        return r.status_code
    except exceptions.RequestException:
        pass


def send_ring(data):
    url_post = server_address + "/api/ring/"
    try:
        r = post(url=url_post, data=data)
        return r.status_code
    except exceptions.RequestException:
        pass


def take_pic():
    import subprocess

    # subprocess.call("fswebcam -d /dev/video0 -r 1024x768 -S0 pic.jpg", shell=True)
    print('PIC CAPTURED')

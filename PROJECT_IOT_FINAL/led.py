import network
import machine
import ssd1306
import socket
import time
import urequests
import json
from machine import Pin,I2C,ADC,RTC
i2c = I2C(scl = Pin(5), sda=Pin(4), freq=100000)
oled = ssd1306.SSD1306_I2C(128, 32, i2c)
t = None
while True:
    r = urequests.get('http://ec2-52-201-213-2.compute-1.amazonaws.com:5000/led/')
    if json.loads(r.text)['result']!=t:
        t = json.loads(r.text)['result']
        oled.fill(0)
        oled.text(t,0, 10)
        oled.show()
        r.close()
    time.sleep(10)
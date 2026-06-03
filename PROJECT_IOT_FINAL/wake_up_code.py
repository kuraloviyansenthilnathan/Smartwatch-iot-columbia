import network
import machine
import ssd1306
import socket
import time
from machine import Pin,I2C,ADC,RTC
import urequests
import json

def do_connect():
    sta_if = network.WLAN(network.STA_IF)
    if not sta_if.isconnected():
        print('connecting to network...')
        sta_if.active(True)
        sta_if.connect('SpectrumSetup-99', 'futuretooth823')
        while not sta_if.isconnected():
            pass
    return sta_if.ifconfig()

i2c = I2C(scl = Pin(5), sda=Pin(4), freq=100000)

oled = ssd1306.SSD1306_I2C(128, 32, i2c)
ip_addr = do_connect()
print(ip_addr)

t = None
while True:
    r = urequests.get('http://ec2-75-101-212-225.compute-1.amazonaws.com:5000/led')
    # print(json.loads(r.text))
    t = json.loads(r.text)['result']
    oled.fill(0)
    oled.text(t,0, 10)
    oled.show()
    r.close()
    time.sleep(5)
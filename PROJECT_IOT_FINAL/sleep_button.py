import network
import machine
import ssd1306
import socket
import time
from machine import Pin,RTC
import urequests
import json
import dht

global state
global sleep_mode
sleep_mode = 0
state = 1
def handler(pin):
    global state
    global sleep_mode
    count = 0
    cur_value = pin.value()

    while count < 5:
        if pin.value() != cur_value:
            count = 0
        else:
            count += 1
        time.sleep_ms(5)

    if (sleep_mode == 0):    
        r = urequests.get('http://ec2-54-198-81-137.compute-1.amazonaws.com:5000/sleeping/sleep_start')
        print("start")
        sleep_mode = 1
    else:
        r = urequests.get('http://ec2-54-198-81-137.compute-1.amazonaws.com:5000/sleeping/sleep_end')
        print("stop")
        sleep_mode = 0
        
    time.sleep_ms(10)
    print('inside the handler callback function')
    state = 1 - state

def do_connect():
    sta_if = network.WLAN(network.STA_IF)
    if not sta_if.isconnected():
        print('connecting to network...')
        sta_if.active(True)
        sta_if.connect('Columbia University', '')
        while not sta_if.isconnected():
            pass
    return sta_if.ifconfig()
                
        
ip_addr = do_connect()
print(ip_addr)

def main():
    switch = Pin(12, Pin.IN, Pin.PULL_UP)
    sensor = dht.DHT11(Pin(2))
    pwm = machine.PWM(Pin(15))
    pwm.freq(70)

    switch.irq(trigger=Pin.IRQ_RISING, handler=handler)

    while True:

        if sleep_mode == 1:
            url = "http://ec2-54-198-81-137.compute-1.amazonaws.com:5000/value/temphumid"
            sensor.measure() 
            temp = sensor.temperature()
            humid = sensor.humidity() 
            data = {"temperature": temp,
            "humidity":humid}
            response = urequests.post(url, json=data)


if __name__ == '__main__':
    main()
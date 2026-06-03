import network
import machine
import ssd1306
import socket
import time
from machine import Pin,RTC
import urequests
import json
import ujson
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

    # while count < 5:
    #     if pin.value() != cur_value:
    #         count = 0
    #     else:
    #         count += 1
    #     time.sleep_ms(5)

    if (sleep_mode == 0):    
        r = urequests.get('http://ec2-3-93-173-70.compute-1.amazonaws.com:5000/sleeping/sleep_start')
        print("start")
        sleep_mode = 1
    else:
        z = urequests.get('http://ec2-3-93-173-70.compute-1.amazonaws.com:5000/sleeping/sleep_end')
        print("stop")
        sleep_mode = 0
        
    time.sleep_ms(1)
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
socket_addr = socket.getaddrinfo(str(ip_addr[0]), 80)[0][-1]
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind(socket_addr)
s.settimeout(1)
s.listen(1)

print('listening on', socket_addr)

switch = Pin(12, Pin.IN, Pin.PULL_UP)
sensor = dht.DHT11(Pin(2))
pwm = machine.PWM(Pin(15))
pwm.freq(70)

switch.irq(trigger=Pin.IRQ_RISING, handler=handler)

while True:

        if sleep_mode == 1:
            sensor.measure() 
            temp = str(sensor.temperature())
            humid = str(sensor.humidity())
            url = "http://ec2-3-93-173-70.compute-1.amazonaws.com:5000/value/temphumid?temp={}&humid={}".format(temp,humid)
            print(temp)
            response = urequests.get(url)
            response.close()
        time.sleep(1)   
            

# if __name__ == '__main__':
#     main()
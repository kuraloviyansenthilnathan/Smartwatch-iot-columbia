import urequests
import network
import json
import ssd1306
import machine
from machine import Pin,I2C

i2c = I2C(scl = Pin(5), sda=Pin(4), freq=100000)
oled = ssd1306.SSD1306_I2C(128, 32, i2c)

def connectnow():
    sta_if = network.WLAN(network.STA_IF)
    if not sta_if.isconnected():
        sta_if.active(True)
        sta_if.connect('Columbia University', '')
        while not sta_if.isconnected():
            pass
    return sta_if.config('mac')


def main():
    mac = connectnow()
    print(mac)

    myurl = 'http://ip-api.com/json'
    inf = urequests.get(myurl)
    mytext = json.loads(inf.text)

    lat = mytext['lat']
    lng = mytext['lon']

    while True:
        oled.fill(0)
        mylatitude = 'lat: ' + str(lat)
        mylongitude = 'lng: ' + str(lng)
        oled.text(mylatitude, 0, 0)
        oled.text(mylongitude, 0, 10)
        oled.show()
if __name__ == '__main__':
    main()



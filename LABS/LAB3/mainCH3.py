

import network
import urequests
import json
import machine
import ssd1306
from machine import Pin,I2C

#i2c = machine.I2C(-1, Pin(5), Pin(4))
i2c = I2C(scl = Pin(5), sda=Pin(4), freq=100000)
oled = ssd1306.SSD1306_I2C(128, 32, i2c)


def do_connect():
    sta_if = network.WLAN(network.STA_IF)
    if not sta_if.isconnected():
        print('connecting to network...')
        sta_if.active(True)
        sta_if.connect('Columbia University', '')
        while not sta_if.isconnected():
            pass
    return sta_if.config('mac')


def main():
    mac_address = do_connect()
    print(mac_address)

    # params = {
    #     "homeMobileCountryCode": 310,
    #     "homeMobileNetworkCode": 410,
    #     "radioType": "gsm",
    #     "carrier": "Vodafone",
    #     "considerIp": "true",
    #     "cellTowers": [
    #         {
    #             "cellId": 42,
    #             "locationAreaCode": 415,
    #             "mobileCountryCode": 310,
    #             "mobileNetworkCode": 410,
    #             "age": 0,
    #             "signalStrength": -60,
    #             "timingAdvance": 15
    #         }
    #     ],
    #     "wifiAccessPoints": [
    #         {
    #             "macAddress": mac_address,
    #             "signalStrength": -43,
    #             "age": 0,
    #             "channel": 11,
    #             "signalToNoiseRatio": 0
    #         }
    #     ]
    # }


    # geo_url = 'https://www.googleapis.com/geolocation/v1/geolocate?key=AIzaSyAUujOdE1VOAxpmlwg_nOung02sfdQjqk4  '
    # geo_inf = urequests.post(geo_url, data=json.dumps(params))
    # geo_text = json.loads(geo_inf.text)
    geo_url = 'http://ip-api.com/json'
    geo_inf = urequests.get(geo_url)
    geo_text = json.loads(geo_inf.text)


    # lat = geo_text['location']['lat']
    # lng = geo_text['location']['lng']



    lat = geo_text['lat']
    lng = geo_text['lon']
    weather_url = "http://api.openweathermap.org/data/2.5/weather?lat=%s&lon=%s&appid=c362508530960d518c2322739bfc85f4" % (lat, lng)
    #http://api.openweathermap.org/data/2.5/weather?lat=%s&lon=%s&appid=c362508530960d518c2322739bfc85f4
    #weather = json.loads(urequests.get(weather_url).text)
    weather = json.loads(urequests.get(weather_url).text)['weather'][0]['main']
    temp = json.loads(urequests.get(weather_url).text)['main']['temp']

    while True:
        oled.fill(0)
        lat_text = 'lat: ' + str(lat)
        lng_text = 'lng: ' + str(lng)
        oled.text(lat_text, 0, 0)
        oled.text(lng_text, 0, 10)
        # weather_text = 'weather: ' + weather
        oled.text(weather, 0, 20)
        oled.text(str(temp-273)+' C', 40, 20)
        oled.show()




   

if __name__ == '__main__':
    main()



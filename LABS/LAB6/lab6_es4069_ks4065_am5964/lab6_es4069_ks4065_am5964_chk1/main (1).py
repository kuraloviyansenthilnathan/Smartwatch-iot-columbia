from machine import Pin, RTC, I2C, ADC, PWM, SPI
import utime
import sys
import ssd1306
import ustruct
import network
import usocket
import urequests
import ujson

rtc = RTC()
# i2c = I2C(sda=Pin(4), scl=Pin(5), freq=200000)
# display = ssd1306.SSD1306_I2C(128, 32, i2c)
# display.poweron()
def do_connect():
    sta_if = network.WLAN(network.STA_IF)
    if not sta_if.isconnected():
        sta_if.active(True)
        sta_if.connect('Columbia University', '')
        while not sta_if.isconnected():
            pass
    return sta_if.config('mac')

hspi = SPI(1, baudrate=1000000, polarity=1, phase=1)
cs = Pin(2, Pin.OUT, value=1)

DEV = 0x00
reg_1 = 0x31
reg_2 = 0x2D
reg_3 = 0x2C
reg_4 = 0x2E
reg_5 = 0x38
reg_6 = 0x32

id = 0b11100101
g = 9.80665     
sensitivity = (1.0 / 256)

def write(hspi: SPI, cs: Pin, reg: int, val: int) -> None:

    msg = bytearray()
    msg.append(0b00000000 | reg)
    msg.append(val)
    cs.value(0)
    hspi.write(msg)
    cs.value(1)

def read(hspi: SPI, cs: Pin, reg: int, nbytes: int = 1) -> bytearray:

    Mega = None
    if nbytes < 1:
        return bytearray()
    elif nbytes == 1:
        Mega = 0
    else:
        Mega = 1

    msg = bytearray()
    msg.append(0b10000000 | (Mega << 6) | reg)

    cs.value(0)
    hspi.write(msg)
    val = hspi.read(nbytes)
    cs.value(1)

    return val

print(do_connect())
read(hspi, cs, DEV)

val = read(hspi, cs, DEV)
val = read(hspi, cs, reg_1)
val = int.from_bytes(val, "big") & ~(1 << 6)
write(hspi, cs, reg_1, val)

val = read(hspi, cs, reg_2)
val = int.from_bytes(val, "big") | (1 << 3)
write(hspi, cs, reg_2, val)
utime.sleep_ms(1000)
url = "http://ec2-54-91-139-193.compute-1.amazonaws.com:5000/post"

while True:
    val = read(hspi, cs, reg_6, 6)
    x = ustruct.unpack_from("<h", val, 0)[0]
    z = ustruct.unpack_from("<h", val, 4)[0]
    y = ustruct.unpack_from("<h", val, 2)[0]
    const = g * sensitivity
    x = x * const
    y = y * const
    z = z * const
    print(x,y,z)
    utime.sleep_ms(100)
    # display.fill(0)
    # display.text('{:02d}:{:02d}:{:02d}'.format(t[4],t[5],t[6]), x/255*100, y/255*100)
    # display.text('{:02d}:{:02d}:{:02d}'.format(t[1],t[2],t[3]), x/255*100, (y+20)*100/255)
    # display.show()
    # url = "http://ec2-54-91-139-193.compute-1.amazonaws.com:5000/post"
    # _, _, host, path = url.split('/', 3)
    # addr = usocket.getaddrinfo(host, 5000)[0][-1]

    # print("The %dth coordinates:")
    # s = usocket.socket()
    # s.connect(addr)
    # post_json = '{"xcoordinate":{} , "ycoordinate":{} ,  "zcoordinate":{}}'.format(str(x),str(y),str(z))
    post_data = ujson.dumps({'xcoordinate':  str(x),
    'ycoordinate': str(y),
    'zcoordinate': str(z)})
    # data_json = simplejson.dumps(data)
    # payload = {'json_payload': data_json}

    # post_json = '{"xcoordinate": "12" , "ycoordinate": "23",  "zcoordinate":"22"}'
    # post = 'POST /%s HTTP/1.1\r\nContent-length: %d\r\nContent-Type: application/json\r\nHost: %s\r\n\r\n%s' % \
    # (path, len(post_json), host, post_json)

    # s.send(str.encode(post))
    response = urequests.post(url, headers = {'content-type': 'application/json'},data=post_data)
    response.close()
    # print(response.text)
    # print(response.json())


import network
import machine
import ssd1306
import socket
import time
from machine import Pin,I2C

# i2c = machine.I2C(-1, Pin(5), Pin(4))
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
    return sta_if.ifconfig()

ip_addr = do_connect()
print(ip_addr)

socket_addr = socket.getaddrinfo(str(ip_addr[0]), 80)[0][-1]
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind(socket_addr)
s.listen(1)
print('listening on', socket_addr)

while True:
    cl, addr = s.accept()
    print('client connected from', addr)
    request = cl.recv(1024)
    request = str(request)
    print('content = %s' % request)

    if 'msg' in request:
        msg = request.split('/?msg=')[1].split('HTTP')[0]
        msg = msg.replace('%20', ' ')
        oled.fill(0)
        oled.text(msg, 0, 0)
        oled.show()

        resp_msg = 'well done'
        suc_response = "HTTP/1.1 200 OK\r\n\r\n%s" % resp_msg
        cl.send(str.encode(suc_response))

    else:
        fail_response = "HTTP/1.1 501 Implemented\r\n\r\nPlease attach msg!"
        cl.send(str.encode(fail_response))

    time.sleep(1)
    cl.close()



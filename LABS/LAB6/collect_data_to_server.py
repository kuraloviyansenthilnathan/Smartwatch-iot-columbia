import machine
from machine import Pin, RTC, I2C, ADC, PWM, SPI
import utime
import sys
import ssd1306
import network
import ustruct
import usocket
import ssl
rtc = RTC()
# i2c = I2C(sda=Pin(4), scl=Pin(5), freq=200000)
# display = ssd1306.SSD1306_I2C(128, 32, i2c)
# display.poweron()

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

read(hspi, cs, DEV)

val = read(hspi, cs, DEV)
val = read(hspi, cs, reg_1)
val = int.from_bytes(val, "big") & ~(1 << 6)
write(hspi, cs, reg_1, val)

val = read(hspi, cs, reg_2)
val = int.from_bytes(val, "big") | (1 << 3)
write(hspi, cs, reg_2, val)
utime.sleep_ms(1000)


def do_connect():
    sta_if = network.WLAN(network.STA_IF)
    if not sta_if.isconnected():
        sta_if.active(True)
        sta_if.connect('Columbia University', '')
        while not sta_if.isconnected():
            pass
    return sta_if.config('mac')


def get_pos():
    t = rtc.datetime()
    val = read(hspi, cs, reg_6, 6)
    x = ustruct.unpack_from("<h", val, 0)[0]
    z = ustruct.unpack_from("<h", val, 4)[0]
    y = ustruct.unpack_from("<h", val, 2)[0]
    const = g * sensitivity
    x = x * const
    y = y * const
    z = z * const
    print(x,y,z)
    return (x,y,z)

# def record(p):
#     # debounce
#     global record_state
#     irq_state = machine.disable_irq()
#     active = 0
#     while active < 20:
#         if p.value() == 0:
#             active += 1
#         else:
#             return
#         utime.sleep_ms(100)


#     if record_state == -1:
#         record_state = 1
#     else:
#         record_state = 1 - record_state

#     machine.enable_irq(irq_state)


# def write(register, value):
#     write_val = ustruct.pack('B', value)
#     write_reg_val = ustruct.pack('B', register)

#     cs.value(0)
#     spi.write(write_reg_val)
#     spi.write(write_val)
#     cs.value(1)


# def reallocate():
#     # free the memory
#     gc.collect()
#     gc.mem_free()
#     button_b.irq(trigger=Pin.IRQ_FALLING, handler=record)


def generate_clean_list(letters):
    if len(letters) < 20:
        return []
    else:
        new_list = []
        a = len(letters) // 20
        b = len(letters) % 20
        idx = 0
        for i in range(20):
            tempx = 0
            tempy = 0
            for j in range(a):
                tempx += letters[idx + j][0]
                tempy += letters[idx + j][1]
            tempx = tempx // a
            tempy = tempy // a
            new_list.append([tempx, tempy])
            idx += a
            if b > 0:
                idx += 1
                b -= 1
        return new_list


do_connect()
# data format
# write(0x31, 0x01)
# # power ctl
# write(0x2D, 0x08)
# button_b.irq(trigger=Pin.IRQ_FALLING, handler=record)

letter_list = []

while True:
    # if record_state == 1:
        x, y, z = get_pos()

        # url = "http://52.90.217.13/post"
        # _, _, host, path = url.split('/', 3)
        # addr = usocket.getaddrinfo(host, 8080)[0][-1]
        #
        # print(start)
        # s = usocket.socket()
        # s.connect(addr)
        # post_json = '{"xcoordinate": ' + str(x) + ', "ycoordinate": ' + str(y) + ', "zcoordinate": ' + str(start) + '}'
        # post = 'POST /%s HTTP/1.1\r\nContent-length: %d\r\nContent-Type: application/json\r\nHost: %s\r\n\r\n%s' % \
        #        (path, len(post_json), host, post_json)
        #
        # s.send(str.encode(post))
        # reallocate()
        letter_list.append([x, y,z])
        utime.sleep(0.05)

    # if record_state == 0:
        if len(letter_list) < 10:
            continue
        else:
            send_list = generate_clean_list(letter_list)

            # print("start sending message for team %d......" % team_no)
            for i in range(20):
                cx = send_list[i][0]
                cy = send_list[i][1]

                url = "http://ec2-3-89-119-154.compute-1.amazonaws.com:5000/post"
                _, _, host, path = url.split('/', 3)
                addr = usocket.getaddrinfo(host, 8080)[0][-1]

                print("The %dth coordinates:" % i)
                s = usocket.socket()
                s.connect(addr)
                post_json = '{"xcoordinate": ' + str(cx) + ', "ycoordinate": ' + str(cy) + ', "zcoordinate": '  + '}'
                post = 'POST /%s HTTP/1.1\r\nContent-length: %d\r\nContent-Type: application/json\r\nHost: %s\r\n\r\n%s' % \
                       (path, len(post_json), host, post_json)

                s.send(str.encode(post))
                print(cx, cy)
                # reallocate()
                utime.sleep(0.2)

            # record_state = -1
            letter_list = []

            # print("%dth team sent complete!" % team_no)
            # team_no += 1


import ssd1306
import time
import sys
import ustruct
import machine
from machine import Pin, RTC, I2C, SPI

i2c = I2C(scl = Pin(5), sda=Pin(4), freq=200000)
oled = ssd1306.SSD1306_I2C(128, 32, i2c)
spi = machine.SPI(1, baudrate=2000000, polarity=1, phase=1)
cs = machine.Pin(2, machine.Pin.OUT)
rtc = RTC()

def get_pos():
    cs.value(0)
    x2 = spi.read(5, 0x33)
    cs.value(1)

    cs.value(0)
    y2 = spi.read(5, 0x35)
    cs.value(1)

    print("%s, %s" % (x2[1], y2[1]))
    return [x2[1], y2[1]]


def main():
    # initialize the power of ADXL345
    power_ctl = b'\x2d\x08'
    data_format = b'\x31\x0f'
    cs.value(0)
    spi.write(power_ctl)
    cs.value(1)
    cs.value(0)
    spi.write(data_format)
    cs.value(1)

    # init position of the word in oled
    px, py = 50, 10
    while True:
        t = rtc.datetime()
        oled.fill(0)
        oled.text('{:02d}:{:02d}:{:02d}'.format(t[4],t[5],t[6]), px, py)
        oled.text('{:02d}:{:02d}:{:02d}'.format(t[1],t[2],t[3]), px, py+20)
        oled.show()

        avg_x = get_pos()[0]
        avg_y = get_pos()[1]
        print(get_pos()[0])
        print(get_pos()[1])

        if 0 < avg_x < 128:
            px += avg_x
        if avg_x > 128:
            px -= 256 - avg_x

        if 0 < avg_y < 128:
            py -= avg_y
        if avg_y > 128:
            py += 256 - avg_y

        if px >= 128:
            px = 0
        if px < 0:
            px = 128
        if py >= 32:
            py = 0
        if py < 0:
            py = 32

        time.sleep(0.001)


if __name__ == '__main__':
    main()

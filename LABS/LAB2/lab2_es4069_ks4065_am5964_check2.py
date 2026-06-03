import time
import machine
from machine import Pin


state = 1
def handler(pin):
    global state

    count = 0
    cur_value = pin.value()

    while count < 5:
        if pin.value() != cur_value:
            count = 0
        else:
            count += 1
        time.sleep_ms(5)
    print('inside the handler callback function')
    state = 1 - state


def main():
    switch = Pin(13, Pin.IN, Pin.PULL_UP)
    pwm = machine.PWM(Pin(15))
    pwm.freq(70)

    switch.irq(trigger=Pin.IRQ_RISING | Pin.IRQ_FALLING, handler=handler)

    while True:
        if state == 1:
            pwm.duty(1023)
        else:
            pwm.duty(0)


if __name__ == '__main__':
    main()
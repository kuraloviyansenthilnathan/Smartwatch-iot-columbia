import time
import machine
from machine import Pin,ADC,PWM


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

    pwm0 = PWM(Pin(15), freq=1000, duty=512)
    pwm1 = PWM(Pin(14), freq=1000, duty=512)
    adc0 = ADC(0)

    switch.irq(trigger=Pin.IRQ_RISING | Pin.IRQ_FALLING, handler=handler)

    while True:
        if state == 1:
            pwm1.freq(0)
            pwm0.duty(0)
        else:
            pwm0.duty(adc0.read())
            pwm1.freq(adc0.read())

if __name__ == '__main__':
    main()
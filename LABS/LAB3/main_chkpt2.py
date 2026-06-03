from machine import Pin, I2C, RTC,ADC

import ssd1306
import ntptime
import time

i2c = I2C(scl = Pin(5), sda=Pin(4), freq=100000)
display = ssd1306.SSD1306_I2C(128,32,i2c)

rtc = RTC()
#rtc.datetime((2022,9,28,3,16,4,0,0))
global t
t = list(rtc.datetime())
#ntptime.settime()

state = 1
toggle = 0
def handler_A(pin):
    global t

    if toggle == 0:
        curr_value = t[4]
        if curr_value<23:
            curr_value+=1
        else:
            curr_value = 0
        t[4] = curr_value
        # rtc.datetime((t[0],t[1],t[2]),t[3],curr_value,t[5],t[6],t[7])

    
    elif toggle == 1:
        curr_value = t[5]
        if curr_value<59:
            curr_value+=1
        else:
            curr_value = 0
        t[5] = curr_value
        # rtc.datetime((t[0],t[1],t[2]),t[3],t[4],curr_value,t[6],t[7])

    else:
        curr_value = t[6]
        if curr_value<59:
            curr_value+=1
        else:
            curr_value = 0
        t[6] = curr_value
        # rtc.datetime((t[0],t[1],t[2]),t[3],t[4],t[5],curr_value,t[7])
    state = 1- state

def handler_B(pin):
    global t
    if toggle == 0:
        curr_value = t[4]
        if curr_value>=1:
            curr_value-=1
        else:
            curr_value = 23
        t[4] = curr_value

    elif toggle == 1:
        curr_value = t[5]
        if curr_value>=1:
            curr_value-=1
        else:
            curr_value = 59
        t[5] = curr_value
    else:
        curr_value = t[6]
        if curr_value>=1:
            curr_value-=1
        else:
            curr_value = 59
        t[6] = curr_value
    state = 1- state

def handler_C(pin):
    global toggle
    if toggle <=1:
        toggle+=1
    else:
        toggle = 0
    print(toggle)
    state = 1- state



def main():
    A = Pin(12, Pin.IN, Pin.PULL_UP)
    B = Pin(13, Pin.IN, Pin.PULL_UP)
    C = Pin(14, Pin.IN, Pin.PULL_UP)
    A.irq(trigger=Pin.IRQ_RISING , handler= handler_A)
    B.irq(trigger=Pin.IRQ_RISING , handler= handler_B)
    C.irq(trigger=Pin.IRQ_RISING , handler= handler_C)
    display.poweron()
    adc0 = ADC(0)

    while True:
        # t = rtc.datetime()
        if state ==1:
            if t[6]<59:
                t[6]+=1
                time.sleep(1)
            else:
                t[6] = 0
                if t[5]<59:
                    t[5]+=1
                    time.sleep(1)
                else:
                    t[5]=0
                    if t[4]<23:
                        t[4]+=1
                        time.sleep(1)
                    else:
                        t[4]= 0
                        time.sleep(1)
            display.fill(0)
            display.contrast(adc0.read()*2)
            display.text('{:02d}:{:02d}:{:02d}'.format(t[4],t[5],t[6]),0,0,10)
            #display.text('{:02d}-{:02d}-{:02d}'.format(t[0],t[1],t[2]),2,0,10)
            # print(t)
            display.show()


        else:

            display.fill(0)
            display.contrast(adc0.read()*2)
            display.text('{:02d}:{:02d}:{:02d}'.format(t[4],t[5],t[6]),0,0,10)
            #display.text('{:02d}-{:02d}-{:02d}'.format(t[0],t[1],t[2]),2,0,10)
            # print(t)
            display.show()


if __name__ == '__main__':
    main()
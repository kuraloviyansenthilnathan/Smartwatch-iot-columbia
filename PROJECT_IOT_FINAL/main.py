import network
import machine
import ssd1306
import socket
import time
from machine import Pin,I2C,ADC,RTC
import urequests
import json
i2c = I2C(scl = Pin(5), sda=Pin(4), freq=100000)
oled = ssd1306.SSD1306_I2C(128, 32, i2c)
rtc = machine.RTC()
rtc.datetime((2022, 12, 11, 0, 3, 20, 0, 0))
alarm_time = [58,21,3]
adc0 = ADC(0)
pwm = machine.PWM(machine.Pin(15))
cur = 0
mode = 0
pos = [6, 5, 4, 2, 1, 0]
pos_name = ["second", "minute", "hour", "day", "month", "year"]

def display_time():
    # global adc0
    oled.fill(0)
    cur_date = "date: " + str(rtc.datetime()[0]) + '/' + str(rtc.datetime()[1]) + '/' + str(rtc.datetime()[2])
    cur_time = "time: " + str(rtc.datetime()[4]) + ':' + str(rtc.datetime()[5]) + ':' + str(rtc.datetime()[6])
    alarm = "alarm: " + str(alarm_time[2]) + ':' + str(alarm_time[1]) + ':' + str(alarm_time[0])
    # oled.contrast(adc0.read()*5)
    oled.text(cur_date, 0, 0)
    oled.text(cur_time, 0, 10)
    oled.text(alarm, 0, 20)
    oled.show()


# change which pos do you want to change
def change_pos(p):
    global cur, pos_name, mode
    # debounce
    irq_state = machine.disable_irq()
    active = 0
    while active < 20:
        if p.value() == 0:
            active += 1
        else:
            return
        time.sleep_ms(1)

    if mode == 0:
        oled.fill(0)
        cur = (cur + 1) % 6
        oled.text(pos_name[cur], 0, 0)
        oled.show()
    elif mode == 1:
        oled.fill(0)
        cur = (cur + 1) % 3
        oled.text(pos_name[cur], 0, 0)
        oled.show()

    machine.enable_irq(irq_state)


# plus 1 on the position
def acc_time(p):
    global cur, rtc, mode, alarm_time
    # debounce
    irq_state = machine.disable_irq()
    active = 0
    while active < 20:
        if p.value() == 0:
            active += 1
        else:
            return
        time.sleep_ms(1)

    if mode == 0:
        cur_datetime = list(rtc.datetime())
        cur_datetime[pos[cur]] += 1
        rtc.datetime(tuple(cur_datetime))
    elif mode == 1:
        if cur==2:
            if alarm_time[cur]>=23:
                alarm_time[cur] = 0
            else:
                alarm_time[cur]+=1
        else:
            if alarm_time[cur]>=59:
                alarm_time[cur] = 0
            else:
                alarm_time[cur]+=1
    oled.fill(0)
    cur_date = "date: " + str(rtc.datetime()[0]) + '/' + str(rtc.datetime()[1]) + '/' + str(rtc.datetime()[2])
    cur_time = "time: " + str(rtc.datetime()[4]) + ':' + str(rtc.datetime()[5]) + ':' + str(rtc.datetime()[6])
    alarm = "alarm: " + str(alarm_time[2]) + ':' + str(alarm_time[1]) + ':' + str(alarm_time[0])
    oled.text(cur_date, 0, 0)
    oled.text(cur_time, 0, 10)
    oled.text(alarm, 0, 20)
    oled.show()

    machine.enable_irq(irq_state)


# change to alarm or time
def change_mode(p):
    global mode
    # debounce
    irq_state = machine.disable_irq()
    active = 0
    while active < 20:
        if p.value() == 0:
            active += 1
        else:
            return
        time.sleep_ms(1)

    mode = 1 - mode
    print(mode)
    mode_name = ['normal', 'alarm']
    oled.fill(0)
    oled.text(mode_name[mode], 0, 0)
    oled.show()

    machine.enable_irq(irq_state)


# blink the led and start piezo as an alarm
def blink(p):
    p.freq(1000)
    for i in range(10):
        for j in range(1000):
            p.duty(j)
            time.sleep(0.001)
        display_time()
        for j in range(1000, -1, -1):
            p.duty(j)
            time.sleep(0.001)
        display_time()


def do_connect():
    sta_if = network.WLAN(network.STA_IF)
    if not sta_if.isconnected():
        print('connecting to network...')
        sta_if.active(True)
        sta_if.connect('SpectrumSetup-99', 'futuretooth823')
        while not sta_if.isconnected():
            pass
    return sta_if.ifconfig()

def show_time():
    oled.fill(0)
    cur_date = "date: " + str(rtc.datetime()[0]) + '/' + str(rtc.datetime()[1]) + '/' + str(rtc.datetime()[2])
    cur_time = "time: " + str(rtc.datetime()[4]) + ':' + str(rtc.datetime()[5]) + ':' + str(rtc.datetime()[6])
    oled.text(cur_date, 0, 0)
    oled.text(cur_time, 0, 10)
    oled.show()
def check(request):
            msg = request.split('/?msg=')[1].split('HTTP')[0]
            msg = msg.replace('%20', ' ')
            oled.fill(0) 
            print('start')
            print(msg)
            print('end')
            # if '100' in msg:
            #     return True
            # return False
            
            r = urequests.get('http://ec2-75-101-212-225.compute-1.amazonaws.com:5000/send?val='+msg)
            print(json.loads(r.text))
            return json.loads(r.text)['result']
                
        
ip_addr = do_connect()
print(ip_addr)
socket_addr = socket.getaddrinfo(str(ip_addr[0]), 80)[0][-1]
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind(socket_addr)
s.settimeout(1)
s.listen(1)

print('listening on', socket_addr)


myurl = 'http://ip-api.com/json'
inf = urequests.get(myurl)
mytext = json.loads(inf.text)

lat = mytext['lat']
lng = mytext['lon']

wurl = "http://api.openweathermap.org/data/2.5/weather?lat=%s&lon=%s&appid=c362508530960d518c2322739bfc85f4" % (lat, lng)

weather = json.loads(urequests.get(wurl).text)['weather'][0]['main']
temp = json.loads(urequests.get(wurl).text)['main']['temp']

turl = "https://api.tomtom.com/traffic/services/4/flowSegmentData/relative0/10/json?point=52.41072%2C4.84239&unit=KMPH&openLr=false&key=CNFAmvQvr4FEJHNdajFiBYJIqavlUmKA"

#i_nf = urequests.get(turl)
#my_text = json.loads(i_nf.text)

#road_traffic_status = my_text['flowSegmentData']['roadClosure']


button_a = Pin(12, Pin.IN, Pin.PULL_UP)
button_b = Pin(13, Pin.IN, Pin.PULL_UP)
button_c = Pin(14, Pin.IN, Pin.PULL_UP)

button_a.irq(trigger=Pin.IRQ_FALLING, handler=change_mode)
button_b.irq(trigger=Pin.IRQ_FALLING, handler=change_pos)
button_c.irq(trigger=Pin.IRQ_FALLING, handler=acc_time)
flag = False
alarm_set = True
weather_check = False
counter = 0
while True:
        if alarm_set and not weather_check:
            if  'Snow' in weather:
                alarm_time[2]-=1
            if 'Tornado' in weather:
                alarm_time[2]-=2

            if 'Fog' in weather:
                alarm_time[2]-=1
            
            if  'Rain' in weather :
                alarm_time[2]-=1
            if 'Thunderstorm' in weather:
                alarm_time[2]-=2
            if  'Clear' in weather:
                alarm_time[2]-=2
   #         if  'true' in road_traffic_status:
   #             alarm_time[2]-=2
            alarm_set = False
            weather_check = True


        if alarm_time[2]<0:
               alarm_time[2]= 12+ alarm_time[2]
        clients = []
        # if rtc.datetime()[4] == alarm_time[2] and rtc.datetime()[5] == alarm_time[1] and rtc.datetime()[6] == alarm_time[0]:
        #          blink(pwm)
        if rtc.datetime()[4] == alarm_time[2] and rtc.datetime()[5] == alarm_time[1] and (rtc.datetime()[6] == alarm_time[0] or rtc.datetime()[6] == alarm_time[0]+1):
                    flag = True
        display_time()
        if flag == True:
            blink(pwm)
            counter+=1
            if counter>=15:
                r = urequests.get('http://ec2-75-101-212-225.compute-1.amazonaws.com:5000/not_woken')
                r.close()
                print(counter)
        try:
            cl, addr = s.accept()
            print('client connected from', addr)      
            clients.append(cl)
        except:
            pass
        try:
                request = cl.recv(1024)
                request = str(request)
                print('content = %s' % request)
                if 'msg' in request:
                    r =  check(request)
                    print(r)
                    if r==True:
                        r = urequests.get('http://ec2-75-101-212-225.compute-1.amazonaws.com:5000/generate')
                        flag = False
                        counter = 0
                    suc_response = "HTTP/1.1 200 OK\r\n\r\n%s" % r
                    r.close()
                    cl.send(str.encode(suc_response))

                else:
                    fail_response = "HTTP/1.1 501 Implemented\r\n\r\nPlease attach msg!"
                    cl.send(str.encode(fail_response))
                cl.close()
        except:
                pass
        time.sleep(0.1)        

# if __name__ == '__main__':
#     main()


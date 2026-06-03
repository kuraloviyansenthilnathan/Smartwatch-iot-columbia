from machine import Pin, PWM, ADC
import utime
# builtin_led = Pin(0, Pin.OUT)
# antenna_led = Pin(2, Pin.OUT)
# builtin_led.value(1) # Built in LED - 1 is off
# antenna_led.value(0) # Antenna LED - 0 is on

pwm0 = PWM(Pin(15), freq=1000, duty=512)
pwm1 = PWM(Pin(13), freq=1000, duty=512)

#pwm0.freq(1000)
#pwm1.duty(512)

adc0 = ADC(0)



while True:
	# builtin_led.value(not builtin_led.value())
	# antenna_led.value(not antenna_led.value())
	# utime.sleep(1)print(intadc0.read())
	pwm0.duty(adc0.read())
	pwm1.freq(adc0.read())
	print("4")
	utime.sleep(0.05)

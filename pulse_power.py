#!/usr/bin/env python

# NAME: Compute power from pulses (time based)
# DESCRIPTION: Power is computed from the exact time between pulses. Basic version, no filter
import time
from drbox import sdb, mainloop, gpio

GPIO_PATH = '/sys/class/gpio/gpio42'
PULSE_WEIGHT = 1 # Wh / pulse
PERIOD = 15  # report a value when at least N seconds elapsed between pulses

start_date = time.time()
last_date = time.time()
pulse_count = None

usleep = lambda x: time.sleep(x/1000000.0)

def now_ts():
    return time.time()

def main():
    c = sdb.Client('pulse_counter')
    c.connect()

    tag_pulse_power = c.add_tag('PULSE_POWER', sdb.DT_DINT, 1)
    tag_top_15s = c.add_tag('TOP_15_SEC', sdb.DT_BOOL, 1)

    gpio_pulse = gpio.GPIO(GPIO_PATH)
    global pulse_count, start_date
    pulse_count = 0
    
    def on_top_15s(tag, user_data):
        if tag.read():
            global start_date, pulse_count, last_date
            delta_t = last_date - start_date
            power = round((pulse_count-1) * PULSE_WEIGHT * 3600.0 / delta_t)
            if power < 0:  # Error maybe no pulse detected
                power = 0

            tag_pulse_power.write(power)
 
            # start a new cycle
            pulse_count = 0
    
    def on_gpio_change(gpio, value, data):
        
        if not value:
            # react on rising edge only, not all GPIO's support the edge parameter
            return
        else:
            # let's sleep before testing the GPIO level again to debounce the pulses
            usleep(300);
            value = gpio_pulse.read()
            if (value == 0):
                #print("[DEBUG] Bad detect 1\n")
                return
            usleep(300);
            value = gpio_pulse.read()
            if (value == 0):
                #print("[DEBUG] Bad detect 2\n")
                return
            usleep(300)
            value = gpio_pulse.read()
            if (value == 0):
                print("[DEBUG] Bad detect 3\n")
                return
            usleep(300);
            value = gpio_pulse.read()
            if (value == 0): 
                print("[DEBUG] Bad detect 4\n")
                return
        
        global pulse_count, start_date, last_date
        
        if pulse_count == 0:
            start_date = now_ts()
        
        pulse_count += 1
        last_date = now_ts()
    
    tag_top_15s.on_event(on_top_15s)
    loop = mainloop.Mainloop()
    c.register_on_mainloop(loop)
    gpio_pulse.register_on_mainloop(loop)

    gpio_pulse.on_change(on_gpio_change)

    loop.run()


if __name__ == '__main__':
    main()
#!/usr/bin/env python
import json

import time
from drbox import sdb, mainloop

prev_base = None
prev_base_date = None

THRESHOLD_LOW = 100
THRESHOLD_ZERO = 0


def now_ts():
    return time.time()

def write_instant_power(tag, value):
    print("instant power: " + str(value))
    tag.write(value)


def main():
    c = sdb.Client('tic_instant_power')
    c.connect()

    tic_base = c.get_tag_by_name('TIC_BASE')
    tic_instant_power = c.add_tag('TIC_INSTANT_POWER', sdb.DT_DINT, 1)

    def on_tag_change(tag, user_data):
        global prev_base, prev_base_date, current_ps
        t = now_ts()
        base = tic_base.read()
        if prev_base is None:
            prev_base = base
            prev_base_date = t
        else:
            pe = 0
            min_delay = 8  # do not report a data faster than this delay to increase accuracy with high power
            if base > prev_base and (t - prev_base_date) > min_delay:
                pe += (base - prev_base) * 3600.0 / (t - prev_base_date)
                prev_base = base
                prev_base_date = t

            if pe > 0:
                write_instant_power(tic_instant_power, pe)

    tic_base.on_event(on_tag_change)

    loop = mainloop.Mainloop()
    c.register_on_mainloop(loop)

    prev_msg_date = now_ts()
    threshold_time = 3600 / THRESHOLD_LOW
    while True:
        loop.run(1*mainloop.SECOND)
        if prev_base_date is not None:
            t = now_ts()
            if t - prev_msg_date > 5:
                delta_t = t - prev_base_date
                if delta_t > threshold_time:
                    pe = 3600/delta_t
                    if pe < THRESHOLD_ZERO:
                        pe = 0
                    write_instant_power(tic_instant_power, pe)
                    prev_msg_date = t


if __name__ == '__main__':
    main()
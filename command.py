#!/usr/bin/python

import linuxcnc
import hal
import time

s = linuxcnc.stat()
c = linuxcnc.command()

def ok_for_mdi():
    s.poll()
    return not s.estop and s.enabled and s.homed and (s.interp_state == linuxcnc.INTERP_IDLE)

if ok_for_mdi():
   c.mode(linuxcnc.MODE_MDI)
   c.wait_complete() # wait until mode switch executed
   c.mdi("G0 X1 Y2 Z1")




# h = hal.component("passthrough")
# h.newpin("in", hal.HAL_FLOAT, hal.HAL_IN)
# h.newpin("out", hal.HAL_FLOAT, hal.HAL_OUT)
# h.ready()

# try:
#     while 1:
#         time.sleep(1)
#         h['out'] = h['in']
# except KeyboardInterrupt:
#     raise SystemExit
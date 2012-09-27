#!/usr/bin/python

import sys
#import linuxcnc
import emc

#----------
# try:
#     s = linuxcnc.stat() # create a connection to the status channel
#     s.poll() # get current values
# except linuxcnc.error, detail:
#     print "error", detail
#     sys.exit(1)
# for x in dir(s):
#     if not x.startswith('_'):
#         print x, getattr(s,x)

# import linuxcnc

#----------
# s = linuxcnc.stat()
# c = linuxcnc.command()
s = emc.stat()
c = emc.command()


# def ok_for_mdi():
# 	s.poll()
# 	return s.estop and s.enabled and s.homed and (s.interp_state == linuxcnc.INTERP_IDLE)

s.poll()
print "estop", s.estop
print  "enabled", s.enabled
print "homed", s.homed
print "state idle?", (s.interp_state == emc.INTERP_IDLE)
print "interpreter state", s.interp_state
print "exec state", s.exec_state

# if ok_for_mdi():
# s.poll()
c.mode(emc.MODE_MDI)
c.wait_complete(2.0) # wait until mode switch executed
c.mdi("G1 X10 Y20 Z30 F250")
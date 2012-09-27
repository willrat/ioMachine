#!/usr/bin/python

import emc
import hal
import time
import os
import threading



# class MachineTimer(threading.Timer):
# 	timeOut = False
# 	def __init__(self, *args, **kw):
# 		super( MachineTimer, self ).__init__(*args, **kw)
#         timeOut = False

# 	def complete():
# 		timeOut = True

# class EF:
# 	def __init__(self):


class MachineTimer():

	timeOut = False

	def __init__(self):
		self.timer = threading.Timer(1, self.complete)
		self.timer.start()
        timeOut = False
        print "Timer started"

	def complete(self):
		self.timeOut = True


class StateMachine():

	def __init__(self):
		self.currentState = 1
		self.entry = True
		self.timer1 = MachineTimer()
		self.timer2 = MachineTimer()

	# change the state of the machine
	def newState(self, stateNumber):
		# global entry, currentState
		self.entry = True;
		self.currentState = stateNumber

	# def readyTimeOut(self):
	# 	self.timeoutComplete = True

	def standby(self):
		#global entry, timer2
		
		if self.entry:
			print "standby entry"
			print ("%.6f" % time.time())
			self.timer2 = MachineTimer()
			# timer2.start()
			self.entry = False
			h['hydraulicMotorContactor'] = 0

		if self.timer2.timeOut:
			self.newState(1)

		# this is a hack to go from standby to cycle
		if h['startButton']:
			self.newState(3)

	def ready(self):
		
		if self.entry:
			print "ready entry"
			# print ("%.6f" % time.time())
			self.timer1 = MachineTimer()
			# timer1.start()
			self.entry = False
			#h['hydraulicMotorContactor'] = 1
			# print ("Prehome 0 %.6f" % time.time())
			# command.home(0)
			# print ("Prehome 1 %.6f" % time.time())
			# command.home(1)
			# print ("Prehome 2 %.6f" % time.time())
			# command.home(2)
		
		# timeout goto cycle
		if self.timer1.timeOut:
			self.newState(4)

		# if h['FootPedal']:
		# 	self.newState(4)



	def closeVice(self):
		if self.entry:
			h['hydraulicMotorContactor'] = 1
			self.entry = False			
			print "closeVice Entry"
			h['dumpValve'] = 1

		# the vice sas close
		if h['viceSafetyRelay']:
			self.newState(4)


	def cycle(self):
		# global status
		# global command

		if self.entry:
			print "cycle entry"
			self.entry = False
			# command.mode(emc.MODE_AUTO)
			command.mode(emc.MODE_MDI)
			#command.wait_complete()

			
		status.poll()

    	# if (not status.estop) and status.enabled and status.homed and (status.interp_state == emc.INTERP_IDLE):
    	# if status.interp_state == emc.INTERP_IDLE:
		# if status.interp_state == emc.INTERP_IDLE:
		# 	print "status idle"
		# if status.homed:
		# 	print "status homed"
		# if status.enabled:
		# 	print "status enabled"
		# if status.estop:
		# 	print "estop"


		if (status.task_mode == emc.MODE_MDI and status.interp_state == emc.INTERP_IDLE):
			# print ("time A %.6f" % time.time())
			print "task mode is MODE_MDI, issuing command"
			# print ("time B %.6f" % time.time())
			
			mdiCommand = "G0X10"
			command.mdi(mdiCommand)
			print ("time C %.6f" % time.time())
		else:
			print "Not in MDI Mode"
		

	# statenames = {	"READY",
	# 				"STANDBY",
	# 				CLOSEVICE, 
	# 				CYCLE
	# }

	statenames = [	"READY",
					"STANDBY",
					"CLOSEVICE", 
					"CYCLE" ]
	

	# dict of state functions
	states = {	1 : ready,
				2 : standby,
				3 : closeVice,
				4 : cycle
	}

	def run(self):
		# print self.statenames[self.currentState]
		self.states[self.currentState](self)

# res = os.spawnvp(os.P_WAIT, "halcmd", ["halcmd", "-i", vars.emcini.get(), "-f", postgui_halfile])
# connect the new pins to the system
# processid = os.spawnvp(os.P_WAIT, "halcmd", ["halcmd", "-f", "post.hal"])
# if processid:
# 	raise SystemExit, processid
h = hal.component("machine")

#inputs
h.newpin("mcb1", hal.HAL_BIT, hal.HAL_IN)
h.newpin("mcb2", hal.HAL_BIT, hal.HAL_IN)
h.newpin("mcb3", hal.HAL_BIT, hal.HAL_IN)

startButton = h.newpin("hydraulicStartPB", hal.HAL_BIT, hal.HAL_IN)
stopButton = h.newpin("hydraulicStopPB", hal.HAL_BIT, hal.HAL_IN)

h.newpin("viceSafetyRelay", hal.HAL_BIT, hal.HAL_IN)
h.newpin("eStopRelay", hal.HAL_BIT, hal.HAL_IN)
h.newpin("2HandControlRelay", hal.HAL_BIT, hal.HAL_IN)
h.newpin("FootPedal", hal.HAL_BIT, hal.HAL_IN)

#outputs
h.newpin("viceOpenValve", hal.HAL_BIT, hal.HAL_OUT)
h.newpin("viceCloseValve", hal.HAL_BIT, hal.HAL_OUT)
h.newpin("dumpValve", hal.HAL_BIT, hal.HAL_OUT)
h.newpin("hydraulicMotorContactor", hal.HAL_BIT, hal.HAL_OUT)

h.ready()

status = emc.stat()
command = emc.command()

# def ok_for_mdi():
#     s.poll()
#     return not s.estop and s.enabled and s.homed and (s.interp_state == emc.INTERP_IDLE)

# if ok_for_mdi():
#    c.mode(emc.MODE_MDI)
#    c.wait_complete() # wait until mode switch executed
#    c.mdi("G0 X10 Y20 Z30")


machine = StateMachine()

# def ok_for_mdi():
# 	s.poll()
# 	return not s.estop and s.enabled and s.homed and (s.interp_state == emc.INTERP_IDLE)


while 1:
	#print "machine current state" + machine.currentState
	machine.run()

	# if machine.currentState == 3:
	# 	if ok_for_mdi():
	# 		print "ok for mdi"
	# 		command.mode(emc.MODE_MDI)
	# 		command.wait_complete() # wait until mode switch executed
	# 		command.mdi("G0 X10 Y20 Z30")


	# if h['hydraulicStartPB']:
	# 	h['hydraulicMotorContactor'] = 1

	# if h['2HandControlRelay'] or h['FootPedal']:
	# 	#start cycle
	# 	h['viceCloseValve'] = 1




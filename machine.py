#!/usr/bin/python

import emc
import hal
import time
import os
import threading

import gui1
import gtk

hmi = gui1.hmi

# class MachineTimer(threading.Timer):
# 	timeOut = False
# 	def __init__(self, *args, **kw):
# 		super( MachineTimer, self ).__init__(*args, **kw)
#         timeOut = False

# 	def complete():
# 		timeOut = True

# class EF:
# 	def __init__(self):


# class MachineTimer():

# 	timeOut = False

# 	def __init__(self, period):
# 		self.period = period
# 		self.start()

# 	def start(self):
# 		self.timer = threading.Timer(self.period, self.complete)
# 		self.timer.start()
# 		self.startTime = time.time()
# 		self.timeOut = False
# 		print "Timer started for %s seconds" % self.period

# 	def complete(self):
# 		self.timeOut = True
# 		self.completionTime = time.time()
# 		#print "Timer comleted in %s" % time.time() - self.startTime

# 	def renew(self):
# 		self.timer.cancel()
# 		self.start()

# 	def reset(self, period=None):
# 		if period:
# 			self.period = period
# 		self.renew()


class MachineTimer(threading.Thread):

	def __init__(self, period=1000, running=True):
		threading.Thread.__init__(self)
		self.period = period
		#self.timeOut = False
		self.reset()
		self.running = running
		#self.start()

	#def start(self):
	# def whatWasStart(self):
	# 	self.timer = threading.Timer(self.period, self.complete)
	# 	self.timer.start()
	# 	self.startTime = time.time()
	# 	self.timeOut = False
	# 	print "Timer started for %s seconds" % self.period

	def setRunning(self, running):
		# timer pause
		#if not running and self.running:
		# resume timer
		#if running and not self.running:
		self.running = running

	# def complete(self):
	# 	self.timeOut = True
	# 	self.completionTime = time.time()
	# 	#print "Timer comleted in %s" % time.time() - self.startTime

	# def renew(self):
	# 	self.timer.cancel()
	# 	self.start()
	def renew(self):
		self.reset()

	def reset(self, period=None):
		if period:
			self.period = period
		
		self.startTime = time.time()
		self.timeOut = False
		self.running = True

		print "Timer started for %s seconds" % self.period

	def run(self):
		try:
			while 1:			
				if self.running and not self.timeOut:
					currentTime = time.time()
					self.elapsed = currentTime - self.startTime
					self.remaining = self.period - self.elapsed
					#print "time remaining %s" % self.remaining
					if self.remaining <= 0.0: self.timeOut = True
				#else:
		except KeyboardInterrupt:
			raise SystemExit


class StateMachine(threading.Thread):

	# change the state of the machine
	def newState(self, stateName):
		# global entry, currentState
		self.entry = True;
		self.currentState = stateName
		print "Chaning state to %s" % stateName

	def getState(self):
		return self.currentState

	def requestState(self, state):
		print "requestState"

	# machine state methods
	def standby(self):
		#global entry, timer2
		
		if self.entry:
			#print "standby entry"
			#print ("%.6f" % time.time())
			#self.timer2.reset()
			# timer2.start()
			self.entry = False
			h['hydraulicMotor'] = 0
			h['dumpValve'] = 0
			self.setViceInactive()

		# if self.timer2.timeOut:
		# 	#self.newState(1)
		# 	self.newState("READY")

		if h['startButton']:
			#h['hydraulicMotor'] = 
			self.newState("READY")


		# this is a hack to go from standby to cycle
		# if h['startButton']:
		# 	#self.newState(3)
		# 	self.newState("CLOSEVICE")

	def ready(self):
		
		if self.entry:
			#print "ready entry"
			# print ("%.6f" % time.time())
			self.standbyTimer.reset()
			# standbyTimer.start()
			self.entry = False
			h['hydraulicMotor'] = 1
			
			# need to drive motion.enable to true
			if command:
				command.state(emc.STATE_ON)
		
		# timeout goto cycle
		# if self.standbyTimer.timeOut:
		# 	self.newState(4)

		if h['stopButton']:
			self.newState("STANDBY")

		#if h['footPedal'] or h['startButton']:
		if h['footPedal']:
			self.newState("CLOSEVICE")

		if h['requestManual']:
			self.newState("MANUAL")

	def manual(self):
		if self.entry:
			print "Manual mode"
			if command:
				command.mode(emc.MODE_MANUAL)
		

	def closeVice(self):
		if self.entry:
			#h['hydraulicMotor'] = 1
			self.entry = False			
			#print "closeVice Entry"
			
			# for testing
			#h['dumpValve'] = 1

		#if h['2HandControlRelay']:
		if h['footPedal']:
			h['dumpValve'] = 1
			#h['viceCloseValve'] = 1
			self.setViceClose()
		else:
			h['dumpValve'] = 0
			self.setViceInactive()


		# else:
		# 	h['dumpValve'] = 0
		# 	h['viceCloseValve'] = 0

		# the vice has closed
		if h['viceSafetyRelay']:
			self.newState("STARTSPINDLE")

	def startSpindle(self):
		print "startSpindle"
		if self.entry:
			h['spindle'] = 1
			h['spindleSpeed'] = 1.0			
			self.spindleStartUptimer.reset(0.2)
			self.entry = False
		
		if self.spindleStartUptimer:
			self.newState("CYCLE")

	# def readyForNextMove(self):
	# 	if status.task_mode == emc.MODE_MDI \
	# 	and status.interp_state == emc.INTERP_IDLE \
	# 	and self.moveCounter != len(commands):
	# 		if status.inpos or status.delay_left > 0.0:
	# 			return True

	# 	return False

	def cycle(self):
		# global status
		# global command

		if self.entry:
			print "cycle entry"
			self.entry = False			
			command.mode(emc.MODE_MDI)
			self.moveCounter = 0
			#self.slowDownTimer = MachineTimer(0.1)
			self.cycleStateMessageTimer.reset()

		status.poll()

		# print messages every x
		if self.cycleStateMessageTimer.timeOut:
			self.cycleStateMessageTimer.reset()
			print "state %s" % status.state
			print "interp state %s" % status.interp_state
			if status.inpos: print "Inposition"
			else: print "NOT in position"
			if status.delay_left > 0: print "Waiting for delay"

		#commands = ["G0 X5", "G4 P0.1", "G1 Y5 F150", "G4 P0.1", "G0 Y0", "G0 X50"]
		commands = ["G0 Y16.4 X100", "G0 X50", "G4 P2", "G1 Y30 F25", "G4 P2", "G0 Y16.4", "G0 X100" ]

		#length = len(commands)
		# print "queue length %s" % status.queue
		# if status.inpos or status.delay_left > 0.0:
		# 	print "we are either dwelling or in position"

		if status.task_mode == emc.MODE_MDI \
		 	and status.interp_state == emc.INTERP_IDLE \
		 	and self.moveCounter != len(commands) \
		 	and (status.inpos or status.delay_left > 0.0): # TODO: needs revising
			
		#if self.readyForNextMove:
			if ok_for_mdi():
				print "moveCounter = %s" % self.moveCounter
				print "task mode is MODE_MDI, issuing command %s" % commands[self.moveCounter]				
				# move to next position
				command.mdi(commands[self.moveCounter])
				self.moveCounter += 1
				# print ("time C %.6f" % time.time())

			else:
				print "not ready for MDI or not in position"


		if status.state == emc.RCS_DONE and status.inpos:
		# if self.moveCounter == len(commands) and (status.inpos or status.delay_left <= 0.0):
		# 	#print "rat"
			h['spindle'] = 0
			h['spindleSpeed'] = 0.0
			self.newState("OPENVICE")
			

		# else: print "Not in MDI Mode"

	# utility methods
	def setViceOpen(self):
		h['viceOpenValve'] = 1
		h['viceCloseValve'] = 0

	def setViceClose(self):
		h['viceOpenValve'] = 0
		h['viceCloseValve'] = 1

	def setViceInactive(self):
		h['viceOpenValve'] = 0
		h['viceCloseValve'] = 0

	def openVice(self):
		if self.entry:
			print "open vice entry"
			self.entry = False
			self.viceUnClampTimer.reset()

		if h['footPedal']:
			self.setViceOpen()
			h['dumpValve'] = 1
			self.viceUnClampTimer.setRunning(True)
		else:
			self.setViceInactive()
			h['dumpValve'] = 0
			self.viceUnClampTimer.setRunning(False)

		if self.viceUnClampTimer.timeOut:
			print "end state"
			self.newState("READY")


	# dict of state functions
	states = {	"READY" : ready,
				"STANDBY" : standby,
				"MANUAL" : manual,
				"CLOSEVICE" : closeVice,
				"STARTSPINDLE" : startSpindle, 
				"CYCLE" : cycle,
				"OPENVICE" : openVice
	}

	def __init__(self):
		threading.Thread.__init__(self)

		self.currentState = "STANDBY"
		self.entry = True
		self.standbyTimer = MachineTimer(1, False)
		self.standbyTimer.start()

		self.timer2 = MachineTimer(1, False)
		
		self.moveCounter = 0

		#periodically print current state name
		self.printStateTimer = MachineTimer(15)
		self.printStateTimer.start()

		self.cycleStateMessageTimer = MachineTimer(0.5)
		self.cycleStateMessageTimer.start()

		self.spindleStartUptimer = MachineTimer(0.05, False)
		self.viceUnClampTimer = MachineTimer(1, False)

		self.requestedState = None

	def run(self):
		# print self.statenames[self.currentState]
		try:
			while 1:
				# execute the current state
				self.states[self.currentState](self)

				# perodically print the state to stdout
				if self.printStateTimer.timeOut:
					self.printStateTimer.reset()
					print "CURRENT STATE is %s" % self.currentState

				# limitation that we cannot be sure that multiple requests will be
				# handled. 
				if self.requestedState:
					newState(self.reqestedState)
		except KeyboardInterrupt:
			raise SystemExit



h = hal.component("machine")

#inputs
h.newpin("mcb1", hal.HAL_BIT, hal.HAL_IN)
h.newpin("mcb2", hal.HAL_BIT, hal.HAL_IN)
h.newpin("mcb3", hal.HAL_BIT, hal.HAL_IN)

h.newpin("startButton", hal.HAL_BIT, hal.HAL_IN)
h.newpin("stopButton", hal.HAL_BIT, hal.HAL_IN)

h.newpin("viceSafetyRelay", hal.HAL_BIT, hal.HAL_IN)
h.newpin("eStopRelay", hal.HAL_BIT, hal.HAL_IN)
h.newpin("2HandControlRelay", hal.HAL_BIT, hal.HAL_IN)
h.newpin("footPedal", hal.HAL_BIT, hal.HAL_IN)

h.newpin("requestManual", hal.HAL_BIT, hal.HAL_IN)

#outputs
h.newpin("viceOpenValve", hal.HAL_BIT, hal.HAL_OUT)
h.newpin("viceCloseValve", hal.HAL_BIT, hal.HAL_OUT)
h.newpin("dumpValve", hal.HAL_BIT, hal.HAL_OUT)
h.newpin("hydraulicMotor", hal.HAL_BIT, hal.HAL_OUT)
h.newpin("spindle", hal.HAL_BIT, hal.HAL_OUT)
h.newpin("spindleSpeed", hal.HAL_FLOAT, hal.HAL_OUT)

h.ready()

status = emc.stat()
command = emc.command()

def ok_for_mdi():
    status.poll()
    return not status.estop and status.enabled and status.homed and (status.interp_state == emc.INTERP_IDLE)

try:
	machine = StateMachine()
	machine.start()

	app = hmi(machine)
	gtk.main()

	while 1:
		variable = 1

except KeyboardInterrupt:
	raise SystemExit

# res = os.spawnvp(os.P_WAIT, "halcmd", ["halcmd", "-i", vars.emcini.get(), "-f", postgui_halfile])
# connect the new pins to the system
# processid = os.spawnvp(os.P_WAIT, "halcmd", ["halcmd", "-f", "post.hal"])
# if processid:
# 	raise SystemExit, processid


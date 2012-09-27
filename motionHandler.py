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
#class MachineTimer():

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


#class MotionHandler(threading.Thread):
class MotionHandler():

	# change the state of the machine
	def newState(self, stateName):
		# global entry, currentState
		self.entry = True;
		self.currentState = stateName
		print "Chaning state to %s" % stateName

	def waiting(self):
		if self.entry:
			self.entry = False

			# if command:
			# 	command.state(emc.STATE_OFF)

		if h['enableMotion']:
			self.newState("ENABLE")


	# def readyForNextMove(self):
	# 	if status.task_mode == emc.MODE_MDI \
	# 	and status.interp_state == emc.INTERP_IDLE \
	# 	and self.moveCounter != len(commands):
	# 		if status.inpos or status.delay_left > 0.0:
	# 			return True

	# 	return False

	def enable(self):
		
		status.poll()

		if self.entry:
			#print "ready entry"
			self.entry = False
			#'h['hydraulicMotor'] = 1
			
			# need to drive motion.enable to true
			if command:
				command.state(emc.STATE_ON)
				command.mode(emc.MODE_MDI)
		
		

		# turn on if required
		if status.task_state == emc.STATE_OFF:
			command.state(emc.STATE_ON)
		
		# if status.state == emc.STATE_ON \
		# and status.mode == emc.MODE_MDI:
		# 	self.newState("MOTION")

		if status.task_state == emc.STATE_ON:
			self.newState("MOTION")

	def motionAuto(self):

		status.poll()

		if self.entry:
			print "auto cycle"
			self.entry = False
			command.mode(emc.MODE_AUTO)



			#self.moveCounter = 0

		if status.task_mode == emc.MODE_AUTO \
		and status.state != emc.RCS_EXEC \
		and status.task_state == emc.STATE_ON:
			command.auto(emc.AUTO_RUN, 0)
			self.newState("WAITCOMPLETE")

	def waitForCompletion(self):
		if self.entry:
			self.entry = False

		status.poll()

		if status.task_mode == emc.MODE_MANUAL \
		and status.state == emc.RCS_DONE:
			self.newState("FINAL")

	def motion(self):
		# global status
		# global command

		if self.entry:
			print "cycle entry"
			self.entry = False
			command.mode(emc.MODE_MDI)
			self.moveCounter = 0
			#self.slowDownTimer = MachineTimer(0.1)
			#self.cycleStateMessageTimer.reset()

		status.poll()

		# print messages every x
		# if self.cycleStateMessageTimer.timeOut:
		# 	self.cycleStateMessageTimer.reset()
		# 	print "state %s" % status.state
		# 	print "interp state %s" % status.interp_state
		# 	if status.inpos: print "Inposition"
		# 	else: print "NOT in position"
		# 	if status.delay_left > 0: print "Waiting for delay"

		commands = ["G0 Y16.4 X100", "G0 X50", "G4 P2", "G1 Y30 F25", "G4 P2", "G0 Y16.4", "G0 X100" ]

		#length = len(commands)
		# print "queue length %s" % status.queue
		# if status.inpos or status.delay_left > 0.0:
		# 	print "we are either dwelling or in position"

		if status.interp_state == emc.INTERP_IDLE \
		 	and self.moveCounter != len(commands) \
		 	and (status.inpos or status.delay_left > 0.0): # TODO: needs revising
			
			print "moveCounter = %s" % self.moveCounter
			print "task mode is MODE_MDI, issuing command %s" % commands[self.moveCounter]				
			# move to next position
			command.mdi(commands[self.moveCounter])
			self.moveCounter += 1
			# print ("time C %.6f" % time.time())

		else:
				print "not ready for MDI or not in position"


		if status.state == emc.RCS_DONE \
			and status.inpos \
			and status.delay_left <= 0.0:
		# if self.moveCounter == len(commands) and (status.inpos or status.delay_left <= 0.0):
		# 	#print "rat"
			# h['spindle'] = 0
			# h['spindleSpeed'] = 0.0
			self.newState("FINAL")
			

		# else: print "Not in MDI Mode"


	def final(self):
		if self.entry:
			self.entry = False
			
			#command.state(emc.STATE_OFF)
			h['motionComplete'] = 1
			return

		#wait for enable to drop before return to waiting...
		if h['enableMotion'] == 0:
			self.newState("WAITING")
			h['motionComplete'] = 0

	def finalOld(self):
		if self.entry:
			self.entry = False
			
			command.state(emc.STATE_OFF)
			return

		status.poll()
		if status.state == emc.STATE_OFF:
			#self.newState("WAITING")
			#signal motionComplete
			h['motionComplete'] = 1

		#wait for enable to drop before return to waiting...
		if h['enableMotion'] == 0:
			self.newState("WAITING")
			h['motionComplete'] = 0

	# dict of state functions
	states = {	"WAITING" : waiting, 
				"ENABLE" : enable,
				"MOTION" : motionAuto,
				"WAITCOMPLETE" : waitForCompletion,
				"FINAL" : final
	}

	def __init__(self):
		#threading.Thread.__init__(self)

		self.currentState = "WAITING"
		self.entry = True
		self.moveCounter = 0

		#periodically print current state name
		self.printStateTimer = MachineTimer(15)
		self.printStateTimer.start()

		# self.cycleStateMessageTimer = MachineTimer(0.5)
		# self.cycleStateMessageTimer.start()

		# self.spindleStartUptimer = MachineTimer(0.05, False)
		# self.viceUnClampTimer = MachineTimer(1, False)

		# self.requestedState = None

	def runOld(self):
		# print self.statenames[self.currentState]
		try:
			while 1:
				# execute the current state
				self.states[self.currentState](self)

				# perodically print the state to stdout
				if self.printStateTimer.timeOut:
					self.printStateTimer.reset()
					print "Motion Handler current is %s" % self.currentState

				
		except KeyboardInterrupt:
			raise SystemExit

	def run(self):
		self.states[self.currentState](self)

		# perodically print the state to stdout
		if self.printStateTimer.timeOut:
			self.printStateTimer.reset()
			print "Motion Handler current is %s" % self.currentState

h = hal.component("motionHandler")

#inputs
h.newpin("enableMotion", hal.HAL_BIT, hal.HAL_IN)
h.newpin("enableManual", hal.HAL_BIT, hal.HAL_IN)

h.newpin("motionComplete", hal.HAL_BIT, hal.HAL_OUT)


h.ready()

status = emc.stat()
command = emc.command()

try:
	machine = MotionHandler()
	while 1:
		machine.run()

except KeyboardInterrupt:
	raise SystemExit

# def ok_for_mdi():
#     status.poll()
#     return not status.estop and status.enabled and status.homed and (status.interp_state == emc.INTERP_IDLE)

# try:
# 	machine = MotionHandler()
# 	machine.start()

# 	# app = hmi(machine)
# 	# gtk.main()

# 	while 1:
# 		variable = 1

# except KeyboardInterrupt:
# 	raise SystemExit

# res = os.spawnvp(os.P_WAIT, "halcmd", ["halcmd", "-i", vars.emcini.get(), "-f", postgui_halfile])
# connect the new pins to the system
# processid = os.spawnvp(os.P_WAIT, "halcmd", ["halcmd", "-f", "post.hal"])
# if processid:
# 	raise SystemExit, processid


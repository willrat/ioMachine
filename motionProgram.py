#
#
# things we want to pickle

import emc
import os
import gettext

gettext.install('machine')

parameters = [ _('Program Name'),
               _('Forming Start Position X (mm)'),
               _('Forming Start Position Y (mm)'),
               _('Position To Tube Y (mm)'),
               _('Position To Tube Feed  (mm/s)'),
               _('Forming Position Y  (mm)'),
               _('Forming Feed  (mm/s)'),
               _('Forming Dwell (s)'),
               _('Tube Stop Position X  (mm)'),
               _('Tube Stop Position Y (mm)'),
               _('Vice Unclamp Timer (s)')]

units = ['',
         'mm',
         'mm',
         'mm',
         'mm/s',
         'mm',
         'mm/s',
         's',
         'mm',
         'mm',
         's' ]


command = emc.command()
status = emc.stat()

class motionProgram():
    
  def __init__(self):
    print "init motionControlProgram"

    self.program = [_('Default Program'),
                    90,
                    0,
                    0,
                    250,
                    0,
                    50,
                    1,
                    25,
                    5,
                    0.5]

    print self.program

  def fillListStore(self, listStore):
    counter = 0
    for item in self.program:
    
      listStore.append( [ parameters[counter], item] )
      counter += 1


## TODO: this need to reference the gremlin to update

# # load created text program into emc
#  def loadMotionControlProgram(self):
#    if command:
#      command.mode(emc.MODE_MDI)
#      command.wait_complete()
#      command.mode(emc.MODE_AUTO)
#      command.wait_complete()
#      
#      print "LOAD: Done state prepare"
#      self.command.program_open("/tmp/MotionProgram.ngc")
#      
#      self.builder.get_object("hal_gremlin1").load("/tmp/MotionProgram.ngc")
#         
#      if self.verbose:
#          print "LOAD: Done Load command issue"
      

  def createProgram(self):

    programName = self.program[0]
    startPositionX = float(self.program[1])
    startPositionY = float(self.program[2])
    positionToTubeY = float(self.program[3])
    positionToTubeFeed = float(self.program[4])                               
    formingPositionY = float(self.program[5])
    formingFeed = float(self.program[6])
    formingDwell = float(self.program[7])
    tubeStopPositionX = float(self.program[8])
    tubeStopPositionY = float(self.program[9])

    # logic checking
    if startPositionY > positionToTubeY:
        startPositionY = 0
        
    if positionToTubeY > formingPositionY:
        positionToTubeY = 0

    programString = ""
    programString += "; program for %s\n" % (programName)
    programString += ";rapid to safe position\n"
    programString += "G0 Y0\n"
    programString += "G0 X100\n"

    programString += "G1 X %2.2f Y %2.2f F1000\n" % (startPositionX, startPositionY)
    programString += "M3 S200\n"

    programString += "G1 Y %2.2f F %2.2f \n" % (positionToTubeY, positionToTubeFeed)
    programString += "G1 Y %2.2f F %2.2f \n" % (formingPositionY, formingFeed)
    programString += "G4 P %2.2f \n" % (formingDwell)

    programString += "G1 X %2.2f Y %2.2f F1000\n" % (startPositionX, startPositionY)
    programString += "M4 S200\n "
    programString += "G1 X %2.2f Y %2.2f F1000\n" % (tubeStopPositionX, tubeStopPositionY)
    programString += "M30\n"
    
    #programString += "G1 X %2.2f Y %2.2f F1000\n" % (startPositonX, startPositonY)

    f = open('/tmp/MotionProgram.ngc', 'w')
    f.write(programString)
    f.close()
    
    print "*****************************"
    print "Written program"
    print programString
    print "*****************************"


  
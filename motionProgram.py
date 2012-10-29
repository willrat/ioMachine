import emc
import copy

#import gettext
#import language
from language import *

#parameters = [ _('Program Name'),
#               _('Forming Start Position X (mm)'),
#               _('Forming Start Position Y (mm)'),
#               _('Forming Position Y  (mm)'),
#               _('Forming Feed  (mm/s)'),
#               _('Forming Dwell (s)'),
#               _('Tube Stop Position X  (mm)'),
#               _('Tube Stop Position Y (mm)'),
#               _('Vice Unclamp Timer (s)')]

parameters = [ _('Program Name'),
               _('Forming Start Position X'),
               _('Forming Start Position Y'),
               _('Forming Position Y'),
               _('Forming Feed'),
               _('Forming Dwell'),
               _('Tube Stop Position X '),
               _('Tube Stop Position Y'),
               _('Vice Unclamp Timer'),
               _('Clearance Position X')]

isNumeric = [0,
             1,
             1,
             1,
             1,
             1,
             1,
             1,
             1,
             1]

units = ['',
         'mm',
         'mm',
         'mm',
         'mm/s',
         's',
         'mm',
         'mm',
         's',
         'mm']


command = emc.command()
status = emc.stat()

class motionProgram():

  def __init__(self, mp=None):
    #print "init motionControlProgram"

    if mp:
      print "MOTION PROGRAM: Creating copy"
      self.program = copy.deepcopy(mp.program)
    else:
      print "MOTION PROGRAM: Creating new default"
      self.program = [_('Default Program'),
                      90,
                      0,
                      0,
                      50,
                      1,
                      25,
                      5,
                      0.5,
                      0]

    print self.program

  def fillListStore(self, listStore):
#    counter = 0
#    for item in self.program:
#    
#      listStore.append( [ parameters[counter], item] )
#      counter += 1

    lenProgram = len(self.program)
    lenParameters = len(parameters)

    for counter, item in enumerate(parameters):

      if counter < lenProgram:
        # use float conversion to format string
        itemText = self.program[counter]
        if self.isNumeric(counter):
          itemText = float(itemText)

        listStore.append([item, itemText])
      else:
        listStore.append([item, float(0.0)])

  def updateFromlistStore(self, listStore):

    self.program = []
    # copy the values from the list store back into the 
    # current program array 
    for i, item in enumerate(listStore):

        #self.currentProgram.program[i] = item[1]
        self.program.append(item[1])

  def isClearancePosition(self):
    try:
      pos = float(self.program[9])
      return not (pos == 0.0)
    except:
      return False

  def getValue(self, parameter):
    counter = 0
    for item in self.program:
      if parameters[counter] == parameter:
        return self.program[counter]
      counter = counter + 1

  def getParameterLabel(self, index):
    return parameters[int(index)]

  def isNumeric(self, index):
    try:
      if isNumeric[int(index)]:
        return True
      else:
        return False
    except:
      return False



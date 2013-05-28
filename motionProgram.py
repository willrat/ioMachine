import emc
import copy

from language import *

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

#limits = [( -1,-1 ),(1,1) ]
maxValue = [0.0,
            100.0,
            22.0,
            22.0,
            150.0,
            10.0,
            98.0,
            22.0,
            2.0,
            100.0]


command = emc.command()
status = emc.stat()

class motionProgram():

  def __init__(self, mp=None):
    #print "init motionControlProgram"

    if mp:
      print "MOTION PROGRAM: Creating copy"
      self.program = copy.deepcopy(mp.program)
      self.program[0] = self.program[0] + _(" (COPY)")
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

  #  static
  def getParameterLabel(self, index):
    return parameters[int(index)]

  #  static
  def isNumeric(self, index):
    try:
      if isNumeric[int(index)]:
        return True
      else:
        return False
    except:
      return False

  # not used
  def checkRange(self, index):
    value = float(self.program[index])
    maxVal = float(maxValue[index])

    if value > max:
      self.program[index] = max[index]

  #  static
  @staticmethod
  def validateValue(index, value):
    maxVal = float(maxValue[index])
    if value > maxVal:
      return maxVal
    return value




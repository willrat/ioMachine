#
#
# things we want to pickle

import gui1


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


  
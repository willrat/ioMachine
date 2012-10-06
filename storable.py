#
#
# things we want to pickle

from motionProgram import motionProgram

class storable():
    
  def __init__(self):
    # create store for all programs on the 'hmi'
    self.programs = []
    
    self.programs.append(motionProgram())
    self.programs.append(motionProgram())
    self.programs.append(motionProgram())
    self.programs.append(motionProgram())
    
    # plus other things we might need to keep
    # track 
    
  def getPrograms(self):
    return self.programs
    
  
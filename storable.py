#
#
# things we want to pickle

import gui1

class storable():
    
  def __init__(self, stateMachine=None):
    # create store for all programs on the 'hmi'
    self.programs = []
    
    self.programs.append(motionControlProgram())
    self.programs.append(motionControlProgram())
    self.programs.append(motionControlProgram())
    self.programs.append(motionControlProgram())
    
  
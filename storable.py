#
#
# data store

# from motionProgram import motionProgram

import pickle

FILENAME = "./machineSettings.pkl"

class storable():

  def __init__(self):
    # create store for all programs on the 'hmi'
    self.programs = []
#
    # create 1 default program so there is never an empty list
   # self.programs.append(motionProgram())

    # plus other things we might need to keep
    # track here....
    self.currentIndex = 0
    self.language = ""


  def remove(self, index):
    pass


  def getPrograms(self):
    return self.programs

  def saveState(self):
    self.pickleData()

  def loadState(self):
    self.unPickleData()

  def pickleData(self):
    # store the storable to disk
    # TODO: we could have a time stamped file here in case of corruption
    file = open(FILENAME, "wb")
    pickle.dump(self.__dict__, open(FILENAME, "wb"))
    file.close()


  def unPickleData(self):
    # get the storable back from disk
    try:
      file = open(FILENAME, "rb")
      tempDict = pickle.load(file)
      self.__dict__.update(tempDict)
      file.close()
    except:
      print "STORAGE: No file %s found" % FILENAME


import copy
import gtk

from language import *


class move(object):
  def __init__(self, op= -1, pos=0.0):
    self.operation = int(op)
    self.position = float(pos)

  def getText(self):
    text = 'ERROR'
    if self.operation == 0:
      text = 'I'
    elif self.operation == 1:
      text = 'O'
    elif self.operation == -1:
      text = 'NONE'

    return (text, self.position)

  def getOperation(self):
    return int(self.operation)

  def getPosition(self):
    return float(self.position)

  def setFromText(self, tuple):
    if tuple[0] == 'I':
      self.operation = 0
    elif tuple[0] == 'O':
      self.operation = 1
    else:
      self.operation = -1
    self.position = tuple[1]

# class axisConfig(object):
#   def __init__(self):
#     # this is the base size of this axi
#     self.baseSize = 0
#     # this is the position on the axis where baseSize is
#     self.offset = 0
#     pass

class toolConfiguration(object):
  def __init__(self, mp=None):
    self.settings = []
    self.settings.append(toolSetting())
    self.settings.append(toolSetting())
    self.id = int()
    self.name = ""

class toolSetting(object):
  def __init__(self):
    self.nominalSize = float()
    self.mandrelTaper = float()
    self.offset = float()


class ioProgram(object):

  def __init__(self, mp=None):
    # print "init motionControlProgram"

    # # todo: copy code removed
    if mp:
      pass
    else:
      pass

    self.programName = ""

    self.moves = []
#     for counter in range(10):
#       # self.moves.append((-1, 0.0))
#       newMove = move()
#       newMove.operation = 1
#       newMove.position = float(counter + 1) * 1.03
#       self.moves.append(newMove)
#     self.moves.append(move(0, 2))
#     self.moves.append(move(1, 10))
#     self.moves.append(move(1, 1))
#     self.moves.append(move(1, 10))
#     self.moves.append(move(1, 1))
#     self.moves.append(move(0, 10))
#     self.moves.append(move(0, 2))
#     self.moves.append(move(1, 8))
#     self.moves.append(move(0, 10))
#     self.moves.append(move())

    self.programName = "temp program"
    self.moves.append(move(0, 2))
    self.moves.append(move(0, 5))
    self.moves.append(move(0, 2))
    self.moves.append(move(0, 5))
    self.moves.append(move(0, 2))
    self.moves.append(move(0, 5))
    self.moves.append(move(0, 2))
    self.moves.append(move(0, 5))

    self.moves.append(move())
    self.moves.append(move())

    print self.moves
    # print self.program



  # fill the list store for the program edit
  def fillListStore(self, listStore):
    for move in self.moves:
      info = (move.getText()[0], move.getText()[1], gtk.STOCK_GO_FORWARD)
      listStore.append(info)

  def updateFromlistStore(self, listStore):
    for index, move in enumerate(self.moves):
      move.setFromText(listStore[index])

  def getOperation(self, index):
    return self.moves[index]

  def getMove(self, index):
    return self.moves[index]


#   #  static
#   @staticmethod
#   def validateValue(index, value):
#     maxVal = float(maxValue[index])
#     if value > maxVal:
#       return maxVal
#     return value




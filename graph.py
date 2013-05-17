#!/usr/bin/env python

import pygtk
pygtk.require("2.0")
import gobject
import gtk
import gladevcp.makepins
from gladevcp.gladebuilder import GladeBuilder
#import threading
#import time
import hal
import emc
import os

#from decimal import *


# imports from project
from storable import storable
from motionProgram import motionProgram
from keyboard import touchKeyboard

from language import *


FINAL = True
CYCLE_PROGRAM = "/tmp/MotionProgram.ngc"
TUBE_STOP_PROGRAM = "/tmp/tubeStopProgram.ngc"

class myGraph(object):


  def initGui(self):

    self.builder = gtk.Builder()
    self.builder.add_from_file("graph.glade")

    settings = gtk.settings_get_default()
    settings.set_string_property("gtk-font-name", "Sans 14", "")

    self.builder.connect_signals(self)
    self.window1 = self.builder.get_object("window1")
    self.window1.show()


  def connectHalPins(self):
    #connect the new pins to the system
    postgui_halfile = "/home/user/installation/hmi.hal"
    processid = os.spawnvp(os.P_WAIT, "halcmd", ["halcmd", "-f", postgui_halfile])

  def __init__(self, number=0):

    self.command = emc.command()
    self.status = emc.stat()
    self.initGui()

    name = "graph"
    name += "-%s" % (number)

    self.h = hal.component(name)

    panel = gladevcp.makepins.GladePanel(self.h, "graph.glade", self.builder, None)
    self.h.ready()
    self.connectHalPins()

def printHalPins():
  #res = os.spawnvp(os.P_WAIT, "halcmd", ["halcmd", "-i", vars.emcini.get(), "-f", postgui_halfile])  
  processid = os.spawnvp(os.P_WAIT, "halcmd", ["halcmd", "show", "pin", "hmi"])
  if processid:
    raise SystemExit, processid



if __name__ == "__main__":
  try:
    app = myGraph(1)
    app = myGraph(2)
    gtk.main()
  except KeyboardInterrupt:
    raise SystemExit

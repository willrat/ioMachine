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

class hmi(object):

  #
  #  utility functions
  #

  # load created text program into emc
  def loadMotionControlProgram(self, program=CYCLE_PROGRAM):

    self.command.mode(emc.MODE_MDI)
    self.command.mode(emc.MODE_AUTO)
    self.command.program_open(program)
    self.builder.get_object("hal_gremlin1").load(program)

    h['unclampTime'] = float(self.currentProgram.program[8])

    # increment counter to inform machine.comp
    # that the new program has been loaded
    if program == TUBE_STOP_PROGRAM:
      h['cycleStatus'] = 3
    else:
      h['cycleStatus'] = 1

  def createProgram(self):

    programName = self.currentProgram.program[0]
    print "create program %s" % programName
    startPositionX = float(self.currentProgram.program[1])
    startPositionY = float(self.currentProgram.program[2])
    formingPositionY = float(self.currentProgram.program[3])
    formingFeed = float(self.currentProgram.program[4])
    formingDwell = float(self.currentProgram.program[5])
    tubeStopPositionX = float(self.currentProgram.program[6])
    tubeStopPositionY = float(self.currentProgram.program[7])

    clearancePosition = float(self.currentProgram.program[9])

    # logic checking
    if startPositionY > formingPositionY:
        startPositionY = 0

    programString = ""
    programString += "; program for %s\n" % (programName)
    programString += ";rapid to safe position\n"
    programString += "G0 Y0\n"

    #programString += "G1 X %2.2f Y %2.2f F1000\n" % (startPositionX, startPositionY)
    # rapid to start position
    programString += "G0 X %2.2f Y %2.2f \n" % (startPositionX, startPositionY)
    programString += "M3 S200\n"

    programString += "G1 Y %2.2f F %2.2f \n" % (formingPositionY, formingFeed)
    programString += "G4 P%2.2f \n" % (formingDwell)

    programString += "G1 X %2.2f Y %2.2f F1000\n" % (startPositionX, startPositionY)
    programString += "M5 S200\n "

    if self.currentProgram.isClearancePosition():
      programString += "G0 Y0\n"
      programString += "G0 X %2.2f\n" % (float(clearancePosition))
    else:
      programString += "G1 X %2.2f F1000\n" % (float(tubeStopPositionX + 1))
      programString += "G1 Y %2.2f \n" % (tubeStopPositionY)
      programString += "G1 X %2.2f F500\n" % (float(tubeStopPositionX))

    programString += "M30\n"

    #programString += "G1 X %2.2f Y %2.2f F1000\n" % (startPositonX, startPositonY)

    f = open(CYCLE_PROGRAM, 'w')
    f.write(programString)
    f.close()

    print "*****************************"
    print "Written program"
    print programString
    print "*****************************"

    tubeStopProg = ""
    tubeStopProg += "; program for %s\n" % (programName)
    tubeStopProg += "; return to tube stop position\n"

    #assuming starting from clearance position
    tubeStopProg += "G0 X %2.2f\n" % (float(clearancePosition))

    #
    tubeStopProg += "G1 X %2.2f F1000\n" % (float(tubeStopPositionX + 1))
    tubeStopProg += "G1 Y %2.2f \n" % (tubeStopPositionY)
    tubeStopProg += "G1 X %2.2f F500\n" % (float(tubeStopPositionX))
    tubeStopProg += "M30\n"

    f = open(TUBE_STOP_PROGRAM, 'w')
    f.write(tubeStopProg)
    f.close()

  #
  #  general application callbacks
  #

  def on_window1_destroy(self, widget, data=None):
    print "on_window1_destroy"
    gtk.main_quit()

  def on_manual_destroy(self, widget, data=None):
    print "on_window1_destroy"
    gtk.main_quit()

  def on_gtk_quit_activate(self, menuitem, data=None):
    print "quit from menu"
    gtk.main_quit()

  #
  # auto mode
  #


  def on_cycleToggle_toggled(self, button):

    if button.get_active():
      self.loadMotionControlProgram(program=CYCLE_PROGRAM)
#      h['cycleStatus'] = 1
    else:
      self.loadMotionControlProgram(program=TUBE_STOP_PROGRAM)
#      h['cycleStatus'] = 3


#    if h['cycleStatus'] == 2 and \
#      self.currentProgram.isClearancePosition():
#      self.loadMotionControlProgram(program=TUBE_STOP_PROGRAM)
#      # set cycle Button 
#      self.cycleToggle.set_active(False)
#      # increment counter to inform machine.comp
#      # that the new program has been loaded
#      h['cycleStatus'] = 3
#
#    elif h['cycleStatus'] == 4:
#      self.loadMotionControlProgram(program=CYCLE_PROGRAM)
#      h['cycleStatus'] = 1;
#      self.cycleToggle.set_active(True)

  #
  #  manual mode
  #

  def on_hydraulicOn_toggled(self, widget, data=None):
      print "on_hydraulicOn_toggled"
      if widget.get_active():
        print "toggle is active"

  def on_hydraulicOn_pressed(self, menuitem, data=None):
      print "hydraulic on pressed"

  def on_hydraulicOn_activate(self, menuitem, data=None):
      print "hydraulic on activate"

  def on_changeScreenButton_clicked(self, widget, data=None):
    print "on_changeScreenButton_clicked"
    self.window1.show()

  def on_viceOpenToggle_toggled(self, widget, data=None):
    print "on_viceOpenToggle_toggled"
#    if widget.get_active:
#      print "widget is active"
#    else:
#      print "widget is not active"
#
#
#    if self.viceCloseToggle:
#      if self.viceOpenToggle.get_active():
#        self.viceCloseToggle.set_active(False)
#    else:
#      print "no viceCloseToggle"


  def on_viceCloseToggle_toggled(self, widget, data=None):
    print "on_viceCloseToggle_toggled"
#    if self.viceOpenToggle:
#      if self.viceCloseToggle.get_active():
#        self.viceOpenToggle.set_active(False)
#    else:
#      print "no viceOpenToggle"

  def on_xJogSpeed_value_changed(self, adjustment):
    pass

  def on_yJogSpeed_value_changed(self, adjustment):
    pass

  # velocity information used for direction only now
  def on_jogZPlus_pressed(self, widget, data=None):
    self.jogAxis(0, 75)

  def on_jogZPlus_released(self, widget, data=None):
    self.jogAxis(0, 0)

  def on_jogZMinus_pressed(self, widget, data=None):
    self.jogAxis(0, -75)

  def on_jogZMinus_released(self, widget, data=None):
    self.jogAxis(0, 0)

  def on_jogXPlus_pressed(self, widget, data=None):
    self.jogAxis(1, 35)

  def on_jogXPlus_released(self, widget, data=None):
    self.jogAxis(1, 0)

  def on_jogXMinus_pressed(self, widget, data=None):
    self.jogAxis(1, -35)

  def on_jogXMinus_released(self, widget, data=None):
    self.jogAxis(1, 0)


  #def jogAxis(self, axis, velocity):
  def jogAxis(self, axis, velocity):

    axisSpeed = 0

    if axis == 0:
      axisSpeed = self.xJogSpeed.value
    elif axis == 1:
      axisSpeed = self.yJogSpeed.value

    print "axis speed %s" % (axisSpeed)

    if velocity == 0:
      pass
    elif velocity < 0:
      velocity = -axisSpeed
    else:
      velocity = axisSpeed

    if self.command and self.status:
      self.status.poll()
      if self.status.task_mode == emc.MODE_MANUAL:
        if velocity == 0:
          self.command.jog(emc.JOG_STOP, axis)
          h['hydraulicAxisJog'] = 0
        else:
          if axis == 1:
            h['hydraulicAxisJog'] = 1
            #time.sleep(0.1)
          self.command.jog(emc.JOG_CONTINUOUS, axis, velocity)
      else:
        print "cannot jog: machine not in manual"
      # for item in self.status.position:
      #   print "postiton %s" % item

  #
  #  controls for notebook, should lock out screen in certain modes...
  #


#  def on_notebook1_select_page(self, notebook, page, page_num, data=None):
#    print "SELECT PAGE"

#  def pollConnections(self):
#
#
#    if self.currentStateString == "MANUAL":
#      #print "current state is manual; set sensitivity appropriately"
#      pass
#    elif self.currentStateString in cycleStates:
#      #print "current state is inCycle"
#      pass
#    else:
#      pass
#      #print "either in standby or in ready"
#
#    return True

  def setNonAutoPagesInactive(self):
    notebook = self.builder.get_object("notebook1")

    for pageNumber in [1, 2, 3]:
      page = notebook.get_nth_page(pageNumber)
      if page:
        page.set_sensitive(False)

    self.builder.get_object("editProgram").set_sensitive(False)

  def setPagesActive(self):
    notebook = self.builder.get_object("notebook1")

    for pageNumber in range(4):
      page = notebook.get_nth_page(pageNumber)
      if page:
        page.set_sensitive(True)

  def on_notebook1_switch_page(self, notebook, page, page_num, data=None):
    print "SWITCH PAGE call back"

    currentPage = notebook.get_current_page()
    print "Switching to page: %s" % page_num
    print "Current page is:   %s" % currentPage

    # set the manual request flag to the machine controller    
    if currentPage == 1:
        h['requestManual'] = 0
    elif page_num == 1:
        h['requestManual'] = 1

    # in auto mode page
    if currentPage == 0:
      #check for 'in cycle', disable notebook pages if so
      if self.currentStateString in cycleStates:
        self.setNonAutoPagesInactive()
      else:
        self.setPagesActive()

      return


  def on_treeview1_row_activated(self, widget, row, col):
    print "row double click"
    print "row %s , col %s" % (row, col)

  def on_treeview1_select_cursor_row(self, widget, data=None):
    print "select cursor row"

  def on_treeview1_cursor_changed(self, widget):
    # here we can find the selected program in the list.
    print "on_treeview1_cursor_changed"
    #widget.


  #
  #  auto screen callbacks
  #
  def on_editProgram_clicked(self, button):
    #load the current program into the dialog's liststore



    self.editCurrent()


  # update the dynamic elements on the screens
  def cyclicUpdate(self):
    # udpate labels
    #

    currentLabelText = _("Current Program:")
    currentLabelText += " "
    currentLabelText += self.currentProgram.program[0]

    self.builder.get_object("currentProgramLabel").set_text(currentLabelText)
    self.builder.get_object("currentProgramLabel1").set_text(currentLabelText)


    #print self.currentProgram[0][1]

    # update the position display
    if self.status:
      self.status.poll()
      positionText = 'X: % 2.2f Y: % 2.2f' % (self.status.actual_position[0], self.status.actual_position[1])

      self.positionLabel = self.builder.get_object("positionLabel1")
      if self.positionLabel:
        self.positionLabel.set_text(positionText)

    # update current state
    self.currentStateString = states[h['currentState']]
    label = self.builder.get_object("stateLabel")
    if states[h['currentState']] and label:
      label.set_text(self.stateMachine.currentState)
    elif label:
      label.set_text("cannot get machine state")

    # set jog buttons off if the 
    # TODO: Read if jog OK
    jogButtonBox = self.builder.get_object("jogButtonBox")
    if jogButtonBox:
      if h['enableJogButtons']:
        jogButtonBox.set_sensitive(True)
      else:
        jogButtonBox.set_sensitive(False)

    # update status label at top of screen
    statusLabel = self.builder.get_object("statusLabel")
    statusText = ""
    statusText += _("Current Status: ")
    try:
      statusText += stateTextVerbose[h['currentState']]
    except:
      statusText += _("ERROR could not get status")

    statusLabel.set_text(statusText)

    # disable controls when the program runs     
    if self.currentStateString in cycleStates:
      self.builder.get_object("editProgram").set_sensitive(False)
    else:
      self.builder.get_object("editProgram").set_sensitive(True)

    # from machine.comp
    #enum cycleStatus {  STATUS_START = 0,
    #          STATUS_CYCLE_PROGRAM_READY,
    #          STATUS_CYCLE_PROGRAM_DONE,
    #          STATUS_STOPPOS_PROGRAM_READY,
    #          STATUS_STOPPOS_PROGRAM_DONE,
    #          STATUS_MAX
    #};

    # if a separate tube stop program is required switch
    # to load tube stop program and back again
    if h['cycleStatus'] == 2 and \
      self.currentProgram.isClearancePosition():
      self.loadMotionControlProgram(program=TUBE_STOP_PROGRAM)
      # set cycle Button 
      self.tubeStopToggle.set_active(True)
      self.cycleToggle.set_active(False)

    elif h['cycleStatus'] == 4 :
      self.loadMotionControlProgram(program=CYCLE_PROGRAM)
      self.tubeStopToggle.set_active(False)
      self.cycleToggle.set_active(True)

    elif h['cycleStatus'] == 2:
      # the program is already loaded so set the flag
      # to let machine.comp know
      h['cycleStatus'] = 1;

    if self.currentProgram.isClearancePosition():
      self.tubeStopToggle.set_sensitive(True)
    else:
      self.tubeStopToggle.set_sensitive(False)



    return True

  #
  #  program save/load management 
  #

  # set the current program from the index 
  def setCurrent(self, index):
    self.s.currentIndex = index
    self.currentProgram = self.programs[self.s.currentIndex]


  # open the dialog box for editing the current program
  def editCurrent(self):

    # clear the list store in the dialog 
    self.programListStore.clear()

    # copy the data over to fill the editor   
    self.currentProgram.fillListStore(self.programListStore)

    self.programDialog.present()
    self.programDialog.fullscreen()

  # load the current program into the motion control
  def loadCurrent(self):
    self.createProgram()
    self.loadMotionControlProgram()
    self.builder.get_object("hal_gremlin1").expose()

    # this list store is used to display the current program
    # on the auto page so need the new program loading into
    # it
    self.programListStore.clear()
    self.currentProgram.fillListStore(self.programListStore)

  # create a new program based on the current
  def on_newProgramButton_clicked(self, button):

    # add a copy of the current program
    print "HMI: New Program"
    newProgram = motionProgram(self.currentProgram)
    newIndex = len(self.programs)
    self.programs.append(newProgram)
    self.setCurrent(newIndex)
    self.currentProgram = newProgram
    self.buildProgramList()
    self.editCurrent()

  # make the selected program the current and load into motion
  def on_loadProgramButton_clicked(self, button):
    # get the reference of the current selected program in the program tree view
    cursor = self.builder.get_object("treeview1").get_cursor()
    #print self.programs[cursor[0][0]]        
    self.setCurrent(cursor[0][0])
    # load data into motion control etc
    self.loadCurrent()
    self.s.saveState()

  def on_deleteProgramButton_clicked(self, button):

    cursor = self.builder.get_object("treeview1").get_cursor()
    removeIndex = int(cursor[0][0])

    # do not allow less than 1 program
    if len(self.s.getPrograms()) <= 1:
      return

    #print self.currentProgram
    removed = self.programs.pop(removeIndex)

    if removeIndex == self.s.currentIndex:
      print "remove current program"
      self.setCurrent(0)
      self.loadCurrent()
    else:
      # find the current program in the list      
      for (counter, item) in enumerate(self.programs):
        if item == self.currentProgram:
          self.setCurrent(counter)
          print "new index is %s" % counter
          break

#    if self.programs[removeIndex] == self.currentProgram:
#      print "remove current program"
#      removed = self.programs.pop(removeIndex)  
#      self.setCurrent(0)
#      self.loadCurrent()
#    else:
#      removed = self.programs.pop(removeIndex)
#      for (counter, item) in enumerate(self.programs):
#        if item == self.currentProgram:
#          self.setCurrent(counter)
#          print "new index is %s" % counter
#          break

    self.buildProgramList()

  #
  #  program edit dialog methods
  #

  def on_value_clicked(self, widget, path, text):
    print "on value clicked"
    print "new text is %s" % text
    print "path is %s" % path
    print widget
    self.programListStore[path][1] = text

  def on_programEditCancel_clicked(self, button):
    print "cancel editing program"
    self.programDialog.iconify()

  def on_programEditOK_clicked(self, button):
    self.currentProgram.updateFromlistStore(self.programListStore)

    print "current program is now:"
    for line in self.currentProgram.program:
        print line

    # create ngc file, load to motion, update gremlin, 'close' window
    self.loadCurrent()
    self.programDialog.iconify()
    self.buildProgramList()
    self.s.saveState()

  def on_editing_started(self, cellrenderer, editable, path, user_param1=None):
    #print "on editing started"    
    self.keyb.getWindow().present()
    self.keyb.reset()
    # store the row we are editing
    self.editingPath = int(path)
#    try:
#      index = int(path)
#    except:
#      index = 0
#      print "COULD NOT CONVERT PATH TO INDEX"

    print "Editing started: path %s" % path

    #load the current string on for editing....    
    self.keyb.setString(self.programListStore[self.editingPath][1])

    # TODO: we could have a box displaying current value for reference
    self.keyb.setParameterLabel(self.currentProgram.getParameterLabel(path))

    isNumeric = self.currentProgram.isNumeric(self.editingPath)
    self.keyb.setNumeric(isNumeric)


  #
  #  system screen
  #  

  def on_shutdownButton_clicked(self, button):
    processid = os.spawnvp(os.P_WAIT, "sudo", ["sudo", "halt"])
    if processid:
      print "shutdown failed"
      #raise SystemExit, processid
    pass

  def on_restartButton_clicked(self, button):
    processid = os.spawnvp(os.P_WAIT, "sudo", ["sudo", "reboot"])
    if processid:
      print "restart failed"
    pass

  def on_changeLanguageButton_clicked(self, button):
    pass
    #on_changeLanguageButton_clicked
    # DOES NOT WORK.... Changing language on the fly is not very good
    # at the moment on this platform

#    print "change language button clicked"
#    lang1.install()
#    
#    locale.setlocale(locale.LC_ALL, "en_GB.utf8")
#    locale.bindtextdomain(APPLICATION_DOMAIN, './locale')

#    self.window1.destroy()
#    self.programDialog.destroy()
#    self.keyb.getWindow().destroy()
#    
#    self.initAll()
#    self.fillLists()



  #
  #  methods for the on screen keyboard
  #

  def on_entryOK_clicked(self, button):
    inputText = self.keyb.getString()

    if self.currentProgram.isNumeric(self.editingPath):
      pass
      # strip zeros from string
      self.programListStore[self.editingPath][1] = (float(inputText))
    else:
      self.programListStore[self.editingPath][1] = inputText

  #
  #  init etc...
  #

  def buildProgramList(self):

    if not self.listStore:
      self.listStore = gtk.ListStore(gobject.TYPE_STRING)
      self.listView.set_model(self.listStore)

    # look up the name of the program from the store and
    # add to the liststore
    self.listStore.clear()
    print "**** Build Program List ****"
    for entry in self.s.getPrograms():

      print "***** %s *****" % entry.program[0]
      print entry

      self.listStore.append([entry.program[0]])

    # save the program list
    self.s.saveState()

  def initGui(self):
    mediumButtonHeight = 60
    largeButtonHeight = 80

    self.builder = gtk.Builder()
    self.builder.set_translation_domain('machine')
    self.builder.add_from_file("gui1.glade")

    settings = gtk.settings_get_default()
    settings.set_string_property("gtk-font-name", "Sans 14", "")

    self.builder.connect_signals(self)
    self.window1 = self.builder.get_object("window1")

    #to set vars
    #self.pollConnections()

    if FINAL:
      self.window1.fullscreen()
    self.window1.show()


    self.viceCloseToggle = self.builder.get_object("viceCloseToggle")
    self.viceOpenToggle = self.builder.get_object("viceOpenToggle")
    self.listStore = None
    self.listView = self.builder.get_object("treeview1")

    self.programDialog = self.builder.get_object("programeditdialog")
    self.programTreeView = self.builder.get_object("treeview2")
    self.programListStore = self.builder.get_object("liststore2")
    self.programListStore.clear()

    self.xJogSpeed = self.builder.get_object("xJogSpeed")
    self.yJogSpeed = self.builder.get_object("yJogSpeed")

    self.cycleToggle = self.builder.get_object("cycleToggle")
    self.tubeStopToggle = self.builder.get_object("tubeStopToggle")

    # set size of jog buttons
    # using large height
    jogButtons = self.builder.get_object("jogButtonBox")
    for item in jogButtons:
      if type(item) == gtk.Button or type(item) == gladevcp.HAL_Button:
        #print "Button : %s " % item.get_label()
        item.set_size_request(225, largeButtonHeight)

    viceJogButtons = self.builder.get_object("viceJogButtons")
    for item in viceJogButtons:
      if type(item) == gtk.Button or type(item) == gladevcp.HAL_RadioButton:
        item.set_size_request(200, largeButtonHeight)

    ## other buttons 'medium'
    programStoreButtons = self.builder.get_object("programStoreButtons")
    for item in programStoreButtons:
      if type(item) == gtk.Button:
        item.set_size_request(200, mediumButtonHeight)

    programDialogButtons = self.builder.get_object("programDialogButtons")
    for item in programDialogButtons:
      if type(item) == gtk.Button:
        item.set_size_request(200, mediumButtonHeight)

    machineControlButtons = self.builder.get_object("machineControlButtons")
    for item in machineControlButtons:
      if type(item) == gtk.Button:
        item.set_size_request(200, mediumButtonHeight)

    autoButtons = self.builder.get_object("autoButtons")
    for item in autoButtons:
      if type(item) == gtk.Button:
        item.set_size_request(200, mediumButtonHeight)


  def initKeyboard(self):
    self.keyb = touchKeyboard()
    self.keyb.getOKButton().connect("clicked", self.on_entryOK_clicked)

  def connectHalPins(self):
    #connect the new pins to the system
    postgui_halfile = "/home/user/installation/hmi.hal"
    processid = os.spawnvp(os.P_WAIT, "halcmd", ["halcmd", "-f", postgui_halfile])

  def initAll(self):
    self.initGui()
    self.initKeyboard()

  def fillLists(self):
    self.buildProgramList()
    self.currentProgram.fillListStore(self.programListStore)
    pass

  def __init__(self, stateMachine=None):

    self.command = emc.command()
    self.status = emc.stat()

    self.verbose = True

    self.initAll()
#    self.initGui()
#    self.initKeyboard()

    # check for hal
    if h:
      #print "-------------------------------------------"
      #printHalPins()
      #print "-------------------------------------------"
      panel = gladevcp.makepins.GladePanel(h, "gui1.glade", self.builder, None)
      h.ready()
      self.connectHalPins()

    self.s = storable()
    self.s.loadState()

    self.programs = self.s.getPrograms()
    self.setCurrent(self.s.currentIndex)

    # go through programs and update if needed in case a new parameter
    for program in self.programs:
      self.programListStore.clear()
      program.fillListStore(self.programListStore)
      program.updateFromlistStore(self.programListStore)

    self.buildProgramList()


    # load the current program
#    self.createProgram()
#    self.loadMotionControlProgram()
    self.loadCurrent()

    # fill the list store based on the current program
#   self.currentProgram.fillListStore(self.programListStore)
    #self.fillLists()

    # udpate display and button states, polling  etc
    gobject.timeout_add(110, self.cyclicUpdate)


# enum states {   STATE_STANDBY = 0,
#                 STATE_READY,
#                 STATE_CLOSEVICE,
#                 STATE_STARTSPINDLE,
#                 STATE_CYCLE,
#                 STATE_OPENVICE,
#                 STATE_MANUAL,
#                 MAX_STATES }; //current_state;

states = [  "STANDBY",
            "READY",
            "CLOSEVICE",
            #"STARTSPINDLE",
            "CYCLE",
            "OPENVICE",
            "MANUAL"]

stateText = [   _("Standby"),
                _("Ready"),
                _("Close Vice"),
                #_("Start Spindle"),
                _("Cycle"),
                _("Open Vice"),
                _("Manual"),
                _("Cycle Aborted")]

stateTextVerbose = [    _("Standby - Press start"),
                        _("Ready - Hold control for cycle"),
                        _("Close Vice - Hold control to close vice"),
                        _("Cycle - Forming tube"),
                        _("Open Vice - Hold control to open vice"),
                        _("Manual"),
                        _("Cycle Aborted")]

# when we are in any of these states we are in a cycle
cycleStates = [ "CLOSEVICE",
                "STARTSPINDLE",
                "CYCLE",
                "OPENVICE"]

def printHalPins():
  #res = os.spawnvp(os.P_WAIT, "halcmd", ["halcmd", "-i", vars.emcini.get(), "-f", postgui_halfile])  
  processid = os.spawnvp(os.P_WAIT, "halcmd", ["halcmd", "show", "pin", "hmi"])
  if processid:
    raise SystemExit, processid



if __name__ == "__main__":
  try:
    h = hal.component("hmi")

    h.newpin("mcb1", hal.HAL_BIT, hal.HAL_IN)
    h.newpin("currentState", hal.HAL_U32, hal.HAL_IN)
    h.newpin("enableJogButtons", hal.HAL_BIT, hal.HAL_IN)
    h.newpin("hydraulicAxisJog", hal.HAL_BIT, hal.HAL_IN)

    #h.newpin("enableJogButtons", hal.HAL_BIT, hal.HAL_IN)

    h.newpin("requestManual", hal.HAL_BIT, hal.HAL_OUT)
    h.newpin("unclampTime", hal.HAL_FLOAT, hal.HAL_OUT)

    # communication between state machine
    h.newpin("cycleStatus", hal.HAL_U32, hal.HAL_IO)


  except:
    print "hal exception"

  try:
    app = hmi()


    gtk.main()
  except KeyboardInterrupt:
    raise SystemExit

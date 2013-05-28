#!/usr/bin/env python

import pygtk
pygtk.require("2.0")
import gobject
import gtk
import gladevcp.makepins
from gladevcp.gladebuilder import GladeBuilder
import hal
import os
import subprocess


import language

# imports from project
from storable import storable
from keyboard import touchKeyboard
from ioProgram import ioProgram


# enum states {   STATE_INITIAL = 0,
#         STATE_STANDBY,
#         STATE_PREPAREREADY,
#         STATE_NOTOOL,
#         STATE_READY,
#         STATE_PREPARETOOLRELEASE,
#         STATE_TOOLRELEASED,
#         STATE_LOWERPART,
#         STATE_MOTION,
#         STATE_FINALISE,
#         STATE_RAISEPART,
#         STATE_MANUAL,
#         STATE_CYCLE_ABORT,
#         STATE_LUBRICANT_LOW,
#         STATE_NO_AIR,
#         STATE_FILTER_BLOCKED,
#         STATE_INVERTER_FAULT,
#         STATE_ESTOP,
#         STATE_CALIBRATE,
#         MAX_STATES };

stateTextVerbose = [    _("STATE_INITIAL"),
                        _("STATE_STANDBY"),
                        _("STATE_PREPAREREADY"),
                        _("STATE_NOTOOL"),
                        _("STATE_READY"),
                        _("STATE_PREPARETOOLRELEASE"),
                        _("STATE_TOOLRELEASED"),
                        _("STATE_LOWERPART"),
                        _("STATE_MOTION"),
                        _("STATE_FINALISE"),
                        _("STATE_RAISEPART"),
                        _("STATE_MANUAL"),
                        _("STATE_CYCLE_ABORT"),
                        _("STATE_LUBRICANT_LOW"),
                        _("STATE_NO_AIR"),
                        _("STATE_FILTER_BLOCKED"),
                        _("STATE_INVERTER_FAULT"),
                        _("STATE_ESTOP"),
                        _("STATE_CALIBRATE"),
                        _("MAX_STATES")]

# these match the statenumbers is ioMachine.c
STATE_MANUAL = 5
STATE_CALIBRATION = 10


class hmi(object):

  #
  #  utility functions
  #


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

  #
  #  manual mode
  #

  def on_editProgramButton_clicked(self, menuitem, data=None):
    self.editCurrent()
    pass


  def on_hydraulicOn_pressed(self, menuitem, data=None):
      print "hydraulic on pressed"

  def on_hydraulicOn_activate(self, menuitem, data=None):
      print "hydraulic on activate"


  def on_changeScreenButton_clicked(self, widget, data=None):
    print "on_changeScreenButton_clicked"
    self.window1.show()
#
#   def on_viceOpenToggle_toggled(self, widget, data=None):
#     print "on_viceOpenToggle_toggled"
#
#   def on_viceCloseToggle_toggled(self, widget, data=None):
#     print "on_viceCloseToggle_toggled"
#
#   def on_xJogSpeed_value_changed(self, adjustment):
#     pass
#
#   def on_yJogSpeed_value_changed(self, adjustment):
#     pass
#
#   # velocity information used for direction only now
#   def on_jogZPlus_pressed(self, widget, data=None):
#     self.jogAxis(0, 75)
#
#   def on_jogZPlus_released(self, widget, data=None):
#     self.jogAxis(0, 0)
#
#   def on_jogZMinus_pressed(self, widget, data=None):
#     self.jogAxis(0, -75)
#
#   def on_jogZMinus_released(self, widget, data=None):
#     self.jogAxis(0, 0)
#
#   def on_jogXPlus_pressed(self, widget, data=None):
#     self.jogAxis(1, 35)
#
#   def on_jogXPlus_released(self, widget, data=None):
#     self.jogAxis(1, 0)
#
#   def on_jogXMinus_pressed(self, widget, data=None):
#     self.jogAxis(1, -35)
#
#   def on_jogXMinus_released(self, widget, data=None):
#     self.jogAxis(1, 0)
#
#
#   # def jogAxis(self, axis, velocity):
#   def jogAxis(self, axis, velocity):
#
#     axisSpeed = 0
#
#     if axis == 0:
#       axisSpeed = self.xJogSpeed.value
#     elif axis == 1:
#       axisSpeed = self.yJogSpeed.value
#
#     print "axis speed %s" % (axisSpeed)
#
#     if velocity == 0:
#       pass
#     elif velocity < 0:
#       velocity = -axisSpeed
#     else:
#       velocity = axisSpeed


  def on_addButton_clicked(self, widget, data=None):
    pass

  def on_removeButton_clicked(self, widget, data=None):
    pass

  def on_editLineButton_clicked(self, widget, data=None):
    pass

  def on_operationColumn_clicked(self, widget, data=None):
    print "on operation column clicked"
    pass

  def on_positionColumn_clicked(self, widget, data=None):
    print "on position column clicked"
    pass


  def onPositionEdit(self, widget, path, text):
    print "on position edit"
    print "widget "
    print widget
    print "path "
    print path
    self.programEditListStore[path][1] = text

  def onOperationEdit(self, widget, path, text):
    print "on operation edit"
    print "widget "
    print widget
    print "path "
    print path
    self.programEditListStore[path][1] = text

  def onPositionEditingStarted(self, cellrenderer, editable, path, user_param1=None):
    self.editCell(path, 1, 'Position')
    pass

  def onOperationEditingStarted(self, cellrenderer, editable, path, user_param1=None):
    self.editCell(path, 0, 'Operation')
    pass

  def onEditingStarted(self, cellrenderer, editable, path, user_param1=None):
    return

  def editCell(self, path, column, label):
    print "editCell: row %s , column %s" % (int(path), int(column))
    print "path"
    print path
    print "Editing started: path %s" % path
    # print "on editing started"

    # present keyboard
    self.keyb.getWindow().present()
    self.keyb.reset()

    # store the row we are editing
    self.editPath = int(path)
    self.editColumn = int(column)

    # load the current string on for editing....
    # TODO: we don't know the column we need
    try:
      self.keyb.setString(self.programEditListStore[int(path)][int(column)])
    except:
      pass

    self.keyb.setParameterLabel(label)

  #
  #  methods for the on screen keyboard
  #

  def on_entryOK_clicked(self, button):
    inputText = self.keyb.getString()
    self.programEditListStore[self.editPath][self.editColumn] = inputText


  #
  #  controls for notebook, should lock out screen in certain modes...
  #

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
      # check for 'in cycle', disable notebook pages if so
      if self.isInCycle():
        self.setNonAutoPagesInactive()
      else:
        self.setPagesActive()

      return


  def on_treeview1_row_activated(self, widget, row, col):
    print "row double click"
    print "row %s , col %s" % (row, col)

  def onRowActivated(self, widget, row, col):
    print "row double click"
    print "row %s , col %s" % (row, col)

  def on_treeview1_select_cursor_row(self, widget, data=None):
    print "select cursor row"

  def on_treeview1_cursor_changed(self, widget):
    # here we can find the selected program in the list.
    print "on_treeview1_cursor_changed"
    # widget.

  def on_calibrateButton_clicked(self, widget, data=None):
    self.calibrateDialog = self.builder.get_object("calibrateDialog")
    self.calibrateDialog.present()
    self.calibrateDialog.fullscreen()

  def on_calibrationDialogOK_clicked(self, widget, data=None):
    self.calibrateDialog = self.builder.get_object("calibrateDialog")
    self.calibrateDialog.iconify()
    # self.calibrateDialog.fullscreen()
    pass


  def on_startCalibrationButton_clicked(self, widget, data=None):
    try:
      h['requestState'] = 18
    except:
      print "Error setting request State"
    pass

  #
  #  auto screen callbacks
  #


  def isInCycle(self):
#     # update current state
#     self.currentStateString = states[h['currentState']]
#
#     if self.currentStateString in cycleStates:
#       return True

    return False

  # update the dynamic elements on the screens
  def cyclicUpdate(self):
    # udpate labels
    #

#     currentLabelText = _("Current Program:")
#     currentLabelText += " "
#     currentLabelText += self.currentProgram.program[0]
#
#     self.builder.get_object("currentProgramLabel").set_text(currentLabelText)
#     self.builder.get_object("currentProgramLabel1").set_text(currentLabelText)


    # print self.currentProgram[0][1]

    # update the position display
#     if self.status:
#       self.status.poll()
#       positionText = 'X: % 2.2f Y: % 2.2f' % (self.status.actual_position[0], self.status.actual_position[1])
#
#       self.positionLabel = self.builder.get_object("positionLabel1")
#       if self.positionLabel:
#         self.positionLabel.set_text(positionText)


    # set jog buttons off if the
    # TODO: Read if jog OK
#     jogButtonBox = self.builder.get_object("jogButtonBox")
#     if jogButtonBox:
#       if h['enableJogButtons']:
#         jogButtonBox.set_sensitive(True)
#       else:
#         jogButtonBox.set_sensitive(False)

    # update status label at top of screen

    statusText = ""
    statusText += _("Current Status: ")
    try:
      statusText += stateTextVerbose[h['currentState']]
    except:
      statusText += _("ERROR could not get status")

    self.statusLabel.set_text(statusText)

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
    self.programEditListStore.clear()

    # copy the data over to fill the editor
    self.currentProgram.fillListStore(self.programEditListStore)

    self.programDialog.present()
    # self.programDialog.fullscreen()

  # load the current program into the motion control
  def loadCurrent(self):
#     self.createProgram()
#     self.loadMotionControlProgram()
#     self.builder.get_object("hal_gremlin1").expose()

    # this list store is used to display the current program
    # on the auto page so need the new program loading into
    # it
#     self.currentProgramStore.clear()
#     self.currentProgram.fillListStore(self.currentProgramStore)
    pass

  # create a new program based on the current
#   def on_newProgramButton_clicked(self, button):
#
#     # add a copy of the current program
#     print "HMI: New Program"
#     newProgram = motionProgram(self.currentProgram)
#     newIndex = len(self.programs)
#     self.programs.append(newProgram)
#     self.setCurrent(newIndex)
#     self.currentProgram = newProgram
#     self.buildProgramList()
#     self.editCurrent()

  # make the selected program the current and load into motion
#   def on_loadProgramButton_clicked(self, button):
#     # get the reference of the current selected program in the program tree view
#     cursor = self.builder.get_object("treeview1").get_cursor()
#     #print self.programs[cursor[0][0]]
#     self.setCurrent(cursor[0][0])
#     # load data into motion control etc
#     self.loadCurrent()
#     self.s.saveState()

#   def on_deleteProgramButton_clicked(self, button):
#
#     cursor = self.builder.get_object("treeview1").get_cursor()
#     removeIndex = int(cursor[0][0])
#
#     # do not allow less than 1 program
#     if len(self.s.getPrograms()) <= 1:
#       return
#
#     #print self.currentProgram
#     removed = self.programs.pop(removeIndex)
#
#     if removeIndex == self.s.currentIndex:
#       print "remove current program"
#       self.setCurrent(0)
#       self.loadCurrent()
#     else:
#       # find the current program in the list
#       for (counter, item) in enumerate(self.programs):
#         if item == self.currentProgram:
#           self.setCurrent(counter)
#           print "new index is %s" % counter
#           break
#
#     self.buildProgramList()

  #
  #  program edit dialog methods
  #

  def on_value_clicked(self, widget, path, text):
#    print "on value clicked"
#    print "new text is %s" % text
#    print "path is %s" % path
#    print widget
    print "on value clicked"
    print "widget" + widget
    self.currentProgramStore[path][1] = text

  def on_programEditCancel_clicked(self, button):
    print "cancel editing program"
    self.programDialog.iconify()

  def on_programEditOK_clicked(self, button):
    self.currentProgram.updateFromlistStore(self.programEditListStore)
    self.loadMovesToHalPins()
    self.programDialog.iconify()

  def on_editing_started(self, cellrenderer, editable, path, user_param1=None):
    # print "on editing started"
    self.keyb.getWindow().present()
    self.keyb.reset()
    # store the row we are editing
    self.editingPath = int(path)

    print "Editing started: path %s" % path

    # load the current string on for editing....
    self.keyb.setString(self.currentProgramStore[self.editingPath][1])

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
      # raise SystemExit, processid
    pass

  def on_restartButton_clicked(self, button):
    processid = os.spawnvp(os.P_WAIT, "sudo", ["sudo", "reboot"])
    if processid:
      print "restart failed"
    pass

  def on_changeLanguageButton_clicked(self, button):
    pass



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

    #
    #  load main screen
    #

    self.builder = gtk.Builder()
#   self.builder.set_translation_domain('machine')
    self.builder.add_from_file("manual_test.glade")

    settings = gtk.settings_get_default()
    settings.set_string_property("gtk-font-name", "Sans 14", "")

    # settings = gtk.settings_get_default()
    settings.props.gtk_button_images = True

    self.builder.connect_signals(self)
    self.window1 = self.builder.get_object("window1")

    # to set vars
    # self.pollConnections()

#     if FINAL:
    # self.window1.fullscreen()
    self.window1.show()

    self.statusLabel = self.builder.get_object("statusLabel")

    self.listStore = None
    self.listView = self.builder.get_object("treeview1")

    self.currentProgramDisplayTree = self.builder.get_object("currentProgramDisplayTree")

#     self.xJogSpeed = self.builder.get_object("xJogSpeed")
#     self.yJogSpeed = self.builder.get_object("yJogSpeed")

    self.cycleToggle = self.builder.get_object("cycleToggle")
    self.tubeStopToggle = self.builder.get_object("tubeStopToggle")

    # set size of jog buttons
    # using large height
    jogButtons = self.builder.get_object("jogButtonBox")
    for item in jogButtons:
      if type(item) == gtk.Button or type(item) == gladevcp.HAL_Button:
        # print "Button : %s " % item.get_label()
        item.set_size_request(225, largeButtonHeight)

    airJogButtons = self.builder.get_object("airControlButtons")
    for item in airJogButtons:
      if type(item) == gtk.Button or type(item) == gladevcp.HAL_ToggleButton:
        item.set_size_request(200, largeButtonHeight)

    hydraulicControlButtons = self.builder.get_object("hydraulicControlButtons")
    for item in hydraulicControlButtons:
      if type(item) == gtk.Button or type(item) == gladevcp.HAL_RadioButton or type(item) == gladevcp.HAL_ToggleButton:
        item.set_size_request(200, largeButtonHeight)


    # # other buttons 'medium'
#     programStoreButtons = self.builder.get_object("programStoreButtons")
#     for item in programStoreButtons:
#       if type(item) == gtk.Button:
#         item.set_size_request(200, mediumButtonHeight)
#
#     programDialogButtons = self.builder.get_object("programDialogButtons")
#     for item in programDialogButtons:
#       if type(item) == gtk.Button:
#         item.set_size_request(200, mediumButtonHeight)

    machineControlButtons = self.builder.get_object("machineControlButtons")
    for item in machineControlButtons:
      if type(item) == gtk.Button:
        item.set_size_request(200, mediumButtonHeight)

#     autoButtons = self.builder.get_object("autoButtons")
#     for item in autoButtons:
#       if type(item) == gtk.Button:
#         item.set_size_request(200, mediumButtonHeight)

    #
    # load program edit dialog
    #
    self.builder2 = gtk.Builder()
    self.builder2.add_from_file("programEditDialog.glade")
    self.builder2.connect_signals(self)

    self.programDialog = self.builder2.get_object("programEditDialog")
    self.programEditTree = self.builder2.get_object("currentProgramEditTree")
    self.programEditListStore = self.builder2.get_object("currentProgramListStore")

    # use the edit store
    self.currentProgramDisplayTree.set_model(self.programEditListStore)

  def initKeyboard(self):
    self.keyb = touchKeyboard()
    self.keyb.getOKButton().connect("clicked", self.on_entryOK_clicked)

  def connectHalPins(self):
    # connect the new pins to the system
    postgui_halfile = "/home/user/installation/hmi.hal"
    processid = os.spawnvp(os.P_WAIT, "halcmd", ["halcmd", "-f", postgui_halfile])

    machineName = "ioMachine"
    hmiName = "hmi"

    for counter in range(10):
      operationPin = "operationType-%s" % counter
      positionPin = "position-%s" % counter

      command1 = []
      command1.append('halcmd')
      command1.append('net')
      command1.append(operationPin)
      command1.append(machineName + '.' + operationPin)
      command1.append(hmiName + '.' + operationPin)
      # print command1
      processid = os.spawnvp(os.P_WAIT, "halcmd", command1)

      command2 = []
      command2.append('halcmd')
      command2.append('net')
      command2.append(positionPin)
      command2.append(machineName + '.' + positionPin)
      command2.append(hmiName + '.' + positionPin)
      # print command2
      processid = os.spawnvp(os.P_WAIT, "halcmd", command2)



  def fillLists(self):
    self.buildProgramList()
    self.currentProgram.fillListStore(self.currentProgramStore)
    pass

  def loadMovesToHalPins(self):

#     for counter in range(10):
#       print "operation is"
#       print self.currentProgram.getOperation(counter).getOperation()
#       operationPins[counter] =

    for counter in range(10):
      operationPin = "operationType-%s" % counter
      positionPin = "position-%s" % counter
      h[operationPin] = self.currentProgram.getOperation(counter).getOperation()
      h[positionPin] = self.currentProgram.getOperation(counter).getPosition()


  def __init__(self):



    self.verbose = True

    self.initGui()
    self.initKeyboard()

    # check for hal
    if h:
      # print "-------------------------------------------"
      # printHalPins()
      # print "-------------------------------------------"
      # panel = gladevcp.makepins.GladePanel(h, "gui1.glade", self.builder, None)
      panel = gladevcp.makepins.GladePanel(h, "manual_test.glade", self.builder, None)
      h.ready()
      self.connectHalPins()

    self.currentProgram = ioProgram()

    self.loadMovesToHalPins()

#    self.s = storable()
#    self.s.loadState()

#    self.programs = self.s.getPrograms()
#    self.setCurrent(self.s.currentIndex)

    # go through programs and update if needed in case a new parameter
#    for program in self.programs:
#      self.currentProgramStore.clear()
#      program.fillListStore(self.currentProgramStore)
#      program.updateFromlistStore(self.currentProgramStore)

#    self.buildProgramList()


    # load the current program
#    self.createProgram()
#    self.loadMotionControlProgram()
#    self.loadCurrent()

    # fill the list store based on the current program
#   self.currentProgram.fillListStore(self.currentProgramStore)
    # self.fillLists()

    # udpate display and button states, polling  etc
    gobject.timeout_add(110, self.cyclicUpdate)



class programEdit(object):

  def __init__(self):
    pass

  def loadGlade(self):
    pass


def printHalPins():
  # res = os.spawnvp(os.P_WAIT, "halcmd", ["halcmd", "-i", vars.emcini.get(), "-f", postgui_halfile])
  processid = os.spawnvp(os.P_WAIT, "halcmd", ["halcmd", "show", "pin", "hmi"])
  if processid:
    raise SystemExit, processid



if __name__ == "__main__":
  try:
    h = hal.component("hmi")

    h.newpin("requestManual", hal.HAL_BIT, hal.HAL_OUT)
    h.newpin("currentState", hal.HAL_U32, hal.HAL_IN)
    h.newpin("requestState", hal.HAL_S32, hal.HAL_IO)
    h.newpin("stateLocked", hal.HAL_BIT, hal.HAL_IN)

#     h.newPin("iAxisPosition", hal.HAL_FLOAT, hal.HAL_IN)
#     h.newPin("oAxisPosition", hal.HAL_FLOAT, hal.HAL_IN)

    # communication between state machine
    # h.newpin("cycleStatus", hal.HAL_U32, hal.HAL_IO)

    for counter in range(10):
      operationPin = "operationType-%s" % counter
      positionPin = "position-%s" % counter
      h.newpin(operationPin, hal.HAL_S32, hal.HAL_OUT)
      h.newpin(positionPin, hal.HAL_FLOAT, hal.HAL_OUT)



  except:
    print "hal exception"

  try:
    app = hmi()
    gtk.main()
  except KeyboardInterrupt:
    raise SystemExit

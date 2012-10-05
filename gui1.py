#!/usr/bin/env python

import pygtk
pygtk.require("2.0")
import gobject
import gtk
import gladevcp.makepins
from gladevcp.gladebuilder import GladeBuilder
import threading
import time
import hal
import emc
import os

import gettext
import locale

APPLICATION_DOMAIN = 'machine'

locale.setlocale(locale.LC_ALL, "fi_FI.utf8")
locale.bindtextdomain(APPLICATION_DOMAIN, './locale')

lang1 = gettext.NullTranslations()
lang2 = gettext.translation(APPLICATION_DOMAIN, localedir='./locale', languages=['fi'], fallback=True)

lang2.install()

class motionControlProgram():
   

  def __init__(self):
    print "init motionControlProgram"

    # these are the default values
#    self.program = [(_('Program Name'), 'default_program'), \
#                    (_('Start Position X'), 25), \
#                    (_('start Position Y'), 0), \
#                    (_('Position To Tube Y'), 0), \
#                    (_('Position To Tube Feed'), 250), \
#                    (_('Forming Position Y'), 0), \
#                    (_('Forming Feed'), 50), \
#                    (_('Forming Dwell'), 1), \
#                    (_('Tube Stop Position X'), 25), \
#                    (_('Tube Stop Position Y'), 5) ]



     

#    self.program = [(_('Program Name'), 'default_program'), \
#                    (_('Forming Start Position X'), 90), \
#                    (_('Forming Start Position Y'), 0), \
#                    (_('Position To Tube Y'), 0), \
#                    (_('Position To Tube Feed'), 250), \
#                    (_('Forming Position Y'), 0), \
#                    (_('Forming Feed'), 50), \
#                    (_('Forming Dwell'), 1), \
#                    (_('Tube Stop Position X'), 25), \
#                    (_('Tube Stop Position Y'), 5) ]

    self.program = [_('Default Program'),
                    90,
                    0,
                    0,
                    250,
                    0,
                    50,
                    1,
                    25,
                    5]

    print self.program

    
#  def getListStore(self):    
#    
#    listStore = gtk.ListStore(gobject.TYPE_STRING, gobject.TYPE_STRING)
#
#    self.fillListStore(listStore)
#
#    return listStore
#    #print self.program
    
  def fillListStore(self, listStore):
#    #for i, key in enumerate(self.program):        
#    for i in range(len(self.program)):
#      #print "fill liststore: %s" % key
#      #listStore.append([ key[0], key[1] ])
#      listStore.append( [ parameters[i], self.program[i]] )
        
    counter = 0
    for item in self.program:
    
      listStore.append( [ parameters[counter], item] )
      counter += 1


  

class hmi(object):
    
  #
  #  utility functions
  #

  # load created text program into emc
  def loadMotionControlProgram(self):
    if self.command:
      self.command.mode(emc.MODE_MDI)
      self.command.wait_complete()
      self.command.mode(emc.MODE_AUTO)
      self.command.wait_complete()
      if self.verbose:
          print "LOAD: Done state prepare"
      self.command.program_open("/tmp/MotionProgram.ngc")
      
      self.builder.get_object("hal_gremlin1").load("/tmp/MotionProgram.ngc")
         
      if self.verbose:
          print "LOAD: Done Load command issue"
      

  def createProgram(self):

#    programName = self.currentProgram[0][1]
#    startPositonX = float(self.currentProgram[1][1])
#    startPositonY = float(self.currentProgram[2][1])
#    positionToTubeY = float(self.currentProgram[3][1])
#    positionToTubeFeed = float(self.currentProgram[4][1])                               
#    formingPositionY = float(self.currentProgram[5][1])
#    formingFeed = float(self.currentProgram[6][1])
#    formingDwell = float(self.currentProgram[7][1])
#    tubeStopPositionX = float(self.currentProgram[8][1])
#    tubeStopPositionY = float(self.currentProgram[9][1])

    programName = self.currentProgram.program[0]
    startPositionX = float(self.currentProgram.program[1])
    startPositionY = float(self.currentProgram.program[2])
    positionToTubeY = float(self.currentProgram.program[3])
    positionToTubeFeed = float(self.currentProgram.program[4])                               
    formingPositionY = float(self.currentProgram.program[5])
    formingFeed = float(self.currentProgram.program[6])
    formingDwell = float(self.currentProgram.program[7])
    tubeStopPositionX = float(self.currentProgram.program[8])
    tubeStopPositionY = float(self.currentProgram.program[9])

    # logic checking
    if startPositionY > positionToTubeY:
        startPositionY = 0
        
    if positionToTubeY > formingPositionY:
        positionToTubeY = 0

    


    programString = ""
    programString += "; program for %s\n" % (programName)
    programString += ";rapid to safe position\n"
    programString += "G0 Y0\n"
    programString += "G0 X100\n"

    programString += "G1 X %2.2f Y %2.2f F1000\n" % (startPositionX, startPositionY)
    programString += "M3 S200\n"

    programString += "G1 Y %2.2f F %2.2f \n" % (positionToTubeY, positionToTubeFeed)
    programString += "G1 Y %2.2f F %2.2f \n" % (formingPositionY, formingFeed)
    programString += "G4 P %2.2f \n" % (formingDwell)

    programString += "G1 X %2.2f Y %2.2f F1000\n" % (startPositionX, startPositionY)
    programString += "M4 S200\n "
    programString += "G1 X %2.2f Y %2.2f F1000\n" % (tubeStopPositionX, tubeStopPositionY)
    programString += "M30\n"
    
    #programString += "G1 X %2.2f Y %2.2f F1000\n" % (startPositonX, startPositonY)

    f = open('/tmp/MotionProgram.ngc', 'w')
    f.write(programString)
    f.close()
    
    print "*****************************"
    print "Written program"
    print programString
    print "*****************************"

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

#  def on_changeScreenButton_button_press_event(self, widget, data=None):
#    print "on_changeScreenButton_button_press_event"
#    if self.window1:
#      self.window1.show()

  def on_viceOpenToggle_toggled(self, widget, data=None):
    print "on_viceOpenToggle_toggled"
    if widget.get_active:
      print "widget is active"
    else:
      print "widget is not active"


    if self.viceCloseToggle:
      if self.viceOpenToggle.get_active():
        self.viceCloseToggle.set_active(False)
    else:
      print "no viceCloseToggle"

    
  def on_viceCloseToggle_toggled(self, widget, data=None):
    print "on_viceCloseToggle_toggled"
    if self.viceOpenToggle:
      if self.viceCloseToggle.get_active():
        self.viceOpenToggle.set_active(False)
    else:
      print "no viceOpenToggle"

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


  def jogAxis(self, axis, velocity):
    if self.command and self.status:
      self.status.poll()
      if self.status.task_mode == emc.MODE_MANUAL:
        if velocity == 0:
          self.command.jog(emc.JOG_STOP, axis)
        else:
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

  def pollConnections(self):
    self.currentStateString = states[h['currentState']]
     
    if self.currentStateString == "MANUAL":
      print "current state is manual; set sensitivity appropriately"
    elif self.currentStateString in cycleStates:
      print "current state is inCycle"
    else:
      pass
      #print "either in standby or in ready"

    return True

  def setNonAutoPagesInactive(self):
    notebook = self.builder.get_object("notebook1")
    
    for pageNumber in [1,2,3]:
      page = notebook.get_nth_page(pageNumber)
      if page:
        page.set_sensitive(False)
    
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
        h['manualRequest'] = 0
    elif page_num == 1:
        h['manualRequest'] = 1
        
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

  def on_newprogrambutton_released(self, widget):
    #createProgram
    self.programs.append()

  #
  #  auto screen callbacks
  #
  def on_editProgram_clicked(self, button):
    #load the current program into the dialog's liststore
    
    
    
    self.editCurrent()  

    
  # update the dynamic elements on the screens
  def updateControls(self):
    currentLabelText = _("Current Program: ")
    currentLabelText += self.currentProgram.program[0]
    
    self.builder.get_object("currentProgramLabel").set_text(currentLabelText)
    self.builder.get_object("currentProgramLabel1").set_text(currentLabelText)
    
    #print self.currentProgram[0][1]

    # update the position display
    if self.status:
      self.status.poll()
      positionText = 'Z: % 2.2f X: % 2.2f' % (self.status.actual_position[0], self.status.actual_position[1])

      self.positionLabel = self.builder.get_object("positionLabel1")
      if self.positionLabel:
        self.positionLabel.set_text(positionText)

    # update current state    
    label = self.builder.get_object("stateLabel")
    if states[h['currentState']] and label:
      label.set_text(self.stateMachine.currentState)
    elif label:
      label.set_text("cannot get machine state")

    # TODO: Read if jog OK
    if True:
      jogButtonBox = self.builder.get_object("jogButtonBox")
      if jogButtonBox:
        jogButtonBox.set_sensitive(False)

    return True

  #
  #  program save/load management 
  #

  def editCurrent(self):
      
    # clear the list store in the dialog 
    self.programListStore.clear()
    
    
    # copy the data over to fill the editor   
    self.currentProgram.fillListStore(self.programListStore)

    self.programDialog.present()
    self.programDialog.fullscreen()

  def on_newProgramButton_clicked(self, button):
    
    # add a copy of the current program
    print "New Program"
    print "current length %s" % len(self.programs)
    self.programs.append(self.currentProgram)
    
    print "new length %s" % len(self.programs)
    self.currentProgram = self.programs[len(self.programs)-1]
      
    self.buildProgramList()
    
    self.editCurrent()
    #self.on_editProgram_clicked(button)

  def on_loadProgramButton_clicked(self, button):
    # TODO: Check if we have 'saved' the current program
    
    # get the reference of the current selected program in the program tree view
    cursor = self.builder.get_object("treeview1").get_cursor()
    print self.programs[cursor[0][0]]

    # copy data into current program
    self.currentProgram = self.programs[cursor[0][0]]
    
    # load data into motion control etc
    self.createProgram()
    self.loadMotionControlProgram()

  #
  #  System screen callbacks
  #
  def on_changeLanguageButton_clicked(self, button):
    #on_changeLanguageButton_clicked
    print "change language button clicked"
    lang1.install()

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
    print "accept edited program"  
    
#    for item in self.listStore:
#        print item
    #self.currentProgram = []
    
    # copy the values from the list store back into the 
    # current program array 
    for i, item in enumerate(self.programListStore):
        print "transfer: %s" % [item[0], item[1]]
        self.currentProgram.program[i] = item[1]
        #self.currentProgram.append(item[1])

    
    print "current program is now:"
    for line in self.currentProgram.program: 
        print line

    # create ngc file, load to motion, update gremlin, 'close' window    
    self.createProgram()
    self.loadMotionControlProgram()
    self.builder.get_object("hal_gremlin1").expose()        
    self.programDialog.iconify()
    self.buildProgramList()
    

  def on_editing_started(self, cellrenderer, editable, path, user_param1=None):
    print "on editing started"
    #self.builder.get_object("")
    
    self.numKeyWindow.present()
    self.numKeyWindow.fullscreen()
    # store the row we are editing
    self.editingPath = path
    

  #
  #  methods for the on screen keyboard
  #
  
  def on_keyboard_button_press(self, button):
    text = button.get_label()
    print "button %s pressed" % text
    
    currentText = self.entryNumeric.get_text()
    
    if text == '-' and len(currentText) > 0:
        return
    
    if text == '.' and currentText.count('.') > 0:
        return
    
    self.entryNumeric.set_text(currentText + text)
  
  def on_entryOK_clicked(self, button):
    #self.builder.get_object("")
    inputText = self.entryNumeric.get_text()
    
#    if inputText.isdigit():
#        print "is digit"
        
    self.programListStore[self.editingPath][1] = inputText
    #self.numKeyWindow.hide()   
    self.entryNumeric.set_text("")
    self.numKeyWindow.iconify()
    
  def on_entryCancel_clicked(self, button):
    self.entryNumeric.set_text("")
    self.numKeyWindow.iconify()

  #
  #  init etc...
  #

  def buildProgramList(self):
    # look up the name of the program from the store and
    # add to the liststore
    self.listStore.clear()
    print "**** Build Program List ****"
    for entry in self.programs:
        print entry
        print entry.program[0] 
        self.listStore.append([entry.program[0]])
    


  def initGui(self):
    self.builder = gtk.Builder()
    self.builder.set_translation_domain('machine')
    self.builder.add_from_file("gui1.glade")

    settings = gtk.settings_get_default()
    settings.set_string_property("gtk-font-name", "Sans 16", "")

    self.builder.connect_signals(self)
    self.window1 = self.builder.get_object("window1")
    
    #self.window1.fullscreen()
    self.window1.show()

    #self.builder.get_object("window2").show()

    self.manualWindow = self.builder.get_object("manual")
    #self.manualWindow.show()
    #self.manualWindow.fullscreen()

    self.viceCloseToggle = self.builder.get_object("viceCloseToggle")
    self.viceOpenToggle = self.builder.get_object("viceOpenToggle")
    #self.positionLabel = self.builder.get_object("positionLabel")

    # self.widget = self.builder.get_object("toggleButton1")
    # self.widget.get_settings().set_string_property('gtk-font-name', 'sans normal 9','')



#    self.scrolledWindow = self.builder.get_object("scrolledwindow1")
#    if not self.scrolledWindow:
#      print "no scrolledwindow"

    self.listStore = self.builder.get_object("liststore1")
    if not self.listStore:
      print "no listStore"

    # treeView = gtk.TreeView(self.listStore)
    # #treeView.connect("row-activated", self.on_activated)
    # treeView.set_rules_hint(True)
    # self.scrolledWindow.add(treeView)
    self.listView = self.builder.get_object("treeview1")
    if not self.listView:
      print "no listView/treeview1"

    self.programDialog = self.builder.get_object("programeditdialog")    
    self.programTreeView = self.builder.get_object("treeview2")
    self.programListStore = self.builder.get_object("liststore2")
    self.programListStore.clear()
    
    #self.motionTester.fillListStore(self.programListStore)    

    #self.programDialog.show()

  
  def initNumericKeyboard(self):
    print ""
    self.numKeyWindow = self.builder.get_object("numericKey")
    self.entryNumeric = self.builder.get_object("entry-numeric")
    
    buttons = range(10)
    buttons.append("minus")
    buttons.append("dot")
    #print buttons
    
    for button in buttons:
      string = "button-%s" % button 
      #print string 
      item = self.builder.get_object(string)
      item.connect("clicked", self.on_keyboard_button_press)
    
    self.entryNumeric.set_text("")
    #self.numKeyWindow.show()    
  
  def __init__(self, stateMachine=None):

    #self.FINAL = False
    self.verbose = True
    
    # create a test program
#    self.motionTester = motionControlProgram()
#    print self.motionTester

    # setup gtk elements
    self.initGui()
    self.initNumericKeyboard()

    # create store for all programs on the 'hmi'
    self.programs = []
    
    # TODO: Load the 'programs' in from file...
    # we'll just make some up for now....
#    self.programs.append(self.motionTester())
#    self.programs.append(self.motionTester())
#    self.programs.append(self.motionTester())
#    self.programs.append(self.motionTester())
    self.programs.append(motionControlProgram())
    self.programs.append(motionControlProgram())
    self.programs.append(motionControlProgram())
    self.programs.append(motionControlProgram())

    # create a new liststore and overwrite current in treeview
    self.listStore = gtk.ListStore(gobject.TYPE_STRING)
    self.listView.set_model(self.listStore)

    self.buildProgramList()

    # load the first program as the current...
    # TODO: save the last used program 
    self.currentProgram = self.programs[0]
    self.currentProgramIndex = 0
    
    # fill the list store based on the current program
    self.currentProgram.fillListStore(self.programListStore)    

    # udpate display and button states, polling  etc
    gobject.timeout_add(150, self.updateControls)
    gobject.timeout_add(150, self.pollConnections)

    # linuxcnc stuff....
    
    self.command = emc.command()
    self.status = emc.stat()
    
    # TODO: 
    #self.createProgram()
    
    # check for hal
    #if h:
      #print "-------------------------------------------"
      #printHalPins()
      #print "-------------------------------------------"
      #panel = gladevcp.makepins.GladePanel(h, "gui1.glade", self.builder, None)
      #h.ready()
      

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
            "STARTSPINDLE",
            "CYCLE",
            "OPENVICE",
            "MANUAL"]

stateText = [   _("Standby"),
                _("Ready"),
                _("Close Vice"),
                _("Start Spindle"),
                _("Cycle"),
                _("Open Vice"),
                _("Manual"),
                _("Cycle Aborted")]

stateTextVerbose = [    _("Standby - Press start"),
                        _("Ready - Hold control for cycle"),
                        _("Close Vice - Hold control to close vice"),
                        _("Start Spindle"),
                        _("Cycle - Forming tube"),
                        _("Open Vice - Hold control to open vice"),
                        _("Manual"),
                        _("Cycle Aborted")]

# when we are in any of these states we are in a cycle
cycleStates = [ "CLOSEVICE",
                "STARTSPINDLE",
                "CYCLE",
                "OPENVICE"]

parameters = [ _('Program Name'),
               _('Forming Start Position X'),
               _('Forming Start Position Y'),
               _('Position To Tube Y'),
               _('Position To Tube Feed'),
               _('Forming Position Y'),
               _('Forming Feed'),
               _('Forming Dwell'),
               _('Tube Stop Position X'),
               _('Tube Stop Position Y')]

def printHalPins():
  #res = os.spawnvp(os.P_WAIT, "halcmd", ["halcmd", "-i", vars.emcini.get(), "-f", postgui_halfile])  
  processid = os.spawnvp(os.P_WAIT, "halcmd", ["halcmd", "show", "pin", "hmi"])
  if processid:
    raise SystemExit, processid

def connectHalPins():
  #connect the new pins to the system
  processid = os.spawnvp(os.P_WAIT, "halcmd", ["halcmd", "-f", "hmi.hal"])    
    

try:
  h = hal.component("hmi")
  h.newpin("mcb1", hal.HAL_BIT, hal.HAL_IN)
  h.newpin("currentState", hal.HAL_U32, hal.HAL_IN)
  
  h.newpin("stateRequest", hal.HAL_U32, hal.HAL_OUT)
  h.newpin("manualRequest", hal.HAL_BIT, hal.HAL_OUT)
  h.ready()
except:
  print "hal exception"




if __name__ == "__main__":
  try:    
    app = hmi()
    gtk.main()
    connectHalPins()
  except KeyboardInterrupt:
    raise SystemExit

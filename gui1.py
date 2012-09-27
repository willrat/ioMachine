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

class hmi(object):

  def on_window1_destroy(self, widget, data=None):
    print "on_window1_destroy"
    gtk.main_quit()

  def on_manual_destroy(self, widget, data=None):
    print "on_window1_destroy"
    gtk.main_quit()

  def on_gtk_quit_activate(self, menuitem, data=None):
    print "quit from menu"
    gtk.main_quit()

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

  def on_changeScreenButton_button_press_event(self, widget, data=None):
    print "on_changeScreenButton_button_press_event"
    if self.window1:
      self.window1.show()

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

  def on_notebook1_select_page(self, notebook, page, page_num, data=None):
    print "call back"

  def on_notebook1_switch_page(self, notebook, page, page_num, data=None):
    print "switch page call back"
    print "page number %s" % page_num

    if page_num == 0:
      print "auto mode"
    elif page_num == 1:
      print "manual"
    elif page_num == 2:

  def updatePositonReadout(self):
    if self.status:
      self.status.poll()
      #positionText = 'Z: {0} X: {1}'.format(self.status.actual_position[0], self.status.actual_position[1])
      positionText = 'Z: % 2.2f X: % 2.2f' % (self.status.actual_position[0], self.status.actual_position[1])
      # data = self.status.actual_position[0]
      # text1 = "% 2.2f"% (data)
      # data = self.status.actual_position[1]
      # text2 = "% 2.2f"% (data)
      #self.builder.get_object("dro_x").set_text(text)
      #
      self.positionLabel = self.builder.get_object("positionLabel1")
      if self.positionLabel:
        self.positionLabel.set_text(positionText)

    label = self.builder.get_object("stateLabel")

    # if self.stateMachine and label:
    #   label.set_text(self.stateMachine.currentState)
    # elif label:
    #   label.set_text("cannot get machine state")

    return True

  def on_manual_show(self, widget, data=None):
    print "on manualWindow show"

  # def theEnd(self):
  #   gtk.main_quit()
  #   self.positionUpdateThread.cancel()



# enum states {   STATE_STANDBY = 0,
#                 STATE_READY,
#                 STATE_CLOSEVICE,
#                 STATE_STARTSPINDLE,
#                 STATE_CYCLE,
#                 STATE_OPENVICE,
#                 STATE_MANUAL,
#                 MAX_STATES }; //current_state;

  # must match order as above
  states = [  "READY",
              "STANDBY",
              "CLOSEVICE",
              "MANUAL",
              "STARTSPINDLE",
              "CYCLE",
              "OPENVICE",
              "MANUAL"]

  #def __init__(self, halComponent=None, stateMachine=None):
  def __init__(self, stateMachine=None):
    self.builder = gtk.Builder()
    self.builder.add_from_file("gui1.glade")

    # hal stuff
    # if not halComponent:      
    #   halComponent = hal.component("gui01")
    # else:
    #   panel = gladevcp.makepins.GladePanel( halComponent, "gui1.glade", self.builder, None)
    #   halComponent.ready()


    settings = gtk.settings_get_default()
    settings.set_string_property("gtk-font-name", "Sans 18", "")

    self.builder.connect_signals(self)
    self.window1 = self.builder.get_object("window1")
    #self.window1.fullscreen()
    self.window1.show()

    self.manualWindow = self.builder.get_object("manual")
    #self.manualWindow.show()
    #self.manualWindow.fullscreen()

    self.viceCloseToggle = self.builder.get_object("viceCloseToggle")
    self.viceOpenToggle = self.builder.get_object("viceOpenToggle")
    #self.positionLabel = self.builder.get_object("positionLabel")

    # self.widget = self.builder.get_object("toggleButton1")
    # self.widget.get_settings().set_string_property('gtk-font-name', 'sans normal 9','')

    self.command = emc.command()
    self.status = emc.stat()

    # udpate positon readout
    gobject.timeout_add(100, self.updatePositonReadout) 

    # thread to udpate positon readout in realtime
    # self.positionUpdateThread = UpdateLabel(self)
    # self.positionUpdateThread.start()

    # #
    # if stateMachine:
    #   self.stateMachine = stateMachine

    # h = hal.component("hmi")
    print "-------------------------------------------"
    printHalPins()
    print "-------------------------------------------"
    panel = gladevcp.makepins.GladePanel( h, "gui1.glade", self.builder, None)
    # h.ready()
    



def printHalPins():
  #res = os.spawnvp(os.P_WAIT, "halcmd", ["halcmd", "-i", vars.emcini.get(), "-f", postgui_halfile])
  #connect the new pins to the system
  processid = os.spawnvp(os.P_WAIT, "halcmd", ["halcmd", "show", "pin", "hmi"])
  if processid:
    raise SystemExit, processid

# class UpdateLabel(threading.Thread):
#   def __init__(self, gui):
#     threading.Thread.__init__(self)
#     self.gui = gui

#   def run(self):
#     while 1:
#       time.sleep(0.05)
#       if self.gui:
#         self.gui.updatePositonReadout()



if __name__ == "__main__":
  try:
    h = hal.component("hmi")
    h.newpin("mcb1", hal.HAL_BIT, hal.HAL_IN)
    h.newpin("stateRequest", hal.HAL_U32, hal.HAL_OUT)

    h.ready()

    printHalPins()

    app = hmi()
    gtk.main()

  except KeyboardInterrupt:
    raise SystemExit


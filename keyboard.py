#!/usr/bin/env python

import pygtk
pygtk.require("2.0")
import gobject
import gtk

class theApp():
  def __init__(self, stateMachine=None):
    self.builder = gtk.Builder()
    self.builder.add_from_file("keyboard.glade")
        
    settings = gtk.settings_get_default()
    settings.set_string_property("gtk-font-name", "Sans 24", "")
    
    self.builder.connect_signals(self)
    self.window1 = self.builder.get_object("window1")
    #self.window1.fullscreen()
    self.window1.show()
    
    #self.builder.get_object("window2").show()

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

app = theApp()
gtk.main()
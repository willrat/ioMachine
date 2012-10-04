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

app = theApp()
gtk.main()
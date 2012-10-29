#!/usr/bin/env python

import pygtk
pygtk.require("2.0")
import gobject
import gtk

class touchKeyboard():
  def __init__(self, stateMachine=None):
    self.builder = gtk.Builder()
    self.builder.add_from_file("keyboard.glade")
    
    self.builder.connect_signals(self)
    self.window1 = self.builder.get_object("window1")
    self.window1.fullscreen()
    self.window1.show()
    
    self.inputString = ""
    
    self.entry = self.builder.get_object("entry1")
    self.pLabel = self.builder.get_object("label1")
    
    #these are the key press buttons
    self.buttons = []
    self.builder.get_object("spaceBar").set_label(" ")
    self._findButtons()
    
    self.builder.get_object("okButton").set_size_request(240, 80)
#    item.set_size_request(80, 80)
    self.builder.get_object("closeButton").set_size_request(240, 80)
#    item.set_size_request(80, 80)
    self.builder.get_object("spaceBar").set_size_request(480, 80)
#    self.builder.get_object()
    
    self.closeButton = self.builder.get_object("closeButton")
    self.closeButton.set_size_request(200,80)  

    self.isNumericOnly = False
    
    self.reset()
    self.iconifyHide()
#    for i in self.buttons:
#      try:
#        print i.get_label()
#      except:
#        print "ASSERT: NOT A BUTTON"
  
  def _findButtons(self):
    #get all the objects in the gui
    objects = self.builder.get_objects()
    
    # go through them
    for item in objects:
      if type(item) == gtk.Button:
        print item.get_label()
        item.set_size_request(75, 75)
        
        # connect any character buttons        
        if (len((str)(item.get_label())) <= 1 ):
          print "added"
          self.buttons.append(item)
          item.connect("clicked", self.on_keyboard_button_press)
          
  
  def getOKButton(self):
    return self.builder.get_object("okButton")
  
  def getWindow(self):
    return self.window1
  
  def reset(self):
    #self.window1.iconify()
    self.setFullKeyboard()
    self.clear()
    self.setParameterLabel("")    
  
  def clear(self):
    self.entry.set_text("")
    
  def getString(self):
    return self.entry.get_text()
  
  def setString(self, string):
    self.entry.set_text(string)
  
  def setParameterLabel(self, string):
    self.pLabel.set_label(string)
    pass

  def setNumericOnly(self):
    self.setNumeric(True)
    
  def setNumeric(self, isNumeric=True):
    self.isNumericOnly = isNumeric
    
    for item in self.buttons:
      label = item.get_label()
      
      if (str)(label).isdigit() or label == "-" or label == ".":
        pass
      else:
        item.set_sensitive(not isNumeric)

  def setFullKeyboard(self):
    self.isNumericOnly = False
    for item in self.buttons:
      item.set_sensitive(True)

  def iconifyHide(self):
    self.window1.iconify()

  #
  # callbacks...
  #

  def on_keyboard_button_press(self, button):
    text = button.get_label()
    print "button %s pressed" % text
    
    currentText = self.entry.get_text()
    
    if self.isNumericOnly:
      if text == '-' and len(currentText) > 0:
        return      
      if text == '.' and currentText.count('.') > 0:
        return
    
    self.entry.set_text(currentText + text)

  def on_okButton_clicked(self, button):
    self.iconifyHide()
  
  def on_closeButton_clicked(self, button):    
    self.iconifyHide()
  
  def on_backSpaceButton_clicked(self, button):
    current = self.entry.get_text()
    print current
    current = current[:-1]
    print "deleted: %s" % current
    self.entry.set_text(current)
    pass
  
  def on_clearButton_clicked(self, button):
    self.entry.set_text("")
    pass

if __name__ == "__main__":
  
  settings = gtk.settings_get_default()
  settings.set_string_property("gtk-font-name", "Sans 16", "")  
  app = touchKeyboard()
  app.setParameterLabel("PARAMETER ENTRY")  
  gtk.main()
  
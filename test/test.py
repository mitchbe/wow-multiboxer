#!/bin/python3
import wx

class MainWindow(wx.Frame):
    def __init__(self, parent, title):
        wx.Frame.__init__(self, parent, title=title, size=(200,100))
        self.panel =  wx.Panel(self, wx.ID_ANY)
        self.panel.Bind(wx.EVT_KEY_DOWN, self.KeyDown)
        self.panel.Bind(wx.EVT_KEY_UP, self.KeyDown)
        self.panel.Bind(wx.EVT_CHAR, self.KeyDown)
        self.panel.SetFocus()

    def KeyDown(self, event=None):
        print("key down" + chr(event.GetUnicodeKey()))

if __name__ == "__main__":
    app = wx.App(False)
    gui = MainWindow(None, "test")
    gui.Show()
    app.MainLoop()

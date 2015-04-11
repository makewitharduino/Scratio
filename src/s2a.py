# -*- coding: utf-8 -*-
from server import *
import serial.tools.list_ports
import wx
import json

class s2a:
    def __init__(self):
        self.oflg = 0
        self.port = ""
        self.getportlist()

    def getportlist(self):
        self.ports = []
        lists = list(serial.tools.list_ports.comports())
        for x in lists:
            self.ports.append(x[0])

        return self.ports

    def connectServer(self):
        self.server = server(8099)
        self.server.main()
        self.server.call_arduino(self.port)

    def click_button(self,event):
        if self.oflg == 0:
            self.connectServer()
            self.button.SetLabel(u'Connecting')
            self.oflg = 1
        else:
            self.server.close()
            self.button.SetLabel(u'Connect')
            self.oflg = 0

    def listbox_select(self,event):
        obj = event.GetEventObject()
        self.port = obj.GetStringSelection()

    def main(self):
        app = wx.App()
        frame = wx.Frame(None, wx.ID_ANY, u'S2A v0.1',size=(300,200))

        application = wx.App()

        panel = wx.Panel(frame,wx.ID_ANY)
        panel.SetBackgroundColour("#AFAFAF")

        s_text = wx.StaticText(panel,wx.ID_ANY,u'Serial Port')

        element_array = self.ports
        listbox = wx.ListBox(panel,wx.ID_ANY,choices=element_array,style=wx.LB_SINGLE)
        listbox.Bind(wx.EVT_LISTBOX,self.listbox_select)

        self.button = wx.Button(panel,wx.ID_ANY,u'Connect')
        self.button.Bind(wx.EVT_BUTTON,self.click_button)

        layout = wx.BoxSizer(wx.VERTICAL)
        layout.Add(s_text,flag=wx.GROW|wx.LEFT|wx.TOP,border=10)
        layout.Add(listbox,flag=wx.GROW|wx.ALL,border=10)
        layout.Add(self.button,flag=wx.GROW|wx.ALIGN_CENTER|wx.LEFT|wx.RIGHT|wx.BOTTOM,border=10)

        panel.SetSizer(layout)

        frame.Show()
        application.MainLoop()

    def close(self):
        self.server.close()
        self.oflg = 0

if __name__ == '__main__':
    s2a = s2a()
    s2a.main()

#Author: Chenyi Liu
#
#   reference :
#       wxPython http://www.wxpython.org/
#       google-chartwrapper http://code.google.com/p/google-chartwrapper/

import os
import wx

import twitterstream
import cal_sentiment

class UpperPanel(wx.Panel):
    def __init__(self, parent, id):
        wx.Panel.__init__(self, parent, id, style=wx.BORDER_SUNKEN)

        button1 = wx.Button(self, -1, 'go', (250, 30))
        self.Bind(wx.EVT_BUTTON, self.OnClick, id=button1.GetId())
        self.SetBackgroundColour("White")

        static = wx.StaticText(self, wx.NewId(), "Enter the screen name(without'@') of a twitter user to see when did he/she get emotional :",
                pos=(100, 10))

        self.textbox = wx.TextCtrl(self, wx.NewId(), "", size=(150, -1),
                pos=(100, 30))

    def OnClick(self, event):
        s=self.textbox.GetValue()
        if twitterstream.fetchsamples(s)==1:
        #    cal_sentiment.drawbarchart()
            cal_sentiment.lines("out.txt")


class LowerPanel(wx.Panel):

    def __init__(self, parent, id):

        wx.Panel.__init__(self, parent, id, style=wx.BORDER_SUNKEN)
        self.SetBackgroundColour("White")


        name=".\Images\\image.jpg"
        name0=".\Images\\0.png"
        name1=".\Images\\1.png"
        name2=".\Images\\2.png"

        static = wx.StaticText(self, wx.NewId(), "Having problems refreshing this panel! I have to show them in a browser.",
                pos=(200, 100))

        #bimg    =   wx.Image(name, wx.BITMAP_TYPE_ANY)
        #img0    =   wx.Image(name0, wx.BITMAP_TYPE_ANY)
        #sb1 = wx.StaticBitmap(self, -1, wx.BitmapFromImage(bimg),pos=(0,0))
        #sb2 = wx.StaticBitmap(self, -1, wx.BitmapFromImage(img0),pos=(10,10))


class MainFrame(wx.Frame):
    def __init__(self, parent, id, title):
        wx.Frame.__init__(self, parent, id, title, size=(800, 600))
        panel = wx.Panel(self, -1)
        self.Bind(wx.EVT_CLOSE, self.OnClose)
        self.lowerpanel = LowerPanel(panel, -1)
        upperpanel = UpperPanel(panel, -1)
        hbox = wx.BoxSizer(wx.VERTICAL)
        hbox.Add(upperpanel, 1, wx.EXPAND | wx.ALL, 0)
        hbox.Add(self.lowerpanel, 6, wx.EXPAND | wx.ALL, 0)
        panel.SetSizer(hbox)
        self.Centre()
        cal_sentiment.InitiatDictionary()

        self.Show(True)

    def OnClose(self, event):
        #cal_sentiment.clearIMGBuffer()
        #print cal_sentiment.filenames
        self.Destroy()

app = wx.PySimpleApp()
#frm = TestFrame(parent=None, id=-1)
#frm.Show()
MainFrame(None, -1, 'When do People Get Emotional? -- Chenyi Liu')
app.MainLoop()

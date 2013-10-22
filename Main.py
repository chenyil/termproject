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

        static1 = wx.StaticText(self, wx.NewId(), "Notice: Only 200 recent tweets of the user will be calculated",
                pos=(100, 60))
        static1 = wx.StaticText(self, wx.NewId(), "Score:high-happy,low-sad Emotional:high-emotional,low-calm ",pos=(100, 80))

    def OnClick(self, event):
        s=self.textbox.GetValue()
        if twitterstream.fetchsamples(s)==1:
        #    cal_sentiment.drawbarchart()
            cal_sentiment.clearBuffer()
            cal_sentiment.lines("out.txt")
        self.GetParent().GetParent().lowerpanel.repaint()

class LowerPanel(wx.Panel):

    def __init__(self, parent, id):

        wx.Panel.__init__(self, parent, id, style=wx.BORDER_SUNKEN)
        self.SetBackgroundColour("White")

    def repaint(self):
        static = wx.StaticText(self, wx.NewId(), "Please wait, it takes time to render images.",
                pos=(200, 10))
        name0=".\Images\\0.png"
        name1=".\Images\\1.png"
        name2=".\Images\\2.png"
        name3=".\Images\\3.png"
        name4=".\Images\\4.png"
        name5=".\Images\\5.png"
        img0    =   wx.Image(name0, wx.BITMAP_TYPE_ANY)
        img1    =   wx.Image(name1, wx.BITMAP_TYPE_ANY)
        img2    =   wx.Image(name2, wx.BITMAP_TYPE_ANY)
        img3    =   wx.Image(name3, wx.BITMAP_TYPE_ANY)
        img4    =   wx.Image(name4, wx.BITMAP_TYPE_ANY)
        img5    =   wx.Image(name5, wx.BITMAP_TYPE_ANY)

        sb0 = wx.StaticBitmap(self, wx.NewId(), wx.BitmapFromImage(img0),pos=(10,10))
        sb1 = wx.StaticBitmap(self, wx.NewId(), wx.BitmapFromImage(img1),pos=(10,210))
        sb2 = wx.StaticBitmap(self, wx.NewId(), wx.BitmapFromImage(img2),pos=(10,410))

        sb3 = wx.StaticBitmap(self, wx.NewId(), wx.BitmapFromImage(img3),pos=(610,10))
        sb4 = wx.StaticBitmap(self, wx.NewId(), wx.BitmapFromImage(img4),pos=(610,210))
        sb5 = wx.StaticBitmap(self, wx.NewId(), wx.BitmapFromImage(img5),pos=(610,410))

        #MainFrame.repaint(self)

class MainFrame(wx.Frame):
    def __init__(self, parent, id, title):
        wx.Frame.__init__(self, parent, id, title, size=(1200, 760))
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
    def repaint(self):
        print("MainFrame Repaint")
        self.Show(False)
        self.Show(True)

    def OnClose(self, event):
        cal_sentiment.clearIMGBuffer()
        #print cal_sentiment.filenames
        self.Destroy()

app = wx.PySimpleApp()
MainFrame(None, -1, 'When do People Get Emotional? -- Chenyi Liu')
app.MainLoop()

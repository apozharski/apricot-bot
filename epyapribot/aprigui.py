#!/usr/bin/env python

#import wxversion
#wxversion.ensureMinimal('2.8')
import wx
from gui.ABotFrame import ABotFrame
from abot import TheBot

class ABotGUI(ABotFrame):
    def SetRobot(self, robot):
        self.robot = robot
    def RobotReady(self):
        return self.robot is not None
    def wxBotConnect(self, event):
        self.SetRobot(TheBot(serport=self.choice_interfaces.GetStringSelection()))
        event.Skip()
    def wxXHome(self, event):
        if self.RobotReady():
            self.robot.xhome()
        event.Skip()

    def wxXMove(self, event):
        if self.RobotReady():
            self.robot.xgoto(self.x_slider.GetValue())
        event.Skip()

    def wxYHome(self, event):
        if self.RobotReady():
            self.robot.yhome()
        event.Skip()

    def wxYMove(self, event):
        if self.RobotReady():
            self.robot.ygoto(self.y_slider.GetValue())
        event.Skip()

    def wxZHome(self, event):
        if self.RobotReady():
            self.robot.zhome()
        event.Skip()

    def wxZMove(self, event):
        if self.RobotReady():
            self.robot.zgoto(self.z_slider.GetValue())
        event.Skip()

    def wxPHomeUp(self, event):
        if self.RobotReady():
            self.robot.phomeup()
        event.Skip()

    def wxPHomeDn(self, event):
        if self.RobotReady():
            self.robot.phomedn()
        event.Skip()

    def wxPMove(self, event):
        if self.RobotReady():
            self.robot.pgoto(self.p_slider.GetValue())
        event.Skip()


class ABotApp(wx.App):
    def OnInit(self):
        wx.InitAllImageHandlers()
        abotTopFrame = ABotGUI(None, -1, "")
        self.SetTopWindow(abotTopFrame)
        abotTopFrame.Show()
        return 1

if __name__ == "__main__":
    abot = ABotApp(0)
    abot.MainLoop()

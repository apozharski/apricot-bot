#!/usr/bin/env python

#import wxversion
#wxversion.ensureMinimal('2.8')
import wx
from gui.ABotFrame import ABotFrame
from abot import TheBot
from target import set_the_stage, name_template

class ABotGUI(ABotFrame):
    def __init__(self, *args, **kwds):
        ABotFrame.__init__(self, *args, **kwds)
        self.plates = {'robobase'  :   ['templates/apribot.apb', 0]}
        self.roboperator = self.SetRobOperator()
    def SetRobOperator(self, plates=None):
        plates = self.plates if plates is None else plates
        self.roboperator = set_the_stage(plates)
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
            self.robot.xgoto(self.spin_ctrl_x.GetValue())
        event.Skip()

    def wxYHome(self, event):
        if self.RobotReady():
            self.robot.yhome()
        event.Skip()

    def wxYMove(self, event):
        if self.RobotReady():
            self.robot.ygoto(self.spin_ctrl_y.GetValue())
        event.Skip()

    def wxZHome(self, event):
        if self.RobotReady():
            self.robot.zhome()
        event.Skip()

    def wxZMove(self, event):
        if self.RobotReady():
            self.robot.zgoto(self.spin_ctrl_z.GetValue())
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
            self.robot.pgoto(self.spin_ctrl_p.GetValue())
        event.Skip()

    def ImportSpot(self, spot, namectrl):
        dlg = wx.FileDialog(self, "Import spot %d template" % spot, "", "", "APB files (*.apb)|*.apb|All files (*.*)|*.*", wx.OPEN)
        try:
            if dlg.ShowModal() == wx.ID_OK:
                key = 'spot%d' % spot
                self.plates[key] = [dlg.GetPath(),spot]
                self.SetRobOperator()
                namectrl.SetValue(name_template(dlg.GetPath()))
            else:
                dlg.Destroy()
        finally:
            dlg.Destroy()

    def UpdateSpot(self, spot, namectrl):
        key = 'spot%d' % spot
        if key in self.plates:
            self.SetRobOperator()
            namectrl.SetValue(name_template(self.plates[key][0]))

    def wxImportSpot1(self, event):
        self.ImportSpot(1,self.text_ctrl_tspot1)
        event.Skip()

    def wxImportSpot2(self, event):
        self.ImportSpot(2,self.text_ctrl_tspot2)
        event.Skip()

    def wxImportSpot3(self, event):
        self.ImportSpot(3,self.text_ctrl_tspot3)
        event.Skip()

    def wxImportSpot4(self, event):
        self.ImportSpot(4,self.text_ctrl_tspot4)
        event.Skip()

    def wxUpdateSpot1(self, event):
        self.UpdateSpot(1,self.text_ctrl_tspot1)
        event.Skip()

    def wxUpdateSpot2(self, event):
        self.UpdateSpot(2,self.text_ctrl_tspot2)
        event.Skip()

    def wxUpdateSpot3(self, event):
        self.UpdateSpot(3,self.text_ctrl_tspot3)
        event.Skip()

    def wxUpdateSpot4(self, event):
        self.UpdateSpot(4,self.text_ctrl_tspot4)
        event.Skip()

    def GetKeyRCTvol(self):
        key = 'spot' + self.radio_box_op_spot.GetStringSelection()
        rct = [int(x.GetValue()) for x in [self.text_ctrl_op_row, self.text_ctrl_op_col, self.text_ctrl_op_tip]]
        vol = int(elf.text_ctrl_op_vol.GetValue())
        return key, rct, vol

    def wxOperateMove(self, event):
        key, rct = self.GetKeyRCTvol()[:2]
        self.roboperator.gotoRCT(key, rct)
        event.Skip()

    def wxOperateAspirate(self, event):
        key, rct, vol = self.GetKeyRCTvol()
        self.roboperator.aspirateRCT(key, rct, vol)
        event.Skip()

    def wxOperateDispense(self, event):
        key, rct, vol = self.GetKeyRCTvol()
        self.roboperator.dispenseRCT(key, rct, vol)
        event.Skip()

    def wxOperatePurge(self, event):
        key, rct = self.GetKeyRCTvol()[:2]
        self.roboperator.emptyRCT(key, rct)
        event.Skip()

    def wxOperateWash(self, event):
        key, rct, vol = self.GetKeyRCTvol()
        self.roboperator.washRCT(key, rct, vol)
        event.Skip()

    def wxOperateHome(self, event):
        self.roboperator.home()
        event.Skip()

class ABotApp(wx.App):
    def OnInit(self):
        abotTopFrame = ABotGUI(None, -1, "")
        self.SetTopWindow(abotTopFrame)
        abotTopFrame.Show()
        return 1

if __name__ == "__main__":
    abot = ABotApp(0)
    abot.MainLoop()

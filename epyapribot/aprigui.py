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
        self.robot = self.roboperator.get_the_bot()
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
        vol = int(self.text_ctrl_op_vol.GetValue())
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

    def wxStepDo(self, ax, v):
        if self.RobotReady():
            if ax == 'x':
                self.robot.xgoto(self.robot.get_x()+v)
                self.label_stepperX.SetLabel('X=%5d' % self.robot.get_x())
            if ax == 'y':
                self.robot.xgoto(self.robot.get_y+v)
                self.label_stepperY.SetLabel('Y=%5d' % self.robot.get_y())
            if ax == 'z':
                self.robot.xgoto(self.robot.get_z+v)
                self.label_stepperZ.SetLabel('Z=%5d' % self.robot.get_z())
            if ax == 'v':
                self.robot.xgoto(self.robot.get_v+v)
                self.label_stepperV.SetLabel('V=%5d' % self.robot.get_v())

    def onStepXm(self, event):
        self.wxStepDo('x',-int(self.choice_xm.GetStringSelection()))
        event.Skip()

    def onStepXm1000(self, event):
        self.wxStepDo('x',-1000)
        event.Skip()

    def onStepXm100(self, event):
        self.wxStepDo('x',-100)
        event.Skip()

    def onStepXm10(self, event):
        self.wxStepDo('x',-10)
        event.Skip()

    def onStepXm1(self, event):
        self.wxStepDo('x',-1)
        event.Skip()

    def onStepXp1(self, event):
        self.wxStepDo('x',1)
        event.Skip()

    def onStepXp10(self, event):
        self.wxStepDo('x',10)
        event.Skip()

    def onStepXp100(self, event):
        self.wxStepDo('x',100)
        event.Skip()

    def onStepXp1000(self, event):
        self.wxStepDo('x',1000)
        event.Skip()

    def onStepXp(self, event):
        self.wxStepDo('x',int(self.choice_xp.GetStringSelection()))
        event.Skip()

    def onStepYm(self, event):
        self.wxStepDo('y',-int(self.choice_ym.GetStringSelection()))
        event.Skip()

    def onStepYm1000(self, event):
        self.wxStepDo('y',-1000)
        event.Skip()

    def onStepYm100(self, event):
        self.wxStepDo('y',-100)
        event.Skip()

    def onStepYm10(self, event):
        self.wxStepDo('y',-10)
        event.Skip()

    def onStepYm1(self, event):
        self.wxStepDo('y',-1)
        event.Skip()

    def onStepYp1(self, event):
        self.wxStepDo('y',1)
        event.Skip()

    def onStepYp10(self, event):
        self.wxStepDo('y',10)
        event.Skip()

    def onStepYp100(self, event):
        self.wxStepDo('y',100)
        event.Skip()

    def onStepYp1000(self, event):
        self.wxStepDo('y',1000)
        event.Skip()

    def onStepYp(self, event):
        self.wxStepDo('y',int(self.choice_ym.GetStringSelection()))
        event.Skip()

    def onStepZm(self, event):
        self.wxStepDo('z',-int(self.choice_zm.GetStringSelection()))
        event.Skip()

    def onStepZm1000(self, event):
        self.wxStepDo('z',-1000)
        event.Skip()

    def onStepZm100(self, event):
        self.wxStepDo('z',-100)
        event.Skip()

    def onStepZm10(self, event):
        self.wxStepDo('z',-10)
        event.Skip()

    def onStepZm1(self, event):
        self.wxStepDo('z',-1)
        event.Skip()

    def onStepZp1(self, event):
        self.wxStepDo('z',1)
        event.Skip()

    def onStepZp10(self, event):
        self.wxStepDo('z',10)
        event.Skip()

    def onStepZp100(self, event):
        self.wxStepDo('z',100)
        event.Skip()

    def onStepZp1000(self, event):
        self.wxStepDo('z',1000)
        event.Skip()

    def onStepZp(self, event):
        self.wxStepDo('z',int(self.choice_zm.GetStringSelection()))
        event.Skip()

    def onStepVm(self, event):
        self.wxStepDo('v',-int(self.choice_vm.GetStringSelection()))
        event.Skip()

    def onStepVm1000(self, event):
        self.wxStepDo('v',-1000)
        event.Skip()

    def onStepVm100(self, event):
        self.wxStepDo('v',-100)
        event.Skip()

    def onStepVm10(self, event):
        self.wxStepDo('v',-10)
        event.Skip()

    def onStepVm1(self, event):
        self.wxStepDo('v',-1)
        event.Skip()

    def onStepVp1(self, event):
        self.wxStepDo('v',1)
        event.Skip()

    def onStepVp10(self, event):
        self.wxStepDo('v',10)
        event.Skip()

    def onStepVp100(self, event):
        self.wxStepDo('v',100)
        event.Skip()

    def onStepVp1000(self, event):
        self.wxStepDo('v',1000)
        event.Skip()

    def onStepVp(self, event):
        self.wxStepDo('v',int(self.choice_vm.GetStringSelection()))
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

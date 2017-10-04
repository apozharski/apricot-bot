#!/usr/bin/env python
#from abot import TheBot
#robot = TheBot()
#robot.xgoto(1000)

from target import ApriTarget, ApriTargetY
base = ApriTarget()
trayspots = ApriTargetY(base, 1000, 4)

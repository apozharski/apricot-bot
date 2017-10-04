#!/usr/bin/env python
from abot import TheBot
robot = TheBot()

from target import ApriTarget, ApriTargetY, ApriTargetX
base = ApriTarget()
trayspots = ApriTargetY(base, 290, 4410, 4)
traycols = ApriTargetY(trayspots, 0, -281, 12)
trayrows = ApriTargetX(traycols, 666, 1126, 8)

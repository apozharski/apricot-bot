#!/usr/bin/env python
from abot import TheBot
robot = TheBot()

def objprint(item):
    print '\n'.join([str(x)+': '+str(item.__getattribute__(x)) for x in dir(item)])

from target import load_template, ApriTarget
base = ApriTarget()
trayspots = load_template('templates/spots.apb',base)
traycols = load_template('templates/nunc96.apb',trayspots,'cols')
trayrows = load_template('templates/nunc96.apb',traycols,'rows')

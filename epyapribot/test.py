#!/usr/bin/env python

def objprint(item):
    print '\n'.join([str(x)+': '+str(item.__getattribute__(x)) for x in dir(item)])


from abot import TheBot
from target import load_template, ApriTarget
robot = TheBot()
base = ApriTarget()
fname = 'templates/swissci8x6.apb'
trayspots = load_template('templates/apribot.apb',base,'spot')
trayrows = load_template(fname,trayspots,'rows')
traycols = load_template(fname,trayrows,'cols')
traywell = load_template(fname,traycols,'well')
traytips = load_template(fname,traywell,'tips')

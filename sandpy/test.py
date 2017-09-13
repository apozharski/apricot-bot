#!/usr/bin/env python
import re, sys, time

ptrn_def = re.compile("^#define *COMM_([A-Z]*) *(\d*)")
with open('sercomm.h') as fhead:
    comms = dict([x.groups() for x in map(ptrn_def.match, fhead.readlines()) if x])

def makecomm(a,b):
    return str(comms.get(a.upper(),'')).ljust(4)+str(b).ljust(8)


import serial
ser = serial.Serial('/dev/ttyUSB0', 9600)
time.sleep(1)
ser.write(makecomm('xfwd', '400'))
ser.write(makecomm('xhome',''))
print ser.readline()
ser.close()

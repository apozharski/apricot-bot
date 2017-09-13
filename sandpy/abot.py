#!/usr/bin/env python
headerhelp = \
'''
ABOT runs a set of Apricot-Bot commands.

The set of available commands is automatically extracted from a header
file (should be the same as the one used by Arduino driver!).  
Specifically, define statements will be parsed for the COMM_* patterns.
Uppercase only
'''
from argparse import ArgumentParser, RawDescriptionHelpFormatter
parser = ArgumentParser(formatter_class=RawDescriptionHelpFormatter,
                        description=headerhelp)
parser.add_argument('-d', '--hfile', default='sercomm.h', help='Header file from which command table is extracted.')
parser.add_argument('-c', '--cfile', help='Command file, defaults to stdin.')
parser.add_argument('-s', '--serial-port', default='USB0', help='Serial port, efaults to USB0.  Actual port is /dev/ttyXXXX.')
parser.add_argument('--dry-run', action='store_true', help='Dry run.')

args, xtra_argv = parser.parse_known_args()

import re, sys, time

ptrn_def = re.compile("^#define *COMM_([A-Z]*) *(\d*)")
with open(args.hfile) as fhead:
    comms = dict([x.groups() for x in map(ptrn_def.match, fhead.readlines()) if x])

def makecomm(a,b):
    return str(comms.get(a.upper(),'')).ljust(4)+str(b).ljust(8)


if not args.dry_run:
    import serial
    ser = serial.Serial('/dev/tty'+args.serial_port, 9600)
    time.sleep(1)
if args.cfile:
    fcomm = open(args.cfile)
else:
    fcomm = sys.stdin
for line in fcomm.readlines():
    if line.strip().lower() == 'end':
        break
    valComm, valParam = (line.split()+['',''])[:2]
    sys.stdout.write('INPUT: '+line)
    sys.stdout.write('SEND : |'+makecomm(valComm, valParam)+'|\n')
    if not args.dry_run:
        print ser.write(makecomm(valComm, valParam))
        print ser.readline()
if args.cfile:
    fcomm.close()
if not args.dry_run:
    ser.close()

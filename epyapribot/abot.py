import serial, time, re

class TheBot(object):
    def __init__(self, fHome=True, *args, **kwds):
        serport = kwds.pop('serport','USB0')
        self.ser = serial.Serial('/dev/tty'+serport, 9600)
        time.sleep(1)
        ptrn_def = re.compile("^#define *COMM_([A-Z]*) *(\d*)")
        self.hfile = kwds.pop('hfile', 'sercomm.h')
        with open(self.hfile) as fhead:
            self.comms = dict([x.groups() for x in map(ptrn_def.match, fhead.readlines()) if x])
        if fHome:
            self.home()
        else:
            self.x = kwds.pop('x')
            self.y = kwds.pop('y')
            self.z = kwds.pop('z')
        self.xargs = args
        self.xkwds = kwds
    def makecomm(self,a,b):
        return str(self.comms.get(a.upper(),'')).ljust(4)+str(b).ljust(8)
    def runcomm(self, valComm, valParam=''):
        return self.ser.write(self.makecomm(valComm, valParam))
    def home(self):
        self.zhome()
        self.xhome()
        self.yhome()
    def xhome(self):
        print self.runcomm('xhome')

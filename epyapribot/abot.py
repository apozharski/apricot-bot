import serial, time, re, inspect, os

XLIMIT = 9200
YLIMIT = 13640
ZLIMIT = 7000
PLIMIT = 36000

class TheBot(object):
    def __init__(self, fHome=True, *args, **kwds):
        serport = kwds.pop('serport','USB0')
        self.ser = serial.Serial('/dev/tty'+serport, 9600)
        time.sleep(1)
        ptrn_def = re.compile("^#define *COMM_([A-Z]*) *(\d*)")
        self.hfile = kwds.pop('hfile', os.path.join(os.path.abspath(os.path.dirname(inspect.getfile(inspect.getmodule(self)))),'sercomm.h'))
        with open(self.hfile) as fhead:
            self.comms = dict([x.groups() for x in map(ptrn_def.match, fhead.readlines()) if x])
        if fHome:
            self.home()
        else:
            self.x = kwds.pop('x')
            self.y = kwds.pop('y')
            self.z = kwds.pop('z')
            self.piston = kwds.pop('v')
        self.xargs = args
        self.xkwds = kwds
    def makecomm(self,a,b):
        return str(self.comms.get(a.upper(),'')).ljust(4)+str(b).ljust(8)
    def runcomm(self, valComm, valParam=''):
        self.ser.write(self.makecomm(valComm, valParam))
        return self.ser.readline()
    def home(self):
        self.zhome()
        self.xhome()
        self.yhome()
        self.phomedn()
    def xhome(self):
        print self.runcomm('xhome')
        self.x = 0
    def yhome(self):
        print self.runcomm('yhome')
        self.y = 0
    def zhome(self):
        print self.runcomm('zhome')
        self.z = 0
    def xgoto(self, x):
        if x < 0 or x > XLIMIT or x is None:
            return
        if self.x < x:
            print self.runcomm('xfwd', x-self.x)
        elif self.x > x:
            print self.runcomm('xback', self.x-x)
        self.x = x
    def ygoto(self, y):
        if y < 0 or y > YLIMIT or y is None:
            return
        if self.y < y:
            print self.runcomm('yfwd', y-self.y)
        elif self.y > y:
            print self.runcomm('yback', self.y-y)
        self.y = y
    def zgoto(self, z):
        if z < 0 or z > ZLIMIT or z is None:
            return
        if self.z < z:
            print self.runcomm('zfwd', z-self.z)
        elif self.z > z:
            print self.runcomm('zback', self.z-z)
        self.z = z
    def phomedn(self):
        print self.runcomm('phomedn')
        self.piston = 0
    def phomeup(self):
        print self.runcomm('phomeup')
        self.piston = PLIMIT
    def pgoto(self, v):
        if v < 0 or v is None:
            return
        if self.piston < v:
            print self.runcomm('pistonup', v-self.piston)
        elif self.piston > v:
            print self.runcomm('pistondn', self.piston-v)
        self.piston = v
    def goto(self, x=None, y=None, z=None, v=None, xyzv=None, order=None, safez=None):
        if xyzv is not None:
            x,y,z,v = xyzv
        if order is None or type(order) not in [str,unicode]:
            order = 'zxyv'
        if safez is not None:
            self.zgoto(safez)
            order = order.replace('z','')
        for c in order:
            if c in 'xyzv':
                exec('self.'+c.replace('v','p')+'goto('+c+')')
        if safez is not None:
            self.zgoto(z)

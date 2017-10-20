import serial, time, re, inspect, os, sys

XLIMIT = 9200
YLIMIT = 13640
ZLIMIT = 7000
PLIMIT = 36000

LIMIT_ERROR = 2

def limit_error(value, value_limit, axletter):
    if value < 0:
        rsn = axletter+'-HOME'
    if value > value_limit:
        rsn = axletter+'-LIMIT'
    sys.stderr.write('WARNING: Requested move beyond '+rsn+' denied.')
    return LIMIT_ERROR

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
        return self.ser.readline().strip()
    def home(self):
        self.zhome()
        self.xhome()
        self.yhome()
        self.phomedn()
    def xhome(self):
        retcode = self.runcomm('xhome')
        self.x = 0
        return retcode
    def yhome(self):
        retcode = self.runcomm('yhome')
        self.y = 0
        return retcode
    def zhome(self):
        retcode = self.runcomm('zhome')
        self.z = 0
        return retcode
    def xgoto(self, x):
        retcode = None
        if x < 0 or x > XLIMIT or x is None:
            return limit_error(x, XLIMIT, 'X')
        if self.x < x:
            retcode = self.runcomm('xfwd', x-self.x)
        elif self.x > x:
            retcode = self.runcomm('xback', self.x-x)
        self.x = x
        return retcode
    def ygoto(self, y):
        retcode = None
        if y < 0 or y > YLIMIT or y is None:
            return limit_error(y, YLIMIT, 'Y')
        if self.y < y:
            retcode = self.runcomm('yfwd', y-self.y)
        elif self.y > y:
            retcode = self.runcomm('yback', self.y-y)
        self.y = y
        return retcode
    def zgoto(self, z):
        retcode = None
        if z < 0 or z > ZLIMIT or z is None:
            return limit_error(z, ZLIMIT, 'Z')
        if self.z < z:
            retcode = self.runcomm('zfwd', z-self.z)
        elif self.z > z:
            retcode = self.runcomm('zback', self.z-z)
        self.z = z
        return retcode
    def phomedn(self):
        retcode = self.runcomm('phomedn')
        self.piston = 0
        return retcode
    def phomeup(self):
        retcode = self.runcomm('phomeup')
        self.piston = PLIMIT
        return retcode
    def pgoto(self, v):
        retcode = None
        if v < 0 or v > PLIMIT or v is None:
            return limit_error(v, PLIMIT, 'P')
        if self.piston < v:
            retcode = self.runcomm('pistonup', v-self.piston)
        elif self.piston > v:
            retcode = self.runcomm('pistondn', self.piston-v)
        self.piston = v
        return retcode
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

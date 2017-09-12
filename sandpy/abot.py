import serial
ser = serial.Serial('/dev/ttyUSB0', 9600)

comms = dict(zip(*[['xhome','yhome','zhome',
                    'ledblink',
                    'xfwd','yfwd','zfwd',
                    'xback','yback','zback',
                    'phomedn','phomeup','pistonup','pistondn',],
                    range(1,15)]))


def makecomm(a,b):
    return str(comms[a]).ljust(4)+str(b).ljust(8)


for i in range(11):
 ser.write(makecomm('zback',1000))
 ser.write(makecomm('yback',281))
 ser.write(makecomm('zfwd',1000))
 ser.write(makecomm('pistondn',1000))

ser.close()

import sys
import pyvisa 
import time
from datetime import date
from datetime import datetime
import csv
import subprocess
import socket

viavi = pyvisa.ResourceManager()
print(viavi.list_resources())
alt9000 = viavi.open_resource("TCPIP0::10.1.1.153::5025::SOCKET")
print(alt9000)
# #multimeter.timeout = 5000
alt9000.read_termination = '\n'
alt9000.write_termination = '\n'
#print(alt9000.query('RALT:ASIM:MODE MAN'))
#time.sleep(1)
alt9000.write(':RALT:TEST:STOP')
time.sleep(2)
alt9000.write(':RALT:ASIM:MODE MAN')
print(alt9000.query('RALT:ASIM:MODE?'))
i=700
cmd=":RALT:ASIM:MAN:CHAN1:START "+str(i)
print(cmd)

alt9000.write(':RALT:ASIM:MAN:CHAN1:RATE 0')
alt9000.write(cmd)
print(alt9000.query(':RALT:ASIM:MAN:CHAN1:START?'))
print(alt9000.query(':RALT:ASIM:MAN:CHAN1:RATE?'))

alt9000.write(":RALT:SET:CHAN1:LOSS:CABL:TX 0.5")
alt9000.write(":RALT:SET:CHAN1:LOSS:CABL:RX 7.2")

print(alt9000.query(":RALT:SET:CHAN1:LOSS:CABL:TX?"))
print(alt9000.query(":RALT:SET:CHAN1:LOSS:CABL:RX?"))

# #print(multimeter.query(":function:voltage:DC"))
#alt9000.ignore_warning()
alt9000.write('RALT:TEST:STAR')
time.sleep(10)
if alt9000.query(':RALT:TEST:RUNN?'):
    print('Test running')
alt9000.write('RALT:TEST:PAUS')
alt9000.write('RALT:ASIM:MAN:CHAN1:ALT 200')
time.sleep(5)
alt9000.write('RALT:ASIM:MAN:CHAN1:ALT 2000')
time.sleep(5)
alt9000.write('RALT:ASIM:MAN:CHAN1:ALT 2500')
time.sleep(5)
alt9000.write('RALT:ASIM:MAN:CHAN1:ALT 50')
time.sleep(5)
alt9000.write('RALT:TEST:STOP')


#print(alt9000.query('RALTimeter:ASIMulation:MANual:CHANnel1:ALTitude 200'))
#time.sleep(5)
#print(alt9000.query('RALT:ASIM:MAN:CHAN1:ActualALTitude?'))
#time.sleep(1)


alt9000.close()
exit()

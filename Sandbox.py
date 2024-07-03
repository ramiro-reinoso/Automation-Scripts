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
print(alt9000.query('RALT:ASIM:MODE?'))

alt9000.write(':RALT:ASIM:MAN:CHAN1:RATE 0')
alt9000.write(':RALT:ASIM:MAN:CHAN1:START 800')
print(alt9000.query(':RALT:ASIM:MAN:CHAN1:START?'))
print(alt9000.query(':RALT:ASIM:MAN:CHAN1:RATE?'))

# #print(multimeter.query(":function:voltage:DC"))
#alt9000.ignore_warning()
alt9000.write('RALT:TEST:STAR')
time.sleep(3)
alt9000.write('RALT:TEST:PAUS')
time.sleep(10)
if alt9000.query(':RALT:TEST:RUNN?'):
    print('Test running')
print("Loop Loss Value: " + alt9000.query(':RALT:SET:CHAN1:LLOSs?'))
time.sleep(3)
alt9000.write('RALT:TEST:STOP')
time.sleep(2)


#print(alt9000.query('RALTimeter:ASIMulation:MANual:CHANnel1:ALTitude 200'))
#time.sleep(5)
#print(alt9000.query('RALT:ASIM:MAN:CHAN1:ActualALTitude?'))
#time.sleep(1)


alt9000.close()
exit()

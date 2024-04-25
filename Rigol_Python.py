import sys
import pyvisa 
import time
from datetime import date
from datetime import datetime
import csv
import subprocess
import socket

rigol = pyvisa.ResourceManager()
print(rigol.list_resources())
multimeter = rigol.open_resource("TCPIP0::10.1.1.155::inst0::INSTR")
print(multimeter)
#multimeter.timeout = 5000
multimeter.read_termination = '\n'
multimeter.write_termination = '\n'
print(multimeter.query('*IDN?'))
#print(multimeter.query(":function:voltage:DC"))

while 1:
  print(multimeter.query(":measure:voltage:DC?"))

multimeter.close()
exit()

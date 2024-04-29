# using time module
import time

# import the VISA libraries to communicate with the Rigol multimeter
import pyvisa

import io
from alt55B_volts_to_feet import voltstofeet

# Open the session with the Rigol multimeter
rigol = pyvisa.ResourceManager()
multimeter = rigol.open_resource("TCPIP0::10.1.1.155::inst0::INSTR")
multimeter.read_termination = '\n'
multimeter.write_termination = '\n'

# Open the output file
outfile = open("ALT-55B_200ft_VCO_Off-On.csv","w")

# init_ts stores the script start time in seconds
init_ts = time.time()

# Establish the baseline performance for 60 seconds
print("Establish baseline performance")
while time.time() < init_ts + 60:
  timestamp = time.time() - init_ts
  print(float(timestamp),",0,NA,", float(voltstofeet(multimeter.query(":measure:voltage:DC?"))),file=outfile)
  print(timestamp)

print("Turn VCOs ON")
while time.time() < init_ts + 120:
  timestamp = time.time() - init_ts
  print(float(timestamp),",1,-62,", float(voltstofeet(multimeter.query(":measure:voltage:DC?"))),file=outfile)
  print(timestamp)


multimeter.close()
outfile.close()
exit()

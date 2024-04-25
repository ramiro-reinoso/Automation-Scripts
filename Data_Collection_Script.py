# using time module
import time
# import the Rohde & Schwarz SMCV libraries
from RsSmcv import *
# import the VISA libraries to communicate with the Rigol multimeter
import pyvisa

import io
from alt55B_volts_to_feet import voltstofeet

# Open the session with the Signal Generator
RsSmcv.assert_minimum_version('5.0.122')
smcv = RsSmcv('TCPIP::10.1.1.150::HISLIP')

# Open the session with the Rigol multimeter
rigol = pyvisa.ResourceManager()
multimeter = rigol.open_resource("TCPIP0::10.1.1.155::inst0::INSTR")
multimeter.read_termination = '\n'
multimeter.write_termination = '\n'

# Open the output file
outfile = open("Sample_Test.csv","w")

# init_ts stores the script start time in seconds
init_ts = time.time()

# Establish the baseline performance for 60 seconds
print("Establish baseline performance")
while time.time() < init_ts + 60:
  timestamp = init_ts - time.time()
  print(float(timestamp),",", float(voltstofeet(multimeter.query(":measure:voltage:DC?"))),file=outfile)

# Start the sweep
for x in range(-30, -10):
  smcv.source.power.level.immediate.set_amplitude(x)
  
  print("Power level ", int(x)," ,RF Output ON")
  temptime = time.time()
  smcv.output.state.set_value(True)
  while time.time() < temptime + 20:
    timestamp = init_ts - time.time()
    print(float(timestamp),",", float(voltstofeet(multimeter.query(":measure:voltage:DC?"))),file=outfile)

  print("RF Power Output OFF")
  temptime = time.time()
  smcv.output.state.set_value(False)   
  while time.time() < temptime + 10:
    timestamp = init_ts - time.time()
    print(float(timestamp),",", float(voltstofeet(multimeter.query(":measure:voltage:DC?"))),file=outfile)

smcv.close()
multimeter.close()
exit()

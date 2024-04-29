# using time module
import time
# import the Rohde & Schwarz SMCV libraries
from RsSmcv import *
# import the VISA libraries to communicate with the Rigol multimeter
import pyvisa

import io
from alt55B_volts_to_feet import voltstofeet

# Setup some variables
genminpower = -15
genmaxpower = 4
minpowerforplot = genminpower - 10
altitudes = [50,100,200,500,1000,2000,2500]

# Open the log file for this session and prepare for logging
siminit=time.time()


# Open the session with the Signal Generator
RsSmcv.assert_minimum_version('5.0.122')
smcv = RsSmcv('TCPIP::10.1.1.150::HISLIP')
print(smcv)

# Open the session with the Rigol multimeter
rigol = pyvisa.ResourceManager()
multimeter = rigol.open_resource("TCPIP0::10.1.1.155::inst0::INSTR")
multimeter.read_termination = '\n'
multimeter.write_termination = '\n'
print(multimeter)

# Open the ALT-9000 control session
viavi = pyvisa.ResourceManager()
alt9000 = viavi.open_resource("TCPIP0::10.1.1.153::5025::SOCKET")
alt9000.read_termination = '\n'
alt9000.write_termination = '\n'
print(alt9000)
# Stop any on-going simulations
alt9000.write('RALT:TEST:STOP')
time.sleep(2)
#Set the Tx and Rx cable losses for the simulation as measured
alt9000.write(":RALT:SET:CHAN1:LOSS:CABL:TX 1.3")
alt9000.write(":RALT:SET:CHAN1:LOSS:CABL:RX 8.7")
print(alt9000.query(":RALT:SET:CHAN1:LOSS:CABL:TX?"))
print(alt9000.query(":RALT:SET:CHAN1:LOSS:CABL:RX?"))
# Set the ALT9000 to manual mode and fixed altitude
alt9000.write(':RALT:ASIM:MODE MAN')
print(alt9000.query('RALT:ASIM:MODE?'))
alt9000.write(':RALT:ASIM:MAN:CHAN1:RATE 0')
print(alt9000.query(':RALT:ASIM:MAN:CHAN1:RATE?'))
# Start the ALT-9000 simulation at 100 ft and pause it
alt9000.write(":RALT:ASIM:MAN:CHAN1:START 100")
alt9000.write('RALT:TEST:STAR')
time.sleep(10)
alt9000.write('RALT:TEST:PAUS')


for i in altitudes:
  print('Altitude ',int(i),' feet')

  # Set the ALT-9000 to the desired altitude
  cmd=":RALT:ASIM:MAN:CHAN1:ALT "+str(i)
  alt9000.write(cmd)
  time.sleep(5)

  # Open the output file for writing
  filename="ALT-55B-Apr29-24\ALT-55B_"+str(i)+".csv"
  outfile = open(filename,"w")

  # init_ts stores the script start time in seconds
  init_ts = time.time()

  # Establish the baseline performance for 60 seconds
  print("Establish baseline performance")
  smcv.output.state.set_value(False)
  time.sleep(2)
  while time.time() < init_ts + 60:
    timestamp = time.time() - init_ts
    print(float(timestamp),",0,",int(minpowerforplot),",", float(voltstofeet(multimeter.query(":measure:voltage:DC?"))),file=outfile)

  # Start the sweep
  for x in range(genminpower, genmaxpower):
    smcv.source.power.level.immediate.set_amplitude(x)
    
    print("Power level ", int(x)," ,RF Output ON")
    smcv.output.state.set_value(True)
    time.sleep(2)  # Wait before collecting sample to avoid any transient effects
    temptime = time.time()
    while time.time() < temptime + 20:
      timestamp = time.time() - init_ts
      print(float(timestamp),",1,", int(x),",", float(voltstofeet(multimeter.query(":measure:voltage:DC?"))),file=outfile)

    print("RF Power Output OFF")
    temptime = time.time()
    smcv.output.state.set_value(False)   
    while time.time() < temptime + 10:
      timestamp = time.time() - init_ts
      print(float(timestamp),",0,",int(minpowerforplot),",", float(voltstofeet(multimeter.query(":measure:voltage:DC?"))),file=outfile)
  
  outfile.close()

alt9000.write('RALT:TEST:STOP')
smcv.close()
multimeter.close()
alt9000.close()
print("Total Simulation Time:")
print(time.time() - siminit)

exit()

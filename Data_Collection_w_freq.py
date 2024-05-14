# using time module
import time
# import the Rohde & Schwarz SMCV libraries
from RsSmcv import *
# import the VISA libraries to communicate with the Rigol multimeter
import pyvisa

# import file libraries
import os

# import local functions
from alt55B_volts_to_feet import voltstofeet

# Setup variables for this simulation
folder="ALT-55B-May14-24-03"
radar="ALT-55B"
genminpower = -11
genmaxpower = -10
minpowerforplot = genminpower - 10
frequencies = [4000]
altitudes = [50]
stopat = 0.2  # Stop if the average altitude is stopat percent greater than baseline altitude
              # for a given power level.
baselineduration = 10 # Duration of the baseline period. AVSI is 60 seconds.
rfonduration = 10 # Duration of the RF ON period. AVSI is 20 seconds.
rfoffduration = 1800 # Duration of the RF OFF period.  AVSI is 10 seconds.

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
# Stop any on-going simulations
alt9000.write('RALT:TEST:STOP')
time.sleep(2)
#Set the Tx and Rx cable losses for the simulation as measured
alt9000.write(":RALT:SET:CHAN1:LOSS:CABL:TX 1.3")
alt9000.write(":RALT:SET:CHAN1:LOSS:CABL:RX 8.7")
# Set the ALT9000 to manual mode and fixed altitude
alt9000.write(':RALT:ASIM:MODE MAN')
alt9000.write(':RALT:ASIM:MAN:CHAN1:RATE 0')
# Log the simulator configuration
print("ALT9000 Session Info: ",str(alt9000))
print("Simulation Mode: ",str(alt9000.query('RALT:ASIM:MODE?')))
print("Simulation Climbing Rate (should be zero): ",str(alt9000.query(':RALT:ASIM:MAN:CHAN1:RATE?'))," feet/sec")
print("Transmit cable losses: ",str(alt9000.query(":RALT:SET:CHAN1:LOSS:CABL:TX?"))," dB")
print("Receive cable losses: ",str(alt9000.query(":RALT:SET:CHAN1:LOSS:CABL:RX?"))," dB")

# Start the ALT-9000 simulation at 100 ft and pause it
alt9000.write(":RALT:ASIM:MAN:CHAN1:START 100")
alt9000.write('RALT:TEST:STAR')
time.sleep(10)
alt9000.write('RALT:TEST:PAUS')

# Start the loop to cycle through 5G carrier center frequencies
for j in frequencies:
  print("Testing with CF "+str(j))
  # Set the frequency in the 5G Signal Generator
  cmd=j*1000000
  smcv.source.frequency.fixed.set_value(cmd)

  # Start the loop to cycle through the altitudes
  for i in altitudes:
    # Set the ALT-9000 to the desired altitude
    cmd=":RALT:ASIM:MAN:CHAN1:ALT "+str(i)
    alt9000.write(cmd)
    time.sleep(5)

    print('Desired Altitude: ',int(i),' feet')
    print("Altitude in ALT9000: ",str(alt9000.query("RALT:ASIM:MAN:CHAN1:ALT?"))," feet")

    # Open the output file for writing
    if not os.path.exists(folder):
      os.makedirs(folder)

    filename=folder+"\\"+radar+"_"+str(j)+"_"+str(i)+".csv"
    outfile = open(filename,"w")

    # Write the column headers in the results csv file
    print("time,rfon,pwr,alt",file=outfile)

    # init_ts stores the script start time in seconds
    init_ts = time.time()

    # Establish the baseline performance for 60 seconds
    print("Establish baseline performance")
    smcv.output.state.set_value(False)
    time.sleep(5)
    basesamples=0
    basecumulative=0.0
    baseaverage=0.0

    while time.time() < init_ts + baselineduration:
      timestamp = time.time() - init_ts
      print(float(timestamp),",0,",int(minpowerforplot),",", float(voltstofeet(multimeter.query(":measure:voltage:DC?"))),file=outfile)
      basesamples=basesamples + 1
      basecumulative=basecumulative + voltstofeet(multimeter.query(":measure:voltage:DC?"))

    baseaverage=basecumulative / basesamples  # Establish the average altitude baseline 

    # Start the sweep
    done = False
    for x in range(genminpower, genmaxpower):
      if done:
        break   # No need to go further as the radar failed the last power level tests

      smcv.source.power.level.immediate.set_amplitude(x)
      
      print("Power level ", int(x)," ,RF Output ON")
      smcv.output.state.set_value(True)
      time.sleep(2)  # Wait before collecting sample to avoid any transient effects
      thissamples=0
      thisaverage=0.0
      thiscumulative=0.0
      temptime = time.time()
      while time.time() < temptime + rfonduration:
        timestamp = time.time() - init_ts
        print(float(timestamp),",1,", int(x),",", float(voltstofeet(multimeter.query(":measure:voltage:DC?"))),file=outfile)
        thissamples=thissamples + 1
        thiscumulative=thiscumulative + voltstofeet(multimeter.query(":measure:voltage:DC?"))

      thisaverage=thiscumulative / thissamples  # Calculate the average altitude for this sweep

      print("RF Power Output OFF")
      temptime = time.time()
      smcv.output.state.set_value(False)   
      while time.time() < temptime + rfoffduration:
        timestamp = time.time() - init_ts
        print(float(timestamp),",0,",int(minpowerforplot),",", float(voltstofeet(multimeter.query(":measure:voltage:DC?"))),file=outfile)

      if (abs(baseaverage - thisaverage)/baseaverage) > stopat:
        done = True
    
    outfile.close()



alt9000.write('RALT:TEST:RES')
time.sleep(2)
alt9000.write('RALT:TEST:STOP')
smcv.close()
multimeter.close()
alt9000.close()
print("Total Simulation Time: ",str(time.time() - siminit)," seconds.")
exit()

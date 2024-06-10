# using time module
import time
# import the datetime library for logging date and time
import datetime
# import the Rohde & Schwarz SMCV libraries
from RsSmcv import *
# import the VISA libraries to communicate with the Rigol multimeter
import pyvisa

# import file libraries
import os

# import local functions
from alt55B_volts_to_feet import voltstofeet
from powertopsd5g import pwrtopsdLabFilter

def logger(logmsg):
    print(str(datetime.datetime.now())+"\t"+logmsg)
    global logfile
    print(str(datetime.datetime.now())+"\t"+logmsg,file=logfile)


# Setup variables for this simulation
folder="ALT-55B-Jun6-24-01"
radar="ALT-55B"
genminpower = -20
genmaxpower = -5
minpowerforplot = genminpower - 10

altitudes = [20,50,100,200,500,1000,2000,2500]
frequencies = [4050]

stopat = 100  # Stop if the average altitude is stopat percent greater than baseline altitude
              # for a given power level.

baselineduration = 60 # Duration of the baseline period. AVSI is 60 seconds.
rfonduration = 20 # Duration of the RF ON period. AVSI is 20 seconds.
rfoffduration = 10 # Duration of the RF OFF period.  AVSI is 10 seconds.

# Open the log file for this session and prepare for logging
# Check if folder exists and if it doesn't exist, then create it
if not os.path.exists(folder):
  os.makedirs(folder)

logfilename=folder+"\\"+radar+"_datacollection_log.csv"
logfile=open(logfilename,'a')
logger("******************************")
logger("******************************")
logger("Start a new Test")
siminit=time.time()

# Open the session with the Signal Generator
RsSmcv.assert_minimum_version('5.0.122')
smcv = RsSmcv('TCPIP::10.1.1.150::HISLIP')
logger("5G Signal Generator Resource Description: "+str(smcv))

# Open the session with the Rigol multimeter
rigol = pyvisa.ResourceManager()
multimeter = rigol.open_resource("TCPIP0::10.1.1.155::inst0::INSTR")
multimeter.read_termination = '\n'
multimeter.write_termination = '\n'
logger("Multimeter Resource Description: "+str(multimeter))

# Open the session with the power supply for the VCO
pwrsupply = pyvisa.ResourceManager()
hmc8042 = pwrsupply.open_resource("TCPIP0::10.1.1.158::5025::SOCKET")
logger("Power Supply Resource Description: "+str(hmc8042))
hmc8042.read_termination = '\n'
hmc8042.write_termination = '\n'


# Open the ALT-9000 control session
viavi = pyvisa.ResourceManager()
alt9000 = viavi.open_resource("TCPIP0::10.1.1.153::5025::SOCKET")
logger("Altitude Simulator Resource Description: "+str(alt9000))
alt9000.read_termination = '\n'
alt9000.write_termination = '\n'
# Stop any on-going simulations
alt9000.write('RALT:TEST:STOP')
time.sleep(2)
#Set the Tx and Rx cable losses for the simulation as measured
alt9000.write(":RALT:SET:CHAN1:LOSS:CABL:TX 1.3")
alt9000.write(":RALT:SET:CHAN1:LOSS:CABL:RX 1.3")
alt9000.write(":RALT:SET:CHAN1:LOSS:EXT:RX 8.7")
# Set the ALT9000 to manual mode and fixed altitude
alt9000.write(':RALT:ASIM:MODE MAN')
alt9000.write(':RALT:ASIM:MAN:CHAN1:RATE 0')
# Log the simulator configuration
logger("Altitude Simulator Mode: "+str(alt9000.query('RALT:ASIM:MODE?')))
logger("Altitude Simulator Simulation Climbing Rate (should be zero): "+str(alt9000.query(':RALT:ASIM:MAN:CHAN1:RATE?'))+" feet/sec")
logger("Altitude Simulator Transmit cable losses: "+str(round(float(alt9000.query(":RALT:SET:CHAN1:LOSS:CABL:TX?")),2))+" dB")
logger("Altitude Simulator Receive cable losses: "+str(round(float(alt9000.query(":RALT:SET:CHAN1:LOSS:CABL:RX?")),2))+" dB")
logger("Altitude Simulator Receive directional coupler losses: "+str(round(float(alt9000.query(":RALT:SET:CHAN1:LOSS:EXT:RX?")),2))+" dB")

# Start the ALT-9000 simulation at 100 ft and pause it
alt9000.write(":RALT:ASIM:MAN:CHAN1:START 100")
alt9000.write('RALT:TEST:STAR')
time.sleep(10)
alt9000.write('RALT:TEST:PAUS')

# Start the loop to cycle through 5G carrier center frequencies
for j in frequencies:
  logger("Collecting data using a 5G carrier with Center Frequency "+str(j)+" MHz")
  # Set the frequency in the 5G Signal Generator
  cmd=j*1000000
  smcv.source.frequency.fixed.set_value(cmd)

  # Start the loop to cycle through the altitudes
  for i in altitudes:
   # Set the ALT-9000 to the desired altitude
    cmd=":RALT:ASIM:MAN:CHAN1:ALT "+str(i)
    alt9000.write(cmd)
    time.sleep(5)

    logger('Desired Altitude: '+str(i)+' feet')
    logger("Altitude Simulated reported by the ALT9000: "+str(alt9000.query("RALT:ASIM:MAN:CHAN1:ALT?"))+" feet")

    # Turn OFF the VCOs for the other planes alt radar simulators if altitude is above 200 feet
    if i > 200:
      logger("Altitude is above 200 feet. Turn OFF VCO Power Supply.")
      hmc8042.write('INST:SEL 1')
      hmc8042.write('OUTP OFF')
      hmc8042.write('OUTP:MAST OFF')
    else:
      logger("Altitude is below 200 feet. Turn ON VCO power supply.")
      hmc8042.write('OUTP:MAST ON')
      hmc8042.write('INST:SEL 1')
      hmc8042.write('OUTP ON')

    # Open the output file for writing
    if not os.path.exists(folder):
      os.makedirs(folder)

    filename=folder+"\\"+radar+"_"+str(j)+"_"+str(i)+".csv"
    outfile = open(filename,"w")

    # Write the column headers in the results csv file
    print("time,rfon,pwr,psd,alt",file=outfile)

    # init_ts stores the script start time in seconds
    init_ts = time.time()

    # Establish the baseline performance for 60 seconds
    logger("Turn OFF 5G Signal Generator Output")
    logger("Establishing baseline performance")
    smcv.output.state.set_value(False)
    time.sleep(5)
    basesamples=0
    basecumulative=0.0
    baseaverage=0.0

    while time.time() < init_ts + baselineduration:
      timestamp = time.time() - init_ts
      print(float(timestamp),",0,",int(minpowerforplot),",", float(pwrtopsdLabFilter(minpowerforplot)),",",float(voltstofeet(multimeter.query(":measure:voltage:DC?"))),file=outfile)
      basesamples=basesamples + 1
      basecumulative=basecumulative + voltstofeet(multimeter.query(":measure:voltage:DC?"))

    baseaverage=basecumulative / basesamples  # Establish the average altitude baseline 
    logger("Completed baseline performance. Average altitude is "+str(round(float(baseaverage),2))+" feet")
    logger("Start data collection")

    # Start the sweep
    done = False
    for x in range(genminpower, genmaxpower):
      if done:
        break   # No need to go further as the radar failed the last power level tests

      smcv.source.power.level.immediate.set_amplitude(x)
      
      logger("5G Center Frequency "+str(j)+" MHz, Altitude "+str(i)+" feet, 5G Output Power Level "+ str(x)+" dBm")
      smcv.output.state.set_value(True)
      time.sleep(2)  # Wait before collecting sample to avoid any transient effects
      thissamples=0
      thisaverage=0.0
      thiscumulative=0.0
      temptime = time.time()
      while time.time() < temptime + rfonduration:
        timestamp = time.time() - init_ts
        print(float(timestamp),",1,", int(x),",", float(pwrtopsdLabFilter(x)),",",float(voltstofeet(multimeter.query(":measure:voltage:DC?"))),file=outfile)
        thissamples=thissamples + 1
        thiscumulative=thiscumulative + voltstofeet(multimeter.query(":measure:voltage:DC?"))

      thisaverage=thiscumulative / thissamples  # Calculate the average altitude for this sweep

      logger("5G Generator RF Power Output OFF")
      temptime = time.time()
      smcv.output.state.set_value(False)   
      while time.time() < temptime + rfoffduration:
        timestamp = time.time() - init_ts
        print(float(timestamp),",0,",int(minpowerforplot),",", float(pwrtopsdLabFilter(minpowerforplot)),",",float(voltstofeet(multimeter.query(":measure:voltage:DC?"))),file=outfile)

      if (abs(baseaverage - thisaverage)/baseaverage) > stopat:
        done = True
    
    outfile.close()



alt9000.write('RALT:TEST:RES')
time.sleep(2)
alt9000.write('RALT:TEST:STOP')
smcv.close()
multimeter.close()
alt9000.close()
logger("Total Simulation Time: "+str(round(time.time() - siminit,2))+" seconds.")
exit()





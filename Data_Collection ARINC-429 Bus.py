#######################################################################
#                                                                     #
#  ALTIMETER RADAR TEST CONTROL SOFTWARE FOR SES TESTBED              #
#  Copyright SES Americom, Inc.                                       #
#                                                                     #
#######################################################################

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

#import the JSON utilities
import json

# import miscellaneous local functions
from alt55B_volts_to_feet import voltstofeet
from powertopsd5g import pwrtopsdFinalV3
from altitudeToVCOAttenuation import onboardVCOatt

# import libraries for the USB ARINC-429 Interfade
import sys
sys.path.append('USB_ARINC_Bus_Interface/')
from UA2000_Interface import openARINC249Card
from UA2000_Interface import readARINCaltitude
from UA2000_Interface import closeARINC249Card

# Subrouting to log and display simulation messages
def logger(logmsg):
    print(str(datetime.datetime.now())+"\t"+logmsg)
    global logfile
    print(str(datetime.datetime.now())+"\t"+logmsg,file=logfile)




# Read the simulation configuration from the JSON files.  There are two JSON files that need to be
# processed.  The first one is the Simulation.json file that containts the name of the JSON file with
# all the details pertaining to the simulation.  All the JSON files are in the json_configs folder.

# Open the main config file and extract the jSON filename where the
# simulation parameters are defined
baseconfig=open('json_configs\\Simulation.json','r')
basedata=json.load(baseconfig)
filename=basedata['ConfigFile']
# Open the JSON file with he detail configuration parameters for the simulation
configfilename="json_configs\\"+filename
jsonfile=open(configfilename)
configs=json.load(jsonfile)

# Setup variables for this simulation using he values in the JSON config file
desc=configs['Description']
signalprofile=configs['5Gtestsignal']
folder=configs['folder']
radar=configs['radar']
genminpower=configs['genminpower']
genmaxpower = configs['genmaxpower']
deltatopwroff = configs['deltatopwroff']
minpowerforplot = genminpower - deltatopwroff  # This is the power logged with the 5G Gen OFF.  This is set to 10 dB min power to help with the graphs.

altitudes = configs['altitudes']
frequencies = configs['frequencies']
includeVCO = configs['includeOtherPlanes']
includeOnBoard = configs['includeOnBoard']
filter5G = configs['5Gfilter']
stopwhenexceed = configs['stopwhenexceed'] # Stop increasing power if the altitude mean error has exceeded a threshold give by "stopat"

stopat = configs['stoplimit']  # Stop if the average altitude is stopat percent greater than baseline altitude
              # for a given power level.  The variable stopwhenexceed must be True to enable this function.  Range [0 to 0.99].

baselineduration = configs['baselineduration'] # Duration of the baseline period. AVSI is 60 seconds.
rfonduration = configs['rfonduration'] # Duration of the RF ON period. AVSI is 20 seconds.
rfoffduration = configs['rfoffduration'] # Duration of the RF OFF period.  AVSI is 10 seconds.
waittostable = configs['waittostable'] # Wait for this number of seconds after making changes to allow for radalt to stabilize


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

# Log the simulation configuration
logger("***************** CONFIGURATION ***********************")
logger("Description: " + desc)
logger("5G Signal Profile: " + signalprofile)
logger("folder: " + folder)
logger("radar: " + radar)
logger("genminpower: "+str(genminpower))
logger("genmaxpower : " + str(genmaxpower))
logger("deltatopwroff : "+ str(deltatopwroff))
logger("altitudes : "+ str(altitudes))
logger("frequencies : "+ str(frequencies))
logger("includeVCO : "+ str(includeVCO))
logger("includeOnBoard : "+ str(includeOnBoard))
logger("5GFilter: " + str(filter5G))
logger("stopwhenexceed : "+ str(stopwhenexceed)) 
logger("stopat : "+ str(stopat))
logger("baselineduration : "+ str(baselineduration))
logger("rfonduration : "+ str(rfonduration))
logger("rfoffduration : "+ str(rfoffduration))
logger("waittostable : "+ str(waittostable))
logger("***************** OPEN DEVICES ***********************")

# Open the session with the Signal Generator
RsSmcv.assert_minimum_version('5.0.122')
smcv = RsSmcv('TCPIP::10.1.1.150::HISLIP')
logger("5G Signal Generator Resource Description: "+str(smcv))

# # Open the session with the Rigol multimeter
# rigol = pyvisa.ResourceManager()
# multimeter = rigol.open_resource("TCPIP0::10.1.1.155::inst0::INSTR")
# multimeter.read_termination = '\n'
# multimeter.write_termination = '\n'
# logger("Multimeter Resource Description: "+str(multimeter))

# Open the session with the Astronics UA2000 ARINC-429 Bus Interface
logger("Opening the ARINC-429 USB Interface Dongle")
hcard,channel,core = openARINC249Card()
if hcard == -99:
  logger("Failed to open the ARINC-429 USB Interface Dongle")
  exit ()
else:
  logger("Success opening the ARINC-429 USB Interface Dongle")

# Open the session with the power supply for the VCO
pwrsupply = pyvisa.ResourceManager()
hmc8042 = pwrsupply.open_resource("TCPIP0::10.1.1.158::5025::SOCKET")
logger("Power Supply Resource Description: "+str(hmc8042))
hmc8042.read_termination = '\n'
hmc8042.write_termination = '\n'
logger("Turning the output power of both channels OFF and master power OFF")
hmc8042.write('OUTP:MAST OFF')
hmc8042.write('INST:SEL 1')
hmc8042.write('OUTP OFF')
hmc8042.write('INST:SEL 2')
hmc8042.write('OUTP OFF')


# Open the session with the onboard VCO attenuator (simulates onboard radalt)
VCOattenuator = pyvisa.ResourceManager()
rcdat6000 = VCOattenuator.open_resource("TCPIP0::10.1.1.159::23::SOCKET")
rcdat6000.read_termination = '\n'
rcdat6000.write_termination = '\n'
logger("Opened Minicircuit Attenuator for onboard VCO control")
logger("Attenuator description: " + str(rcdat6000))
logger("Clearing the input queue. Last return code is " + str(rcdat6000.read()))


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
# These are for bench test
#alt9000.write(":RALT:SET:CHAN1:LOSS:CABL:TX 1.3")
#alt9000.write(":RALT:SET:CHAN1:LOSS:CABL:RX 1.3")
#alt9000.write(":RALT:SET:CHAN1:LOSS:EXT:RX 9.7")

# These are for aircraft test with couplers and long cables
alt9000.write(":RALT:SET:CHAN1:LOSS:CABL:TX 0.9")
alt9000.write(":RALT:SET:CHAN1:LOSS:CABL:RX 0.9")
alt9000.write(":RALT:SET:CHAN1:LOSS:EXT:RX 8.9")
alt9000.write(":RALT:SET:CHAN1:LOSS:EXT:TX 1.9")
alt9000.write(":RALT:SET:CHAN1:LOSS:COUP:TX 0.0")
alt9000.write(":RALT:SET:CHAN1:LOSS:COUP:RX 0.0")

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

# Turn the power supply for the onboard VCO if the onboard VCO simulation flag is on
if includeOnBoard:
  logger("Onboard VCO simulation flag is True.  Turning on the onboard VCO power supply.")
  hmc8042.write('OUTP:MAST ON')
  hmc8042.write('INST:SEL 2')
  hmc8042.write('OUTP ON')
else:
  logger("Onboard VCO simulation flag is False.  Turningn OFF the onboard VCO power supply.")
  hmc8042.write('OUTP:MAST ON')
  hmc8042.write('INST:SEL 2')
  hmc8042.write('OUTP OFF')

logger("************************* START SIMULATION ****************************")
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

    # Set the attenuation of the onboard VCO to correspond to the simulated altitude if onboard simulation is turned on
    if includeOnBoard:
      logger("Setting the onboard VCO attenuator to " + str(onboardVCOatt(i)) + " dB.")
      rcdat6000.query(":CHAN:1:SETATT:" + str(onboardVCOatt(i)))
      logger("Attenuation is set to " + str(rcdat6000.query(":ATT?")))

    # Turn OFF the VCOs for the other planes alt radar simulators if altitude is above 200 feet
    if i > 200:
      logger("Altitude is above 200 feet. Turn OFF VCO Power Supply.")
      hmc8042.write('INST:SEL 1')
      hmc8042.write('OUTP OFF')
    else:
      # Turn ON the VCOs only if the flag to use VCOs in this simulation is set to True
      if includeVCO:
        logger("Altitude is below 200 feet. Turn ON VCO power supply.")
        hmc8042.write('OUTP:MAST ON')
        hmc8042.write('INST:SEL 1')
        hmc8042.write('OUTP ON')
      else:
        logger("VCO flag is OFF.  Keep VCO power supply OFF")
        hmc8042.write('INST:SEL 1')
        hmc8042.write('OUTP OFF')



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
      altitude = readARINCaltitude(channel,core)
      # This is the IBE power conversion
      print(float(timestamp),",0,",int(minpowerforplot),",", float(pwrtopsdFinalV3(minpowerforplot)),",",altitude,file=outfile)

      # This is the OOBE power conversion
      #print(float(timestamp),",0,",int(minpowerforplot),",", float(minpowerforplot - 7.75 - 20),",",altitude,file=outfile)
      
      if altitude > -90:
        basecumulative=basecumulative + altitude
        basesamples=basesamples + 1

      time.sleep(0.05)  # Sleep for 50 milliseconds.  The altitude is updated every 40 milliseconds

    baseaverage=basecumulative / basesamples  # Establish the average altitude baseline
    logger("Completed baseline performance. Average altitude is "+str(round(float(baseaverage),2))+" feet")
    logger("Start data collection")

    # Start the sweep

    for x in range(genminpower, genmaxpower):


      smcv.source.power.level.immediate.set_amplitude(x)
      
      logger("5G Center Frequency "+str(j)+" MHz, Altitude "+str(i)+" feet, 5G Output Power Level "+ str(x)+" dBm")
      smcv.output.state.set_value(True)
      time.sleep(waittostable)  # Wait before collecting sample to avoid any transient effects
      thissamples=0
      thisaverage=0.0
      thiscumulative=0.0
      temptime = time.time()
      while time.time() < temptime + rfonduration:
        timestamp = time.time() - init_ts
        altitude = readARINCaltitude(channel,core)
    #   This conversion is the standard conversion for IBE testing.    
        print(float(timestamp),",1,", int(x),",", float(pwrtopsdFinalV3(x)),",",altitude,file=outfile)

    #   This conversion was used at Calspsn for the OOBE testing.  The path losses are 6.4 dB and the conversion to dBm/MHz is 20 dB.
        #print(float(timestamp),",1,", int(x),",", float(x - 7.75 - 20),",",readARINCaltitude(channel,core),file=outfile)

        thissamples=thissamples + 1
        thiscumulative=thiscumulative + altitude

        time.sleep(0.05)  # Sleep for 50 milliseconds.  The altitude is updated every 40 milliseconds

      thisaverage=thiscumulative / thissamples  # Calculate the average altitude for this sweep

      logger("5G Generator RF Power Output OFF")
      temptime = time.time()
      smcv.output.state.set_value(False)   
      while time.time() < temptime + rfoffduration:
        timestamp = time.time() - init_ts
        altitude = readARINCaltitude(channel,core)

        # This has the standard conversion from 5G power out to PSD
        print(float(timestamp),",0,",int(minpowerforplot),",", float(pwrtopsdFinalV3(minpowerforplot)),",",altitude,file=outfile)

        # This conversion was used at Calspsn for the OOBE testing.  The path losses are 6.4 dB and the conversion to dBm/MHz is 20 dB.
        #print(float(timestamp),",0,", int(minpowerforplot),",", float(minpowerforplot - 7.75 - 20),",",readARINCaltitude(channel,core),file=outfile)

        time.sleep(0.05)  # Sleep for 50 milliseconds.  The altitude is updated every 40 milliseconds

      # Stop the test for this frequency and altitude combination if the altitude average exceeds a predefined threshold
      if (stopwhenexceed and ((abs(baseaverage - thisaverage)/baseaverage) > stopat)):
        logger("Stopped simulation on exceeding baseline average.  Baseline average = "+str(baseaverage)+" feet. This run average = "+str(thisaverage)+" feet.")
        logger("Stopped at "+str(x)+" dBm.  Min power for simulation is "+str(genminpower)+" dBm and Max power is "+str(genmaxpower)+" dBm.")

        break   # No need to go further as the radar failed the last power level tests
    
    outfile.close()


# Stop and close all instruments
hmc8042.write('OUTP:MAST OFF')
alt9000.write('RALT:TEST:RES')
time.sleep(2)
alt9000.write('RALT:TEST:STOP')
smcv.close()
closeARINC249Card(hcard,core)
# multimeter.close()
alt9000.close()
hmc8042.close()
rcdat6000.close()
logger("Total Simulation Time: "+str(round(time.time() - siminit,2))+" seconds.")
exit()





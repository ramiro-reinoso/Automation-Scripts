import keyboard
import os
import time

# import the VISA libraries to communicate with the Rigol multimeter
import pyvisa

from alt55B_volts_to_feet import voltstofeet

# Open the session with the Rigol multimeter
rigol = pyvisa.ResourceManager()
multimeter = rigol.open_resource("TCPIP0::10.1.1.155::inst0::INSTR")
multimeter.read_termination = '\n'
multimeter.write_termination = '\n'

# Setup variables for this simulation
folder="ALT-55B-Jul15-24-01"
radar="ALT-55B"
filedesc="50ft"
power5G=-99
collect_time=60 # Data collection elapsed time.

if not os.path.exists(folder):
    os.makedirs(folder)

filename=folder+"\\"+radar+"_"+filedesc+".csv"
outfile = open(filename,"w")

# Write the column headers in the results csv file
print("time,rfon,pwr,psd,alt",file=outfile)

init_time=time.time()

while time.time() < (init_time + collect_time):
    timestamp = time.time() - init_time
    print(float(timestamp),",0,",int(power5G),",", int(power5G),",",float(voltstofeet(multimeter.query(":measure:voltage:DC?"))),file=outfile)
    print("Time to finish "+ str(round(float(init_time+collect_time-time.time()),2)))
    
    # break if necessary
    if keyboard.is_pressed("q"):
        print("q pressed, ending loop")
        break

outfile.close()
multimeter.close()

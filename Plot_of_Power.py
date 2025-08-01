import pandas as pd
import json
import matplotlib.pyplot as plt

from powertopsd5g import pwrtopsdLabFilter


# Read the simulation configuratin from the JSON files
# Open the main config file and extract the jSON filename where the
# simulation parameters are defined
baseconfig=open('json_configs\\Statistics.json','r')
basedata=json.load(baseconfig)
filename=basedata['ConfigFile']
# Open the JSON file with he detail configuration parameters for the simulation
configfilename="json_configs\\"+filename
jsonfile=open(configfilename)
configs=json.load(jsonfile)

# Setup variables used in the simulation
folder = configs['folder']
radar = configs['radar']
genminpower=configs['genminpower']
genmaxpower = configs['genmaxpower']
genpoweroffdelta = configs['deltatopwroff']
altitudes = configs['altitudes']
frequencies = configs['frequencies']
psdonfile = configs['psdonfile']  # Earlier data collection files had no psd field, just power.
test5Gsignal = configs['5Gtestsignal']
filter5G = configs['5Gfilter']

if not psdonfile:
    print("WARNING *** WARNING *** WARNING *** WARNING *** WARNING *** WARNING *** WARNING *** ")
    print("WARNING: the 5G signal PSD will be re-calculated because it is not in the data collection file.")

# Set the minimum power when 5G generator is OFF
minpowerforplot = genminpower - genpoweroffdelta

if filter5G:
    filtered="with 5G Filter"
else:
    filtered="without 5G Filter"

# Check if the PSD in the CSV file needs to be adjusted and if it does to be adjusted,
# by how much
if "psdcorrection" in configs:
    psdadjust = configs["psdcorrection"]
else:
    psdadjust = 0.0

# Start the plots

for j in frequencies:
    simulation = test5Gsignal + " Centered at " + str(j) + " MHz " + filtered

    for x in altitudes:
        infilename=folder+"\\"+radar+"_"+str(j)+"_"+str(x)+".csv"
        outfilename=folder+"\\"+radar+"_"+str(j)+"_"+str(x)+".png"

        plottitle=radar+" at "+str(x)+" ft with "+simulation



        print("Processing "+infilename)
        simul=pd.read_csv(infilename)



        # Calculate the altitude range for plot
        altaxismax=simul["alt"].max()  # This is the maximum altitude collected
        altaxismax=altaxismax + 0.1*altaxismax # Give ourselves some room at the top
        altaxismin=simul["alt"].min()  # This is the minimum altitude collected
        altaxismin=altaxismin - 0.1*altaxismin # Give ourselves some room at the bottom

        if not psdonfile:
            simul["psd"] = simul["pwr"].apply(pwrtopsdLabFilter)

        # Adjust the psd of the data as per the config file
        simul["psd"] = simul["psd"] + psdadjust

        # Calculate power range for plot
        minplotpsd=simul["psd"].min() - 2   # Minimum PSD when 5G gen if OFF with a little more room.
        maxplotpsd=simul["psd"].max() + 2   # Maximum PSD when 5G gen is ON with a little more room.
        

        ax=simul.plot("time","alt",figsize=(8,4.5)) # Original size is (8,4.5)
        ax1=ax.twinx()
        simul.plot("time","psd",ax=ax1,color="orange")
        ax.legend().set_visible(False)
        ax1.legend().set_visible(False)
        ax.set_ylim([altaxismin,altaxismax])
        ax1.set_ylim([minplotpsd,maxplotpsd])
        ax.set_title(plottitle)
        ax.set_xlabel("Elapsed Time (seconds)",fontsize=8)
        ax.set_ylabel("Measured Altitude (feet)")
        ax1.set_ylabel("Interference PSD at Radalt Input (dBm/MHz)")
        ax.figure.savefig(outfilename,dpi=600) # Original dpi is 600
        plt.close()

exit()

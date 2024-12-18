import pandas as pd
import json
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator
import numpy as np

# Setup variables for this simulation
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
altitudes = configs['altitudes']
frequencies = configs['frequencies']
test5Gsignal = configs['5Gtestsignal']
filter5G = configs['5Gfilter']

if filter5G:
    filtered="with 5G Filter"
else:
    filtered="without 5G Filter"


# Start the plots

for j in frequencies:
    simulation = test5Gsignal + " Centered at " + str(j) + " MHz " + filtered

    for x in altitudes:
        infilename=folder+"\\"+radar+"_"+str(j)+"_"+str(x)+"_stats.csv"
        outfilename=folder+"\\"+radar+"_"+str(j)+"_"+str(x)+"_stats.png"

        plottitle=radar+" at "+str(x)+" ft with "+simulation

        print("Processing "+infilename)
        df=pd.read_csv(infilename)
        # Drop the first row which is the baseline row
        df = df.drop([0])
        
        # Create a figure with subplots
        fig,ax = plt.subplots(figsize=(8,4.5))

        # Create the vector for each of the series
        df1=df[['psd','meanerror']]
        df2=df[['psd','maxerror']]
        df3=df[['psd','minerror']]
        df4=df[['psd','ptile99therror']]
        df5=df[['psd','ptile1sterror']]

        # Plot the series using different colors and line patterns and using the same x axis
        df1.plot.line(ax=ax,x='psd',y=["meanerror"], linewidth= 1.5, linestyle='-', color='blue')
        df2.plot.line(ax=ax,x='psd',y=["maxerror"], linewidth= 1.5, color='black', linestyle='--')
        df3.plot.line(ax=ax,x='psd',y=["minerror"], linewidth= 1.5, color='black', linestyle='-.')
        df4.plot.line(ax=ax,x='psd',y=["ptile99therror"], linewidth= 1.5, color='green', linestyle='--')
        df5.plot.line(ax=ax,x='psd',y=["ptile1sterror"], linewidth= 1.5, color='green', linestyle='-.')

        plt.xlabel("PSD at Input of Radalt (dBm/MHz)")
        plt.ylabel("Percent Error with Respect to Baseline (%)")

        # ax.set_xticks(np.arange(0, 19, 1))
        # ax.set_xticks(np.arange(0, 19, 0.5), minor=True)
        #ax.set_xlim(0,25)
        ax.xaxis.set_major_locator(MultipleLocator(0.5))

        plt.ylim([-2.5,2.5])
        plt.grid(visible=True)
        plt.title(plottitle)

        #plt.show()

        plt.savefig(outfilename,dpi=600)
        plt.close()


exit()

import pandas as pd
import matplotlib.pyplot as plt

from powertopsd5g import pwrtopsdLabFilter

# Setup variables to match the simulation
folder="ALT-55B-May29-24-02"
radar="ALT-55B"
genminpower = -20
genmaxpower = -5
minpowerforplot = genminpower - 10

altitudes = [20,50,100,200,500,1000,2000,2500]
frequencies = [4030,4040,4050,4060,4070,4090]
psdonfile = True  # Earlier data collection files had no psd field, just power.

genpwrtopsd=16.8 # Add this to 5G gen power to get PSD min and max for the plot.

for j in frequencies:
    simulation="100 MHz TM1_1 Centered at "+str(j)+" MHz with Filter"

    # Calculated plot variables
    minplotpsd=minpowerforplot + genpwrtopsd - 2
    maxplotpsd=genmaxpower + genpwrtopsd

    for x in altitudes:
        infilename=folder+"\\"+radar+"_"+str(j)+"_"+str(x)+".csv"
        outfilename=folder+"\\"+radar+"_"+str(j)+"_"+str(x)+".png"

        plottitle=radar+" at "+str(x)+" ft with "+simulation



        print("Processing "+infilename)
        simul=pd.read_csv(infilename)

        altaxismax=simul["alt"].max()
        altaxismax=altaxismax + 0.1*altaxismax # Give ourselves some room at the top

        if not psdonfile:
            simul["psd"] = simul["pwr"].apply(pwrtopsdLabFilter)

        ax=simul.plot("time","alt",figsize=(8,4.5))
        ax1=ax.twinx()
        simul.plot("time","psd",ax=ax1,color="orange")
        ax.legend().set_visible(False)
        ax1.legend().set_visible(False)
        ax.set_ylim([0,altaxismax])
        ax1.set_ylim([minplotpsd,maxplotpsd])
        ax.set_title(plottitle)
        ax.set_xlabel("Elapsed Time (seconds)")
        ax.set_ylabel("Measured Altitude (feet)")
        ax1.set_ylabel("Interference PSD at Radalt Input (dBm/MHz)")
        ax.figure.savefig(outfilename,dpi=600)
        plt.close()

exit()

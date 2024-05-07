import pandas as pd
import matplotlib.pyplot as plt

# Setup variables to match the simulation
folder="ALT-55B-May07-24"
radar="ALT-55B"
genminpower = -35
genmaxpower = -20
minpowerforplot = genminpower - 10
genpwrtopsd=17.8 # Add this to 5G gen power to get PSD
#altitudes = [50,100,200,500,1000,2000,2500]
altitudes = [50,100]
simulation="100 MHz TM1_1 Centered at 3990 MHz"

# Calculated plot variables
minplotpsd=minpowerforplot + genpwrtopsd - 2
maxplotpsd=genmaxpower + genpwrtopsd

for x in altitudes:
    infilename=folder+"\\"+radar+"_"+str(x)+".csv"
    outfilename=folder+"\\"+radar+"_"+str(x)+".png"

    plottitle=radar+" at "+str(x)+" ft with "+simulation



    print("Processing "+infilename)
    simul=pd.read_csv(infilename)

    altaxismax=simul["alt"].max()
    altaxismax=altaxismax + 0.1*altaxismax # Give ourselves some room at the top

    simul["psd"] = simul["pwr"] + genpwrtopsd

    ax=simul.plot("time","alt")
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

exit()

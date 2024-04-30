import pandas as pd
import matplotlib.pyplot as plt

altitudes = [50,100,200,500,1000,2000,2500]
filefolder="ALT-55B-Apr29-24\\"

for x in altitudes:
    infilename=filefolder+"ALT-55B_"+str(x)+".csv"
    outfilename=filefolder+"ALT-55B_"+str(x)+".png"

    plottitle="ALT-55B at "+str(x)+" ft with 100 MHz TM1_1 Centered at 3990 MHz"

    altaxismax=x + 0.1*x

    print("Processing "+infilename)
    simul=pd.read_csv(infilename)

    simul["psd"] = simul["pwr"] - 8.5 -20.0

    ax=simul.plot("time","alt")
    ax1=ax.twinx()
    simul.plot("time","psd",ax=ax1,color="orange")
    ax.legend().set_visible(False)
    ax1.legend().set_visible(False)
    ax.set_ylim([0,altaxismax])
    ax1.set_ylim([-55,-20])
    ax.set_title(plottitle)
    ax.set_xlabel("Elapsed Time (seconds)")
    ax.set_ylabel("Measured Altitude (feet)")
    ax1.set_ylabel("Interference PSD at Radalt Input (dBm/MHz)")
    ax.figure.savefig(outfilename,dpi=600)

exit()

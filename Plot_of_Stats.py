import pandas as pd
import matplotlib.pyplot as plt

#altitudes = [50,100,200,500,1000,2000,2500]
altitudes = [50]
filefolder="ALT-55B-Apr29-24\\"

for x in altitudes:
    infilename=filefolder+"ALT-55B_"+str(x)+"_stats.csv"
    outfilename=filefolder+"ALT-55B_"+str(x)+"_stats.png"

    plottitle="ALT-55B at "+str(x)+" ft with 100 MHz TM1_1 Centered at 3990 MHz"

    print("Processing "+infilename)
    df=pd.read_csv(infilename)
    # Drop the first row which is the baseline row
    df = df.drop([0])
    
    stats=df[['psd','meanerror','maxerror','minerror','ptile99therror','ptile1sterror']].copy()
    print(stats)

    stats.plot('psd',title=plottitle,xlabel="PSD at Input of Radalt (dBm/MHz)",ylabel="Percent Error with Respect to Baseline (%)",
               ylim=[-100,10])
    
    # stats.title(plottitle)
    #stats.plot.xlabel("PSD at Input of Radalt (dBm/MHz)")
    # stats.ylabel("Percent Error with Respect to Baseline (%)")

    plt.show()

    #plt.savefig(outfilename,dpi=600)


exit()

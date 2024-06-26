import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator
import numpy as np

# Setup variables for this simulation
folder="ALT-55B-Jun14-24-03"
radar="ALT-55B"
genminpower = -20
genmaxpower = -5
minpowerforplot = genminpower - 10

frequencies = [4050,4100]
altitudes = [50,100,200]

for j in frequencies:
    for x in altitudes:
        infilename=folder+"\\"+radar+"_"+str(j)+"_"+str(x)+"_stats.csv"
        outfilename=folder+"\\"+radar+"_"+str(j)+"_"+str(x)+"_stats.png"

        plottitle=radar+": IBE Test 100 MHz 5G signal at Center Freq "+str(j)+" MHz for "+str(x)+" feet"

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

        plt.ylim([-80,80])
        plt.grid(visible=True)
        plt.title(plottitle)

        #plt.show()

        plt.savefig(outfilename,dpi=600)
        plt.close()


exit()

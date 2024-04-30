import pandas as pd
import matplotlib.pyplot as plt

simul=pd.read_csv("ALT-55B_50.csv")

simul["psd"] = simul["pwr"] - 8.5 -20.0

ax=simul.plot("time","alt")
ax1=ax.twinx()
simul.plot("time","psd",ax=ax1,color="orange")
ax.legend().set_visible(False)
ax1.legend().set_visible(False)
ax.set_ylim([0,50])
ax1.set_ylim([-55,-20])
ax.set_title("THIS IS THE TITLE")
ax.set_xlabel("Elapsed Time (seconds)")
ax.set_ylabel("Measured Altitude (feet)")
ax1.set_ylabel("Interference PSD at Radalt Input (dBm/MHz)")
ax.figure.savefig("myfirstplot.png")

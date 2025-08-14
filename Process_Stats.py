import pandas as pd
import json
from powertopsd5g import pwrtopsdFinalV3

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
filefolder = configs['folder']
radar = configs['radar']
genpoweroffdelta = configs['deltatopwroff']
altitudes = configs['altitudes']
frequencies = configs['frequencies']
psdonfile = configs['psdonfile']  # Earlier data collection files had no psd field, just power.

if not psdonfile:
    print("WARNING *** WARNING *** WARNING *** WARNING *** WARNING *** WARNING *** WARNING *** ")
    print("WARNING: the 5G signal PSD will be re-calculated because it is not in the data collection file.")

# Calculate the statistics

# Start frequency loop
for j in frequencies:
    
    for x in altitudes:
        infilename=filefolder+"\\"+radar+"_"+str(j)+"_"+str(x)+".csv"
        print(infilename)
        outfilename=filefolder+"\\"+radar+"_"+str(j)+"_"+str(x)+"_stats.csv"

        simul=pd.read_csv(infilename)

        # Compute the baseline statistics (the first 60 seconds with power OFF)
        base=simul[(simul["rfon"] == 0) & (simul["time"] < 65)]
        basemean=base["alt"].mean()
        base1stptile=base["alt"].quantile(0.01)
        base99thptile=base["alt"].quantile(0.99)
        basemin=base["alt"].min()
        basemax=base["alt"].max()
        basestd=base["alt"].std()

        outdf=pd.DataFrame({'pwr':["Baseline"],'psd':["Baseline"],'mean':[basemean],'1stptile':[base1stptile],'99thptile':[base99thptile],
                            'meantest':["N/A"],'1stptiletest':["N/A"],'99ptiletest':["N/A"],'min':[basemin],'max':[basemax],
                            'std':[basestd],'meanerror':["N/A"],'minerror':["N/A"],
                            'maxerror':["N/A"],'ptile1sterror':["N/A"],'ptile99therror':["N/A"],'stderror':["N/A"]})

        genminpower = simul['pwr'].min()
        genmaxpower = simul['pwr'].max()
        genminpower = genminpower + genpoweroffdelta

#        print("Min = "+str(genminpower)+" Max = "+str(genmaxpower))

        for i in range(genminpower,genmaxpower):
            tmppwr=simul[simul["pwr"] == i]

            thismean=tmppwr["alt"].mean()
            this1stptile=tmppwr["alt"].quantile(0.01)
            this99thptile=tmppwr["alt"].quantile(0.99)
            thismin=tmppwr['alt'].min()
            thismax=tmppwr['alt'].max()
            thisstd=tmppwr['alt'].std()   

            # Calculate test inputs
            meantest = abs(basemean - thismean)/thismean * 100
            ptile1sttest = basemean - (0.02 * basemean)
            ptile99thtest = basemean + (0.02 * basemean)

            # print("Power: ",str(i))
            # print(thismean)
            # print(this1stptile)
            # print(this99thptile)

            if meantest > 0.5:
                mtest="FAIL"
            else:
                mtest="PASS"

            if this1stptile < ptile1sttest:
                priptile1sttest="FAIL"
            else:
                priptile1sttest="PASS"

            if this99thptile > ptile99thtest:
                priptile99thtest="FAIL"
            else:
                priptile99thtest="PASS"

            # Error with respect to the baseline data
            meanerror = (basemean - thismean)/basemean * 100
            minerror = (basemin - thismin)/basemin * 100
            maxerror = (basemax - thismax)/basemax * 100
            ptile1sterror = (base1stptile - this1stptile)/base1stptile * 100
            ptile99therror = (base99thptile - this99thptile)/base99thptile * 100
            stderror = (basestd - thisstd)/basestd * 100

            if psdonfile:
                sig5gpsd = tmppwr['psd'].iloc[0]
            else:
                sig5gpsd = pwrtopsdFinalV3(i)

            tmprow={'pwr': i,'psd':round(sig5gpsd,1),'mean': round(thismean,1),'1stptile': round(this1stptile,1),'99thptile': round(this99thptile,1),
                            'meantest': mtest,'1stptiletest': priptile1sttest,'99ptiletest': priptile99thtest,
                            'min':round(thismin,1),'max':round(thismax,1),'std':round(thisstd,1),'meanerror':round(meanerror,1),'minerror':round(minerror,1),
                            'maxerror':round(maxerror,1),'ptile1sterror':round(ptile1sterror,1),'ptile99therror':round(ptile99therror,1),
                            'stderror':round(stderror,1)}
            
            outdf = outdf._append(tmprow, ignore_index=True)

        outdf.to_csv(outfilename)

exit()




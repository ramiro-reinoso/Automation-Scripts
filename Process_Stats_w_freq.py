import pandas as pd
from powertopsd5g import pwrtopsdLabFilter

altitudes = [20,50,100,200,500,1000,2000,2500]
frequencies = [4050,4100]
psdonfile = True  # Earlier data collection files had no psd field, just power.

filefolder="ALT-55B-Jun14-24-01"
radar="ALT-55B"
genminpower = -20
genmaxpower = -5
minpowerforplot = genminpower - 10
genpwrtopsd=14.3 # Add this to 5G gen power to get PSD unless using the pwrtopsd conversion



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
                sig5gpsd = pwrtopsdLabFilter(i)

            tmprow={'pwr': i,'psd':round(sig5gpsd,1),'mean': thismean,'1stptile': this1stptile,'99thptile': this99thptile,
                            'meantest': mtest,'1stptiletest': priptile1sttest,'99ptiletest': priptile99thtest,
                            'min':thismin,'max':thismax,'std':thisstd,'meanerror':meanerror,'minerror':minerror,
                            'maxerror':maxerror,'ptile1sterror':ptile1sterror,'ptile99therror':ptile99therror,
                            'stderror':stderror}
            
            outdf = outdf._append(tmprow, ignore_index=True)

        outdf.to_csv(outfilename)

exit()




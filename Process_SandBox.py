import pandas as pd

simul=pd.read_csv("ALT-55B_50.csv")



base=simul[(simul["rfon"] == 0) & (simul["time"] < 65)]
# print(base.head())
# print(base.describe())
basemean=base["alt"].mean()
base1stptile=base["alt"].quantile(0.01)
base99thptile=base["alt"].quantile(0.99)

outdf=pd.DataFrame({'pwr':["Baseline"],'mean':[basemean],'1stptile':[base1stptile],'99thptile':[base99thptile],
                    'meantest':["N/A"],'1stptiletest':["N/A"],'99ptiletest':["N/A"]})


for i in range(-15,4):
    tmppwr=simul[simul["pwr"] == i]

    thismean=tmppwr["alt"].mean()
    this1stptile=tmppwr["alt"].quantile(0.01)
    this99thptile=tmppwr["alt"].quantile(0.99)

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
        ptile1sttest="FAIL"
    else:
        ptile1sttest="PASS"

    if this99thptile > ptile99thtest:
        priptile99thtest="FAIL"
    else:
        ppriptile99thtest="PASS"

    tmprow={'pwr': i,'mean': thismean,'1stptile': this1stptile,'99thptile': this99thptile,
                    'meantest': mtest,'1stptiletest': ptile1sttest,'99ptiletest': ppriptile99thtest}
    
    outdf = outdf._append(tmprow, ignore_index=True)

print(outdf)
exit()




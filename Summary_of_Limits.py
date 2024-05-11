import pandas as pd

altitudes = [50,100,200,500,1000,2000,2500]
filefolder="ALT-55B-May10-24-03"
radar="ALT-55B"

genpwrtopsd=17.8 # Add this to 5G gen power to get PSD

# Crate the output filename
outfilename=filefolder+"\\"+radar+"_summary.csv"

# Create the output Pandas DataFrame
outdf=pd.DataFrame({'alt':[],'fail':[],'mean':[],'1stptile':[],'99thptile':[],
                        'lastgood':[],'limit':[]})

# Calculate the statistics

for x in altitudes:
    # Open the statistics file for this altitude and create a Pandas DataFrame
    infilename=filefolder+"\\"+radar+"_"+str(x)+"_stats.csv"
    stats=pd.read_csv(infilename)

    # Drop the first row as it contains the baseline statistics which we don't need
    stats = stats.drop([0])
    print(stats)
    stats["pwr"] = pd.to_numeric(stats["pwr"],downcast="integer")
    stats["psd"] = pd.to_numeric(stats["psd"])

    # Set the range for min power and max power for the for loop
    genminpower = stats["pwr"].min()
    genmaxpower = stats["pwr"].max()
    genmaxpower = genmaxpower + 1

    print(genmaxpower)
    print(genminpower)


    mflag = False
    p1flag = False
    p99flag = False
    m = ""
    p1 = ""
    p99 = ""
    psd = 0

    for i in range(genminpower,genmaxpower):
    
        tmppwr=stats[stats["pwr"] == i]
        print(tmppwr)
        index = abs(genminpower) + i + 1
        print(index)

        meantest = tmppwr.loc[index,"meantest"]
        p1test = tmppwr.loc[index,"1stptiletest"]
        p99test = tmppwr.loc[index,"99ptiletest"]
        psd = tmppwr.loc[index,"psd"]

        if meantest == "FAIL":
            mflag = True
            m = "*"

        if p1test == "FAIL":
            p1flag = True
            p1 = "*"

        if p99test == "FAIL":
            p99flag = True
            p99 = "*"

        if mflag or p1flag or p99flag:
            break

    if not mflag and not p1flag and not p99flag:
        fail = "NF"
        good = psd
    else:
        fail = psd
        good = psd - 1
    
    {'alt':[],'fail':[],'mean':[],'1stptile':[],'99thptile':[],
                        'lastgood':[],'limit':[]}
    tmprow={'alt': x,'fail': fail,'mean': m,'1stptile': p1,'99thptile': p99,
                        'lastgood': good,'limit': "N/A"}
        
    outdf = outdf._append(tmprow, ignore_index=True)

outdf.to_csv(outfilename)

exit()




import pandas as pd

altitudes = [50]
frequencies = [4030,4040,4050,4060,4070,4080,4090,4100,4110,4120,4130]

filefolder="ALT-55B-May14-24-01"
radar="ALT-55B"

genpwrtopsd=17.8 # Add this to 5G gen power to get PSD

# Crate the output filename
outfilename=filefolder+"\\"+radar+"_summary.csv"

# Create the output Pandas DataFrame
outdf=pd.DataFrame({'freq':[],'alt':[],'fail':[],'mean':[],'1stptile':[],'99thptile':[],
                        'lastgood':[],'limit':[]})

# Calculate the statistics

# Loop through all frequencies

for j in frequencies:

    for x in altitudes:
        # Open the statistics file for this altitude and create a Pandas DataFrame
        infilename=filefolder+"\\"+radar+"_"+str(j)+"_"+str(x)+"_stats.csv"
        stats=pd.read_csv(infilename)

        # Drop the first row as it contains the baseline statistics which we don't need
        stats = stats.drop([0])

        # Convert the power and psd columnt to integer and float respectively
        stats["pwr"] = pd.to_numeric(stats["pwr"],downcast="integer")
        stats["psd"] = pd.to_numeric(stats["psd"])

        # Set the range for min power and max power for the for loop
        genminpower = stats["pwr"].min()
        genmaxpower = stats["pwr"].max()
        genmaxpower = genmaxpower + 1

        mflag = False
        p1flag = False
        p99flag = False
        m = ""
        p1 = ""
        p99 = ""
        psd = 0.0

        for i in range(genminpower,genmaxpower):
        
            # Filter the dataframe to find the row that corresponds to the power level
            # of interest.
            tmppwr=stats[stats["pwr"] == i]

            # Calculate the index that correspond to the row of the selected power level.
            # Even thouth the tmppwr vector has only one row, the index of that row is not
            # zero but whatever the index was on the stats dataframe.
            index = abs(genminpower) + i + 1

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
        
        tmprow={'freq':j,'alt': x,'fail': fail,'mean': m,'1stptile': p1,'99thptile': p99,
                            'lastgood': good,'limit': "N/A"}
            
        outdf = outdf._append(tmprow, ignore_index=True)

outdf.to_csv(outfilename)

exit()




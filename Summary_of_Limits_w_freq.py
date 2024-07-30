import pandas as pd
import json

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
altitudes = configs['altitudes']
frequencies = configs['frequencies']

# Create the output filename
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

        # Test if there are no rows in the dataframe.  If the dataframe is empty,
        # process the next file
        if stats.shape[0] < 2:
            continue

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
                            'lastgood': round(good,1),'limit': "N/A"}
            
        outdf = outdf._append(tmprow, ignore_index=True)

print("\nCompleted processing.  Results are written to " + outfilename)

outdf.to_csv(outfilename)

exit()




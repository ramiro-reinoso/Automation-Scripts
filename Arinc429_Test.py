import sys
sys.path.append('USB_ARINC_Bus_Interface/')

import time

from UA2000_Interface import openARINC249Card
from UA2000_Interface import readARINCaltitude
from UA2000_Interface import closeARINC249Card


hcard,channel,core = openARINC249Card()

#print(hcard,channel,core)

for i in range(100):
    alt = readARINCaltitude(channel,core)
    
    match (alt):
        case -99:
            print("System error reading data")
            next
        case -1:
            print("NCD")
            next
    
    print("Altitude = ",alt)
    time.sleep(1)

closeARINC249Card(hcard,core)

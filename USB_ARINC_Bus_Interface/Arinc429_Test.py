import sys
sys.path.append('USB_ARINC_Bus_Interface/')

import time

from UA2000_Interface import openARINC249Card
from UA2000_Interface import readARINCaltitude
from UA2000_Interface import closeARINC249Card


hcard,channel,core = openARINC249Card()

print(hcard,channel,core)

for i in range(1):
    print(readARINCaltitude(channel,core))
    
time.sleep(2)
closeARINC249Card(hcard,core)

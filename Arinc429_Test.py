from UA2000_Interface import openARINC249Card
from UA2000_Interface import readARINCaltitude
from UA2000_Interface import closeARINC249Card


hcard,channel,core = openARINC249Card()

for i in range(10):
    print(readARINCaltitude(channel,core))

closeARINC249Card()

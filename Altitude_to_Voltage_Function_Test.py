# import local functions
from alt55B_volts_to_feet import voltstofeet

for i in range(0,100):
    print(str(i/100)+"="+str(voltstofeet(i/100)))

    
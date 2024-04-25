from alt55B_volts_to_feet import voltstofeet

for x in range (0,164,10):
	print(int(x),float(voltstofeet(x/10)))
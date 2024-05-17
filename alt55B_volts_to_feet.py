def voltstofeet(volts):
  volts = float(volts)

  if volts < 10.4:
    volts_to_feet = (volts / 20 * 1000) - 20
  elif volts < 16.5:
    volts_to_feet = (500 + (volts - 10.4) / 3 * 1000)
  else:
    volts_to_feet = -999
 
  return volts_to_feet

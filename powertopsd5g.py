# This function converts the output power setting at the 5G generator to
# power spectral density at the input of the altimeter radar.
# Not implemented yet on the tools because the difference between the linear
# region and the -11 dBm maximum test point is only 0.3 dB.  The conversion
# factor in the linear region is 16.8 dB versus 16.5 dB at 11 dBm of output power.

# VERSION: Red MFC filters May 23-25, 2024

def pwrtopsd(power):
  power = float(power)
  psd = -999

  if power < -12.0:
    psd = power + 14.6
  elif ((power >= -12.0) and (power < -11.0)):
    psd = power + 14.3
  elif (power >= -11.0) and (power < -10.0):
    psd = power + 13.9
  elif (power >= -10.0) and (power < -9.0):
    psd = power + 13.6
  elif (power >= -9.0) and (power < -8.0):
    psd = power + 13.3
  elif (power >= -8.0) and (power < -7.0):
    psd = power + 13.0
  elif (power >= -7.0) and (power < -6.0):
    psd = power + 12.6
  elif (power >= -6.0) and (power < -5.0):
    psd = power + 12.2
  else:
    psd = -999.0

  return psd

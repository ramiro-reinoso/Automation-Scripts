# This function converts the output power setting at the 5G generator to
# power spectral density at the input of the altimeter radar.
# There are different versions depending on the filers and configuration of the testbed

# VERSION: Red MFC filters May 23-25, 2024.  This was used to validate the AVSI results at
# frequencies 3870 MHz and 3930 MHz.
def pwrtopsdRedFilter(power):
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

# VERSION: This is using the filters designed for the testbed with sharp cutoffs to block
# all OOBE emissions.  These filter cutoff is at 3940 MHz.
def pwrtopsdLabFilter(power):
  power = float(power)
  psd = -999

  if power < -12.0:
    psd = power + 16.7
  elif ((power >= -12.0) and (power < -11.0)):
    psd = power + 16.3
  elif (power >= -11.0) and (power < -10.0):
    psd = power + 16.2
  elif (power >= -10.0) and (power < -9.0):
    psd = power + 15.9
  elif (power >= -9.0) and (power < -8.0):
    psd = power + 15.6
  elif (power >= -8.0) and (power < -7.0):
    psd = power + 15.4
  elif (power >= -7.0) and (power < -6.0):
    psd = power + 14.9
  elif (power >= -6.0) and (power < -5.0):
    psd = power + 14.4
  else:
    psd = -999.0

  return psd

# VERSION Final V1: This is using the filters designed for the testbed with sharp cutoffs to block
# all OOBE emissions.  These filter cutoff is at 3940 MHz.  In addition, this version also uses
# the Pasternack waveguide adapters for the filters, all four waveguide adapters.  Previous versions
# used the two Maury calibrated waveguide adapters while waiting for the Pasternack lab adapters.
# Calibration data collected on June 26.
def pwrtopsdFinalV1(power):
  power = float(power)
  psd = -999

  if power < -12.0:
    psd = power + 18.3
  elif ((power >= -12.0) and (power < -11.0)):
    psd = power + 18.1
  elif (power >= -11.0) and (power < -10.0):
    psd = power + 17.9
  elif (power >= -10.0) and (power < -9.0):
    psd = power + 17.7
  elif (power >= -9.0) and (power < -8.0):
    psd = power + 17.4
  elif (power >= -8.0) and (power < -7.0):
    psd = power + 17.2
  elif (power >= -7.0) and (power < -6.0):
    psd = power + 16.8
  elif (power >= -6.0) and (power < -5.0):
    psd = power + 16.4
  elif (power >= -5.0) and (power < -4.0):
    psd = power + 15.9
  elif (power >= -4.0) and (power < -3.0):
    psd = power + 15.3
  elif (power >= -3.0) and (power < -2.0):
    psd = power + 14.8
  elif (power >= -2.0) and (power < -1.0):
    psd = power + 14.2
  elif (power >= -1.0) and (power < 0.0):
    psd = power + 13.5
  else:
    psd = -999.0

  return psd
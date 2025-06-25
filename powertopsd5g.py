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
# Correction for the monitoring port is 33.8 dB when a 30 dB attenuator is connected to it.
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

# VERSION Final V2: This version is based on the configuration for V1 but with isolators installed at the input of the
# combiner port coming from the ALT-9000 receive port and the input of the combiner coming from the RF amplifier.  These 
# isolators added insertion loss and hence the need to re-calibrate.
# The calibration used a 5G 100 MHz signal centered at 4300 MHz.
# Calibration data collected on December 18, 2024.
# 
def pwrtopsdFinalV2(power):
  power = float(power)
  psd = -999

  if power < -12.0:
    psd = power + 17.5
  elif ((power >= -12.0) and (power < -11.0)):
    psd = interpol(power,-12.0,17.5,-11.0,17.2)
  elif (power >= -11.0) and (power < -10.0):
    psd = interpol(power,-11.0,17.2,-10.0,17.0)
  elif (power >= -10.0) and (power < -9.0):
    psd = interpol(power,-10.0,17.0,-9.0,16.7)
  elif (power >= -9.0) and (power < -8.0):
    psd = interpol(power,-9.0,16.7,-8.0,16.4)
  elif (power >= -8.0) and (power < -7.0):
    psd = interpol(power,-8.0,16.4,-7.0,16.0)
  elif (power >= -7.0) and (power < -6.0):
    psd = interpol(power,-7.0,16.0,-6.0,15.5)
  elif (power >= -6.0) and (power < -5.0):
    psd = interpol(power,-6.0,15.5,-5.0,15.0)
  elif (power >= -5.0) and (power < -4.0):
    psd = interpol(power,-5.0,15.0,-4.0,14.4)
  elif (power >= -4.0) and (power < -3.0):
    psd = interpol(power,-4.0,14.4,-3.0,13.8)
  elif (power >= -3.0) and (power < -2.0):
    psd = interpol(power,-3.0,13.8,-2.0,13.1)
  elif (power >= -2.0) and (power < -1.0):
    psd = interpol(power,-2.0,13.1,-1.0,12.45)
  elif (power >= -1.0) and (power <= 0.0):
    psd = interpol(power,-1.0,12.45,0.0,11.65)
  else:
    psd = -999.0

  return psd

# VERSION Final V3: This version is based on the configuration for V2 but 
# with new filters on the input and output of RF amplifier going to 
# 4200 MHz (instead of the 4180 MHz of V1).
# The calibration used a 5G 100 MHz signal centered at 4100 MHz.
# Calibration data collected on June 24, 2025.
# 
def pwrtopsdFinalV3(power):
  power = float(power)
  psd = -999

  if power < -12.0:
    psd = power + 15.5
  elif ((power >= -12.0) and (power < -11.0)):
    psd = interpol(power,-12.0,15.5,-11.0,15.3)
  elif (power >= -11.0) and (power < -10.0):
    psd = interpol(power,-11.0,15.3,-10.0,15.1)
  elif (power >= -10.0) and (power < -9.0):
    psd = interpol(power,-10.0,15.1,-9.0,14.7)
  elif (power >= -9.0) and (power < -8.0):
    psd = interpol(power,-9.0,14.7,-8.0,14.4)
  elif (power >= -8.0) and (power < -7.0):
    psd = interpol(power,-8.0,14.4,-7.0,14.0)
  elif (power >= -7.0) and (power < -6.0):
    psd = interpol(power,-7.0,14.0,-6.0,13.5)
  elif (power >= -6.0) and (power < -5.0):
    psd = interpol(power,-6.0,13.5,-5.0,13.0)
  elif (power >= -5.0) and (power < -4.0):
    psd = interpol(power,-5.0,13.0,-4.0,12.5)
  elif (power >= -4.0) and (power < -3.0):
    psd = interpol(power,-4.0,12.5,-3.0,11.9)
  elif (power >= -3.0) and (power < -2.0):
    psd = interpol(power,-3.0,11.9,-2.0,11.4)
  elif (power >= -2.0) and (power < -1.0):
    psd = interpol(power,-2.0,11.4,-1.0,10.5)
  elif (power >= -1.0) and (power <= 0.0):
    psd = interpol(power,-1.0,10.5,0.0,9.8)
  else:
    psd = -999.0

  return psd



def interpol(pwr,lowbound,lowlimit,highbound,highlimit):
  pwr=float(pwr)
  lowlimit=float(lowlimit)
  highlimit=float(highlimit)
  lowbound=float(lowbound)
  highbound=float(highbound)

  rate=(highlimit - lowlimit) / (highbound - lowbound)

  return pwr + lowlimit + rate * (pwr - lowbound)


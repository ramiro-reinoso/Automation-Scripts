def pwrtopsd(power):
  power = float(power)
  psd = -999

  if power < -12.0:
    psd = power + 16.8
  elif ((power >= -12.0) and (power < -11.0)):
    psd = 4.6 + 0.9 * (power + 12.0)
    print("In the routing power of -12 JAJA "+str(power))
  elif (power >= -11.0) and (power < -10.0):
    psd = 5.5 + 0.7 * (power + 11.0)
  elif (power >= -10.0) and (power < -9.0):
    psd = 6.2 + 0.9 * (power + 10.0)
  elif (power >= -9.0) and (power < -8.0):
    psd = 7.1 + 0.7 * (power + 9.0)
  elif (power >= -8.0) and (power < -7.0):
    psd = 7.8 + 0.6 * (power + 8.0)
  elif (power >= -7.0) and (power < -6.0):
    psd = 8.4 + 0.6 * (power + 7.0)
  elif (power >= -6.0) and (power < -5.0):
    psd = 9.0 + 0.5 * (power + 6.0)
  elif (power >= -5.0) and (power < -4.0):
    psd = 9.5 + 0.5 * (power + 5.0)
  elif (power >= -4.0) and (power < -3.0):
    psd = 10.0 + 0.3 * (power + 4.0)
  elif (power >= -3.0) and (power < -2.0):
    psd = 10.3 + 0.4 * (power + 3.0)
  elif (power >= -2.0) and (power < -1.0):
    psd = 10.7 + 0.4 * (power + 2.0)
  elif (power >= -1.0) and (power <= 0.0):
    psd = 11.1 + 0.2 * (power + 1.0)
  else:
    psd = -999.0

  return psd

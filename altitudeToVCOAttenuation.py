# This function provides the attenuation setting for the VCO simulating the on-board radalt
# given a simulated altitude.

def onboardVCOatt(altitude):
    altitude = float(altitude)
    attenuation = 90.0  # In case of error, return the highest attenuation (safer option)

    if ((altitude >= 20.0) and (altitude < 50.0)):
        attenuation = 6.6
    elif (altitude >= 50.0) and (altitude < 100.0):
        attenuation = 15.5
    elif (altitude >= 100.0) and (altitude < 200.0):
        attenuation = 22.0
    elif (altitude >= 200.0) and (altitude < 500.0):
        attenuation = 28.0
    elif (altitude >= 500.0) and (altitude < 1000.0):
        attenuation = 36.0
    elif (altitude >= 1000.0) and (altitude < 1500.0):
        attenuation = 42.0
    elif (altitude >= 1500.0) and (altitude < 2000.0):
        attenuation = 45.6
    elif (altitude >= 2000.0) and (altitude < 2500.0):
        attenuation = 48.0
    elif (altitude >= 2500.0) and (altitude < 3000.0):
        attenuation = 50.0
    else:
        attenuation = 90.0

    return attenuation
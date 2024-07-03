from powertopsd5g import pwrtopsdFinalV1
from altitudeToVCOAttenuation import onboardVCOatt

print("\n\nTesting 5G output power to PSD at Radalt Input")
for i in range (-25,0):
    print("5G Generator Output Power: "+str(i)+" 5G PSD at Radalt Input: "+str(round(pwrtopsdFinalV1(i),1)))

print("\n\nTesting altitude to onboard VCO attenuation")
for i in [20,50,100,200,500,1000,1500,2000,2500]:
    print("altitude: " + str(i) + " VCO atttenuation: " + str(onboardVCOatt(i)))
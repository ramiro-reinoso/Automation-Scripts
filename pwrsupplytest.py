import pyvisa
import time

pwrsupply = pyvisa.ResourceManager()
print("Power supply resource list: "+str(pwrsupply.list_resources()))
hmc8042 = pwrsupply.open_resource("TCPIP0::10.1.1.158::5025::SOCKET")
print("Resource Description: "+str(hmc8042))

hmc8042.read_termination = '\n'
hmc8042.write_termination = '\n'

hmc8042.write('INST:SEL 1')
print("Instrument Selected: "+str(hmc8042.query('INSTrument:SEL?')))

hmc8042.write('INST:SEL 1')
print("Voltage Channel 1: "+str(hmc8042.query('VOLT?')))


hmc8042.write('INST:SEL 2')
print("Voltage Channel 2: "+str(hmc8042.query('VOLT?')))

hmc8042.write('OUTP:MAST ON')
hmc8042.write('INST:SEL 1')
hmc8042.write('OUTP ON')

time.sleep(5)

hmc8042.write('OUTP:MAST OFF')
hmc8042.write('INST:SEL 1')
hmc8042.write('OUTP OFF')

hmc8042.close()
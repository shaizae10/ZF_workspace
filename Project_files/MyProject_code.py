from skidl import *

# Create the parts
led = Part('device', 'LED')

# Create the circuit
net_5v = Net('5V')
net_gnd = Net('GND')

led[1] += net_5v
led[2] += net_gnd

# Define waveforms for blinking
net_blink = Net('BLINK')


led[1] & net_blink & Net()

Circuit('blinking_led', led, net_5v, net_gnd, net_blink)
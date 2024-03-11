from skidl import *

# Create a circuit with a resistor, LED, and a voltage source
net_5v = Net('5V')
net_gnd = Net('GND')

led = Part('device', 'LED')
resistor = Part('device', 'R', value='220 ohm')
voltage_source = Part('device', 'V', value='5V')

led[1] += resistor[1], net_gnd
led[2] += net_5v
resistor[2] += voltage_source[1]
net_gnd += voltage_source[2]

# Blink the LED using a pulse voltage source
pulse_source = PulseVoltageSource('5V', pulsewidth='1ms', period='2ms')

led[1] += pulse_source['~']

ERC()
generate_netlist()
from skidl import *

# Define components
resistor = Part('device', 'R', footprint='Resistor_SMD:R_0805')
led = Part('device', 'LED', footprint='LED:LED_0805')
buzzer = Part('device', 'Buzzer', footprint='Buzzer:Buzzer_SMD')
capacitor = Part('device', 'C', footprint='Capacitor_SMD:C_0805')

# Connections
net_5v = Net('5V')
net_gnd = Net('GND')
net_sig = Net('SIG')

res1 = resistor(value='1k', ref='R1', pin_nums=['1', '2'])
led1 = led(ref='LED1', pin_nums=[1, 2])
buzzer1 = buzzer(ref='BUZZER1', pin_nums=[1, 2])
cap1 = capacitor(value='100n', ref='C1', pin_nums=['1', '2'])

buzzer1[2] += net_5v & net_gnd
led1[2] += net_5v & net_gnd
res1[1,2] += net_5v
cap1[1,2] += net_gnd

# Generate the netlist and print it to the console
generate_netlist()
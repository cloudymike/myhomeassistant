# A simple testexample of using a volt meter for input power

#Resistors:
#100k Vinput to pin 0
#10K GND to pin 0


adc=machine.ADC(0)
adc.atten(machine.ADC.ATTN_11DB)

volts=adc.read_uv()*11/1000
print('{} V'.format(round(volts,0))
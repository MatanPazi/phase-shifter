import numpy as np
from matplotlib import pyplot as plt
# Vout = mVin + b
# Input and output voltage ranges
Voh = 2.5   # Output high
Vol = 0.3   # Output low
Vih = 2.3   # Input high
Vil = 2.2   # Input low
Vref = 5    # Available reference voltage
maxVar = 0.05

m = (Voh - Vol)/(Vih - Vil)
b = Vol -m*Vil

# Positive Slope (m) and negative offset (b) equations:
# See "Op-Amp Gain and Offset Design with the HP-41C Programmable Calculator":
#   http://www.stefanv.com/calculators/hp41c_offset_gain.html
# And "Designing Gain and Offset in Thirty Seconds":
#   https://www.ti.com/lit/an/sloa097/sloa097.pdf?ts=1704077196109&ref_url=https%253A%252F%252Fwww.google.com%252F

# Choose R1 and Rf, then calculate R2 and Rg
R1 = 10000
Rf = 100000
R2 = -b*R1/((m-1)*Vref + b)
Rg = (b*R1 + Vref*Rf)/((m-1)*Vref)
print(R2, Rg)
t = np.linspace(0,1)
Vin = 0.05*np.sin(t*2*np.pi) + 2.25

# plt.plot(Vin)
# plt.show()
plt.figure(1)
Vout = Vin * (Rf+Rg+(R1*R2)/(R1+R2))/(Rg+(R1*R2)/(R1+R2)) - Vref * (R2*Rf)/((R1+R2) * (Rg + (R1*R2)/(R1+R2)))
plt.plot(Vin, label="Input signal")
plt.plot(Vout, label="Output signal - No variance")

R1 = R1 * (1+maxVar)
Rf = Rf * (1+maxVar)
R2 = R2 * (1-maxVar)
Rg = Rg * (1+maxVar)
VoutVar = Vin * (Rf+Rg+(R1*R2)/(R1+R2))/(Rg+(R1*R2)/(R1+R2)) - Vref * (R2*Rf)/((R1+R2) * (Rg + (R1*R2)/(R1+R2)))
plt.plot(VoutVar, label="Output signal - 5% variance")
plt.legend()
# plt.figure(2)
# diff = Vout - VoutVar
# plt.plot(diff)
plt.show()
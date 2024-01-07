# Script used to find resistor values for signal gain and offset using an Op-Amp
# Sources:
#   Positive Slope (m) and negative offset (b) equations:
#   See "Op-Amp Gain and Offset Design with the HP-41C Programmable Calculator":
#     http://www.stefanv.com/calculators/hp41c_offset_gain.html
#   And "Designing Gain and Offset in Thirty Seconds":
#     https://www.ti.com/lit/an/sloa097/sloa097.pdf?ts=1704077196109&ref_url=https%253A%252F%252Fwww.google.com%252F


import numpy as np

from matplotlib import pyplot as plt

def closest(lst, val):     
    return lst[min(range(len(lst)), key = lambda i: abs(lst[i]-val))]


# Input and output voltage ranges
Voh = 2.5   # Output high
Vol = 0.3   # Output low
Vih = 2.3   # Input high
Vil = 2.2   # Input low
Vref = 5    # Available reference voltage
maxVar = 1  # %

# Vout = m*Vin + b
m = (Voh - Vol)/(Vih - Vil)
b = Vol -m*Vil


# List of available resistors:
resInitList = [5100, 6800, 47000, 68000]
# E24 Resistors
# resInitList = [100,     110,    120,    130,    150,    160,    180,    200,    220,    240,    270,    300,    330,    360,    390,    430,    470,    510,    560,    620,    680,    750,    820,    910,
#                1000,    1100,   1200,   1300,   1500,   1600,   1800,   2000,   2200,   2400,   2700,   3000,   3300,   3600,   3900,   4300,   4700,   5100,   5600,   6200,   6800,   7500,   8200,   9100,
#                10000,   11000,  12000,  13000,  15000,  16000,  18000,  20000,  22000,  24000,  27000,  30000,  33000,  36000,  39000,  43000,  47000,  51000,  56000,  62000,  68000,  75000,  82000,  91000]

resList = []
for i in range(len(resInitList)):
    res1 = resInitList[i]
    resList.append(res1)

    ## Decide if you want to allow for a combination of up to 2 resistors (series / parallel):
    for j in range(i, len(resInitList)):
        res2 = resInitList[j]
        series = res2 + res1
        parallel = int(1 / ((1 / res2) + (1 / res1)))
        resList.append(series)
        resList.append(parallel)


# Generating the input and output signals:
t = np.linspace(0,1)
# Input signal
Vin = ((Vih - Vil)/2)*np.sin(t*2*np.pi) + ((Vih + Vil)/2)
# Desired output signal
VoutDesired = ((Voh - Vol)/2)*np.sin(t*2*np.pi) + ((Voh + Vol)/2)


# Running over all possible resistor combinations to find output signal closest to the desired output signal
costMin = 100  # Init value
R1Fin = 0
RfFin = 0
R2Fin = 0
RgFin = 0

for R1 in resList:    
    for Rf in resList:
        # Equations from first source mentioned above
        R2Temp = -b*R1 / ((m-1)*Vref + b)
        if R2Temp < 0:
            continue

        RgTemp = (b*R1 + Vref*Rf)/((m-1)*Vref)
        if RgTemp < 0:
            continue

        # Finding the closest available resistors to the ones found from the equations
        R2 = closest(resList, R2Temp)
        Rg = closest(resList, RgTemp)
        
        Vout = Vin * (Rf+Rg+(R1*R2)/(R1+R2))/(Rg+(R1*R2)/(R1+R2)) - Vref * (R2*Rf)/((R1+R2) * (Rg + (R1*R2)/(R1+R2)))
        cost = sum((Vout - VoutDesired)**2)
        if cost < costMin:
            costMin = cost
            VoutFin = Vout
            R1Fin = R1
            RfFin = Rf
            R2Fin = R2
            RgFin = Rg

print(R1Fin, RfFin, R2Fin, RgFin)

plt.plot(Vin, label="Input signal")
plt.plot(VoutFin, label="Output signal - No variance")
plt.plot(VoutDesired, label="Desired output signal")

# Adding variance
# R1Fin = R1Fin * (1+maxVar/100)
# RfFin = RfFin * (1+maxVar/100)
# R2Fin = R2Fin * (1+maxVar/100)
# RgFin = RgFin * (1+maxVar/100)
# VoutVar = Vin * (RfFin+RgFin+(R1Fin*R2Fin)/(R1Fin+R2Fin))/(RgFin+(R1Fin*R2Fin)/(R1Fin+R2Fin)) - Vref * (R2Fin*RfFin)/((R1Fin+R2Fin) * (RgFin + (R1Fin*R2Fin)/(R1Fin+R2Fin)))
# plt.plot(VoutVar, label="Output signal - 1% variance")

plt.legend()
plt.show()

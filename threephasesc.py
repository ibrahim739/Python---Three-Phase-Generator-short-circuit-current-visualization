# This script calculate and visualize a Three-Phase Generator bolted short circuit current.

#--------------------------------------------------------------------------------------------------------
# Brief explanation:
# The ac fault current in a synchronous machine can be modeled by the
# series R–L circuit if a time-varying inductance L(t) or reactance
# X(t) = w*L(t) is employed. In standard machine theory texts, the
# following reactances are defined:
# X''d = direct axis subtransient reactance ; T''d: direct axis short circuit subtransient time constant
# X'd = direct axis transient reactance ; T’d: direct axis short circuit transient time constant
# Xa = direct axis synchronous reactance ; Ta: Armature short circuit time constant
# where X''d < X'd < Xd . The subscript d refers to the direct axis.
# There are similar quadrature axis reactances X''q, Xq, and Xq.
# However, if the armature resistance is small, the quadrature axis reactances
# do not significantly affect the short-circuit current.

# ---------------------------------------------------------------------------------------------------------------
# Assumptions:
# We neglecte the effect of q axis due that they don't significantly affect
# the short circuit current as explained before.
# We assume maximum dc offset to obtain the worst short circuit case

# ---------------------------------------------------------------------------------------------------------------------
# The inputs to the script are:

S = input('Please enter the apparent power S in Va:')
Ug = input('Please enter the rms voltage in volt:')
percentageEg = input('Please enter the the generator percentage operating voltage compared to the rated voltage:')
f = input('Please enter the working frequency in hertz:')
Xsecond = input('Please enter the subtransient reactance in p.u:')
Xprime = input('Please enter the transient reactance in p.u:')
Xd = input('Please enter the synchronous reactance in p.u:')
Tsecond = input('Please enter the subtransient time constant in second:')
Tprime = input('Please enter the transient time constant in second: ')
Ta = input('Please enter the Armature time constant in second:')

# S which is the base apparent power in VA
# Ug is the Voltage in V
# percentageEg is the generator percentage operating voltage. For example:
# if The generator is operating at 5% above rated voltage, then
# percentageEg = 0.05, if the generator is operating at the rated voltage
# then percentageEg = 0 .
# f: working frequency in hertz
# Xsecond(x''d): direct axis subtransient reactance in p.u
# Xprime(x'd): direct axis transient reactance in p.u
# Xd(xd): direct axis synchronous reactance in p.u
# Tsecond(T''d): direct axis short circuit subtransient time constant in
# seconds
# Tprime(T'd): direct axis short circuit transient time constant in seconds
# Ta(Ta): Armature short circuit time constant in seconds

# --------------------------------------------------------------------------------------------------------------------
# Example (Typical input problems)
# A 500-MVA 20-kV, 60-Hz synchronous generator with reactances X”d= 0.15 p.u.,
# X’d=0.24 p.u.; Xd =1.1 p.u. and time constants T”d=0.035s, T’d=2s, TA=0.20 s.

# The generator is operating at 5% above rated voltage and at no-load when a bolted
# three-phase short circuit occurs on the load side of the breaker.

# Thus, the inputs to the script are as following:
# S = 500000000
# Ug = 20000
# percentageEg = 0.05
# f = 60
# Xsecond = 0.15
# Xprime = 0.24
# Xd = 1.1
# Tsecond = 0.035
# Tprime = 2
# Ta = 0.2

# ---------------------------------------------------------------------------------------------------------------------
import numpy as np
import math
import matplotlib.pyplot as plt
t = np.arange(0, 3, 0.01) # You can change the time limit
                          # number whenever you want, just change the
                          # time end value ( 3 in this
                          # example)

try:
    S = float(S)
    Ug = float(Ug)
    percentageEg = float(percentageEg)
    f = float(f)
    Xsecond = float(Xsecond)
    Xprime = float(Xprime)
    Xd = float(Xd)
    Tsecond = float(Tsecond)
    Tprime = float(Tprime)
    Ta = float(Ta)
    w = 2*math.pi*f
    Ibase = S/(math.sqrt(3) * Ug);
    Eg = 1 + percentageEg;

    Ish = dict()
    Iac_rms = dict()
    Idc_offset = dict()
    Ish_rms = dict()

    iter = 0
    while iter < len(t):
        Ish[iter] = math.sqrt(2) * Eg * ((1/Xsecond - 1/Xprime) * math.exp(-t[iter]/Tsecond) + (1/Xprime - 1/Xd) * math.exp( -t[iter]/Tprime) + 1/Xd) * math.cos(w*t[iter]) - math.sqrt(2) * Eg * math.exp( -t[iter]/Ta)
        Ish[iter] = Ish[iter] * Ibase
        Iac_rms[iter] = Eg * ((1/Xsecond - 1/Xprime) * math.exp(-t[iter]/Tsecond) + (1/Xprime - 1/Xd) * math.exp(-t[iter]/Tprime) + 1/Xd)
        Iac_rms[iter] = Iac_rms[iter] * Ibase
        Idc_offset[iter] = math.sqrt(2) * (Eg / Xsecond) * math.exp(-t[iter]/Ta)
        Idc_offset[iter] = Idc_offset[iter] * Ibase
        Ish_rms[iter] = math.sqrt(Iac_rms[iter]**2 + Idc_offset[iter]**2)
        iter = iter + 1
    plt.plot(t,Ish.values(), label = 'Iassymetrical(total)-instantaneous')
    plt.plot(t,Ish_rms.values(), label = 'Iassymetrical(total)-rms')
    plt.plot(t,Iac_rms.values(), label = 'Iac-rms')
    plt.plot(t,Idc_offset.values(), label = 'Idc')
    plt.xlabel('Time in seconds')
    plt.ylabel('Short circuit current in Ampere')
    plt.title('Three-Phase Generator bolted Short circuit current')
    plt.legend(loc ='upper center')
    plt.grid()
    plt.show()

except:
    print('Please enter valid integer values')

# Créé par redwo, le 01/10/2026 en Python 3.7

#
# TP Linear System #1
# Yves HECKEL – 10/09/2026
#
import numpy as np
import matplotlib.pyplot as plt
import control as ctrl
import csv_reader as csv

data = csv.lire_csv_oscilloscope("data_1.csv", 6, 14)

#
# indicielle curb
#

# System Parameters
K = 2.036
w0 = 2*3.1415*13*10**(3)
m = 1
tau = 3.3*10**(-3)*10**(-1)/2

"""
# Transfer Function Definition
num = [K]
den = [1/w0, 1]
H = ctrl.TransferFunction(num, den)
print(H)
"""


# Cascading 2 blocks :
p = ctrl.tf('s')
Ha = K / (1 + tau*p)                    # first-order block
Hb = 1 / (p**2/w0**2 + 2*m*p/w0 + 1)    # second-order block
H = Ha * Hb                             # multiplying the blocks


# Computing the Responses
t_step, y_step = ctrl.step_response(H)
t_imp, y_imp = ctrl.impulse_response(H)

t = np.array([i*25*10**(-3) for i in range(8)])
Ve = np.array([1.1]*8)
Vs_step = np.array([ 0.15, 0.28, 1.98, 1.97, 1.86, 1.18, 1.02, 0.82])
#Vs_imp = np.array([ 0.28, 1.98, 1.97, 1.86, 1.18, 1.02, 0.82])


# Plot the step response
plt.figure(1, figsize=(8,6))
plt.subplot(2,1,1)
#plt.plot(t, Vs_step,'ro', markersize=6, label="measures")
plt.plot(t_step, y_step, 'b-', label="model théorique")

#
# modèle réduit réponse indcielle
#
"""
# Model frequency response
p = ctrl.tf('s')
Ha = 1 / (1 + tau*p)
Hb = 1 / (p**2/w0**2 + 2*m*p/w0 + 1)
H = K * Ha

# Computing the Responses
t_step, y_step = ctrl.step_response(H)
t_imp, y_imp = ctrl.impulse_response(H)
"""

"""
# Horizontal line at 5% ?
plt.axhline(1.05*K, color='b', linestyle=':', linewidth=3)
plt.axhline(0.95*K, color='b', linestyle=':', linewidth=3)

# Vertical line corresponding to 5%?
t_r = 3.3*10**(-2)
plt.axvline(t_r, color='b', linestyle=':', linewidth=3)

# A marker for the crossing ?
plt.plot(t_r, 0.95*K, 'b*', markersize=20)

# A text label to indicate the 63% value ?
plt.annotate("temps de réponse", xy=(t_r, 0.95*K), color='b',xytext=(10, -15), textcoords='offset points')

# Horizontal line at 63% ?
plt.axhline(0.63*K, color='r', linestyle=':', linewidth=3)

# Vertical line corresponding to 63%?
t63 = 1/w0
plt.axvline(t63, color='r', linestyle=':', linewidth=3)

# A marker for the crossing ?
plt.plot(t63, 0.63*K, 'r*', markersize=20)

# A text label to indicate the 63% value ?
plt.annotate("63 %", xy=(t63, 0.63*K), color='r',xytext=(10, -15), textcoords='offset points')
"""

"""
plt.title("Step Response")
plt.xlabel("time (s)")
plt.ylabel("amplitude")
plt.grid(True)
"""

# Plot the step response
plt.figure(1, figsize=(8,6))
plt.subplot(2,1,1)
#plt.plot(t, Vs_step,'ro', markersize=6, label="measures")
plt.plot(t_step, y_step, 'g-', label="model réduit")

#plt.plot(t, Vs_imp,'ro', markersize=6, label="measures")
plt.title("Impulse Response")
plt.xlabel("time (s)")
plt.ylabel("amplitude")
plt.grid(True)

# Formatting and show the plot
plt.tight_layout()
plt.show()

#
# fréquential curb
#

# Measures

f_meas = data["frequence"]
Ve_meas = data["Ve"]
Vs_meas = data["Vs"]
#dt_meas = data["dt"]
Phi_meas = -1*data["phi"]

"""
f_meas = np.array([ 1, 10, 100, 1000, 10**4, 10**5, 10**6, 10**7])
Ve_meas = np.array([ 1.1]*8)
Vs_meas = np.array([ 0.02, 0.28, 1.98, 1.97, 1.86, 1.18, 1.02, 0.82])
dt_meas = np.array([ 0, 40, 1.4, 0.5, 0.8, 0.8, 0.8, 0.09 ])
"""

H_meas = Vs_meas / Ve_meas
GdB_meas = 20 * np.log10(H_meas)

# Plot the measured points
plt.figure(2, figsize=(8,6))
plt.subplot(2,1,1)
plt.semilogx(f_meas, GdB_meas,'ro', markersize=6, label="measures")
plt.semilogx(f_meas, GdB_meas, 'r-', label="model")
plt.ylabel("Gain (dB)") ;
plt.grid(True, which="both")
plt.subplot(2,1,2)
plt.semilogx(f_meas, Phi_meas,'ro', markersize=6, label="measures")
plt.semilogx(f_meas, Phi_meas, 'r-', label="model")
plt.xlabel("fréquence (Hz)") ;
plt.ylabel("Phase (°)")

# Manual plot of the model Bode Diagram
# Frequency vector and complex “p”
f_axis = np.logspace(0, 7, 1000)
w_axis = 2*np.pi*f_axis

# Model frequency response
# Cascading 2 blocks :
p = 1j*w_axis
Ha = K / (1 + tau*p)                    # first-order block
Hb = 1 / (p**2/w0**2 + 2*m*p/w0 + 1)    # second-order block
H = Ha * Hb                             # multiplying the blocks

GdB = 20*np.log10(np.abs(H))
Phi = np.angle(H, deg=True)

# Superimpose on the measured points
plt.subplot(2,1,1)
plt.semilogx(f_axis, GdB, 'b-', label="model théorique")
plt.ylabel("Gain (dB)")
plt.grid(True, which="both")
plt.legend(loc="lower left")

# And the phase
plt.subplot(2,1,2)
plt.semilogx(f_axis, Phi, 'b-', label="model théorique")
plt.xlabel("frequency (Hz)")
plt.ylabel("Phase (°)")
plt.grid(True, which="both")

#
# modèle réduit
#

# Model frequency response
p = 1j*w_axis
Ha = 1 / (1 + tau*p)
Hb = 1 / (p**2/w0**2 + 2*m*p/w0 + 1)
H = K * Ha

GdB = 20*np.log10(np.abs(H))
Phi = np.angle(H, deg=True)

# Superimpose on the measured points
plt.subplot(2,1,1)
plt.semilogx(f_axis, GdB, 'g-', label="model réduit")
plt.ylabel("Gain (dB)")
plt.grid(True, which="both")
plt.legend(loc="lower left")
plt.title("gain")

# And the phase
plt.subplot(2,1,2)
plt.semilogx(f_axis, Phi, 'g-', label="model réduit")
plt.xlabel("frequency (Hz)")
plt.ylabel("Phase (°)")
plt.grid(True, which="both")
plt.title("phase")

# Formatting and show the plot

plt.tight_layout()
plt.show()

#
# pôle and réduction
#

# Or with num / den form :
numa = [K] # first-order block
dena = [tau, 1]
numb = [1] # second-order block
denb = [1/w0**2, 2*m/w0, 1]
num = np.polymul(numa, numb) # multiplying each part
den = np.polymul(dena, denb)
H = ctrl.TransferFunction(num, den) # and redefine the TF

# Some possibilities to study the poles of a transfer function H :
pp = ctrl.poles(H)
zz = ctrl.zeros(H)
KK = ctrl.dcgain(H)
np.roots(den)
ctrl.damp(H) # To be tested and analyzed
# And the corresponding plot:
ctrl.pzmap(H, grid=True)

# Formatting and show the plot
plt.tight_layout()
plt.show()

#
# Bode and Black curb
#

# Or with num / den form :
numa = [K] # first-order block
dena = [tau, 1]
numb = [1] # second-order block
denb = [1/w0**2, 2*m/w0, 1]
num = np.polymul(numa, numb) # multiplying each part
den = np.polymul(dena, denb)
H = ctrl.TransferFunction(num, den) # and redefine the TF

# The margins (always on the OL= Open Loop) ?
gm, pm, wcg, wcp = ctrl.margin(H) # the essential 4 values
sm = ctrl.stability_margins(H) # 6 values, including the module margin
# Attention, gm is linear, not in dB

# Plot the margins
ctrl.bode_plot(H, dB=True, Hz=True, margins=True)

# Plot the Black-Nichols chart
ctrl.nichols_plot(H) # ctrl.nichols_grid()

# Studying the Closed Loop (CL) :
T = ctrl.feedback(H, 1) # CL with unity feedback
ctrl.step_info(T, SettlingTimeThreshold=0.05) # overshoot, settling time
np.max(np.abs(T(1j*w_axis))) # resonant peak
ctrl.damp(T) # damping of the CL poles


# Formatting and show the plot
plt.tight_layout()
plt.show()
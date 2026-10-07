# Créé par redwo, le 01/10/2026 en Python 3.7

#
# TP Linear System #1
# Yves HECKEL – 10/09/2026
#
import numpy as np
import matplotlib.pyplot as plt
import control as ctrl
import csv_reader as csv

data = csv.lire_csv_oscilloscope("data_1.csv", 4, 7)

#
# PART 1
#

# System Parameters
K = 1.8
w0 = 1.2*10**4
m = 3*10**(-3)


# Transfer Function Definition
num = [K]
den = [1/w0, 1]
H = ctrl.TransferFunction(num, den)
print(H)

# Second manner to define the TF
w_axis = ctrl.tf('s')
H2 = K / (1 + 2j*m*((w_axis/w0) -(w0/w_axis)))


# Computing the Responses
t_step, y_step = ctrl.step_response(H2)
t_imp, y_imp = ctrl.impulse_response(H2)

t = np.array([i*25*10**(-3) for i in range(8)])
Ve = np.array([1.1]*8)
Vs_step = np.array([ 0.15, 0.28, 1.98, 1.97, 1.86, 1.18, 1.02, 0.82])
#Vs_imp = np.array([ 0.28, 1.98, 1.97, 1.86, 1.18, 1.02, 0.82])


# Plot the step response
plt.figure(1, figsize=(8,6))
plt.subplot(2,1,1)
#plt.plot(t, Vs_step,'ro', markersize=6, label="measures")
plt.plot(t_step, y_step)
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
plt.title("Step Response")
plt.xlabel("time (s)")
plt.ylabel("amplitude")
plt.grid(True)
"""
# And plot the impulse response
plt.subplot(2,1,2)

#plt.plot(t, Vs_imp,'ro', markersize=6, label="measures")
plt.plot(t_imp, y_imp)
plt.title("Impulse Response")
plt.xlabel("time (s)")
plt.ylabel("amplitude")
plt.grid(True)
"""

# Formatting and show the plot
plt.tight_layout()
plt.show()

#
#PART 2
#

# Measures

f_meas = data["frequence"]
Ve_meas = data["Ve"]
Vs_meas = data["Vs"]
dt_meas = data["dt"]
"""
f_meas = np.array([ 1, 10, 100, 1000, 10**4, 10**5, 10**6, 10**7])
Ve_meas = np.array([ 1.1]*8)
Vs_meas = np.array([ 0.02, 0.28, 1.98, 1.97, 1.86, 1.18, 1.02, 0.82])
dt_meas = np.array([ 0, 40, 1.4, 0.5, 0.8, 0.8, 0.8, 0.09 ])
"""
print(dt_meas)
Phi_meas = f_meas*dt_meas*360*-10**(-6)/2
print(Phi_meas)
H_meas = Vs_meas / Ve_meas
GdB_meas = 20 * np.log10(H_meas)

# Plot the measured points
plt.figure(2, figsize=(8,6))
plt.subplot(2,1,1)
plt.semilogx(f_meas, GdB_meas,'ro', markersize=6, label="measures")
plt.ylabel("Gain (dB)") ;
plt.grid(True, which="both")
plt.subplot(2,1,2)
plt.semilogx(f_meas, Phi_meas,'ro', markersize=6, label="measures")
plt.xlabel("fréquence (Hz)") ;
plt.ylabel("Phase (°)")

# Manual plot of the model Bode Diagram
# Frequency vector and complex “p”
f_axis = np.logspace(0, 7, 1000)
w_axis = 2*np.pi*f_axis

# Model frequency response
Hjw = K / (1 + 2j*m*((w_axis/w0) -(w0/w_axis)))
#Hjw = K*1j*w_axis*(m/w0) / (1 + 1j*w_axis*(m/w0))
GdB = 20*np.log10(np.abs(Hjw))
Phi = np.angle(Hjw, deg=True)

# Superimpose on the measured points
plt.subplot(2,1,1)
plt.semilogx(f_axis, GdB, 'b-', label="model")
plt.ylabel("Gain (dB)")
plt.grid(True, which="both")
plt.legend(loc="lower left")

# And the phase
plt.subplot(2,1,2)
plt.semilogx(f_axis, Phi, 'b-', label="model")
plt.xlabel("frequency (Hz)")
plt.ylabel("Phase (°)")
plt.grid(True, which="both")

# Formatting and show the plot
plt.tight_layout()
plt.show()
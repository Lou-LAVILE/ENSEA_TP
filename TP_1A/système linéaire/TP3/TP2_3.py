# Créé par redwo, le 01/10/2026 en Python 3.7

#
# TP Linear System #1
# Yves HECKEL – 10/09/2026
#
import numpy as np
import matplotlib.pyplot as plt
import control as ctrl
import csv_reader as csv

# System Parameters
K = 2.036
w0 = 2*3.1415*13*10**(3)
m = 1
tau = 3.3*10**(-3)*10**(-1)/2



#
# fréquential curb
#

color = ['r','b']
for i in range(1,3):
    # Measures
    print(i)
    data = csv.lire_csv_oscilloscope(f"data_{i}.csv", 5, 14)

    f_meas = data["frequence"]
    Ve_meas = data["Ve"]
    Vs_meas = data["Vs"]
    #dt_meas = data["dt"]
    Phi_meas = -1*data["phi"]

    H_meas = Vs_meas / Ve_meas
    GdB_meas = 20 * np.log10(H_meas)

    c = color[i-1]
    # Plot the measured points

    plt.subplot(2,1,1)
    plt.semilogx(f_meas, GdB_meas,c+'o', markersize=6, label="measures_"+str(i))
    plt.semilogx(f_meas, GdB_meas, c+'-', label="model")
    plt.ylabel("Gain (dB)") ;
    plt.grid(True, which="both")
    plt.title("gain")

    plt.subplot(2,1,2)
    plt.semilogx(f_meas, Phi_meas,c+'o', markersize=6, label="measures_"+str(i))
    plt.semilogx(f_meas, Phi_meas, c+'-', label="model")
    plt.xlabel("fréquence (Hz)") ;
    plt.ylabel("Phase (°)")
    plt.grid(True, which="both")
    plt.title("phase")

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

#boucle ouverte
H = H/(1+H)

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

# Formatting and show the plot
plt.tight_layout()
plt.show()
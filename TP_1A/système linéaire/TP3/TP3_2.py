#
# Skander-LATROUS Lou-LAVILLE / 06/11/26 /
# Asservissement de Vitesse de MCC - Simulation
# Analyse de l’influence des paramètres de correction
#

import numpy as np
import matplotlib.pyplot as plt
import control as ctrl
import csv_reader as csv


def graph_Bode(H, title, color):
    GdB = 20*np.log10(np.abs(H))
    Phi = np.angle(H, deg=True)

    # Superimpose on the measured points
    plt.subplot(2,1,1)
    plt.semilogx(f_axis, GdB, color+'-', label=title)
    plt.ylabel("Gain (dB)")
    plt.grid(True, which="both")
    plt.legend(loc="lower left")

    # And the phase
    plt.subplot(2,1,2)
    plt.semilogx(f_axis, Phi, color+'-', label=title)
    plt.xlabel("frequency (Hz)")
    plt.ylabel("Phase (°)")
    plt.grid(True, which="both")

def add_tau(tau, color):
    plt.axvline(1/tau, color=color, linestyle=':', linewidth=3)

def aff_graph():
    plt.tight_layout()
    plt.show()

def analyze_step_response(t, y):
    y_peak = np.max(y)
    t_peak = t[np.where(y==y_peak)]
    y_resp = y[-1]
    t_resp = t[np.where(y==y_resp)]
    overshoot = y_peak - y_resp
    return (t_peak, y_peak, overshoot, t_resp, y_resp)


#
# Effet d’une action proportionnelle P :
#

R = 0.37
L = 0.6*10**(-3)
K = 0.12
f = 6*10**(-4)
J = 0.003

L_ext = 60*10**(-3)
R_ext = 3

K3 = 4.8
K_T = 0.005

# Q1.2. Calcul des constantes et des gains – à controler avec des prints
L_tot = L+L_ext
R_tot = R+R_ext

tau_e = R_tot/L_tot
tau_m = f/J
tau1 = tau_m / (1+K**2/(R*f))
tau2 = tau_e / (1+K**2/(R*f))
tau3 = 20*10**(-3)

f_axis = np.logspace(0, 7, 1000)
w_axis = 2*np.pi*f_axis
p = 1j*w_axis

T = ctrl.TransferFunction([K3*K*K_T], [tau1*tau2, tau1+tau2+tau3, 1])

KP_val = [0.1, 0.3, 1, 3, 10]
color = ['b', 'g', 'r', 'y', '']

# Q7.2. Tracé des Bode du correcteur
for i, KP in enumerate(KP_val):
    # Definition du correcteur proportionnel – Avec frequency_response en manuel
    C_P = ctrl.TransferFunction([KP], [1])
    CP_mag, CP_phase, CP_omega = ctrl.frequency_response(C_P, omega=w_axis)
    # Diagramme de Bode (gain et phase)
    plt.subplot(2, 2, 1)
    plt.semilogx(CP_omega, 20*np.log10(CP_mag), color[i], label=f"KP = {KP}")
    plt.subplot(2, 2, 3)
    plt.semilogx(CP_omega, CP_phase/np.pi*180, color[i], label=f"KP = {KP}")
    plt.subplot(1, 2, 2)
    ctrl.nichols_plot(C_P)

    #Q9
    # Création de l'axe des temps
    te = 0.01
    t_final = 5
    Taxis = np.arange(0, t_final, te)

    # Et dans la boucle for…
    CP = ctrl.TransferFunction([KP], [1])
    t_TCP, y_TCP = ctrl.step_response(ctrl.feedback(CP*T, 1), Taxis)
    t_peak, y_peak, overshoot, t_resp, y_resp = analyze_step_response(t_TCP, y_TCP, )
    print(f"Tps de réponse à 5% pour KP = {KP} \t: {t_resp} s et D% = {overshoot}")

aff_graph()

print("P+BO")
# Q8.2. Tracé des Bode du correcteur
for i, KP in enumerate(KP_val):
    # Definition du correcteur proportionnel – Avec frequency_response en manuel
    C_P = ctrl.TransferFunction([KP], [1])
    CP_mag, CP_phase, CP_omega = ctrl.frequency_response(C_P*T, omega=w_axis)
    # Diagramme de Bode (gain et phase)
    plt.subplot(2, 2, 1)
    plt.semilogx(CP_omega, 20*np.log10(CP_mag), color[i], label=f"KP = {KP}")
    plt.subplot(2, 2, 3)
    plt.semilogx(CP_omega, CP_phase/np.pi*180, color[i], label=f"KP = {KP}")
    plt.subplot(1, 2, 2)
    ctrl.nichols_plot(C_P*T)

    #Q9
    # Création de l'axe des temps
    te = 0.01
    t_final = 5
    Taxis = np.arange(0, t_final, te)

    # Et dans la boucle for…
    CP = ctrl.TransferFunction([KP], [1])
    t_TCP, y_TCP = ctrl.step_response(ctrl.feedback(CP*T, 1), Taxis)
    t_peak, y_peak, overshoot, t_resp, y_resp = analyze_step_response(t_TCP, y_TCP, )
    print(f"Tps de réponse à 5% pour KP = {KP} \t: {t_resp} s et D% = {overshoot}")

aff_graph()
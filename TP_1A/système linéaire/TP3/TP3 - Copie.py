#
# Skander-LATROUS Lou-LAVILLE / 06/11/26 /
# Asservissement de Vitesse de MCC - Simulation
# Analyse de l’influence des paramètres de correction
#

import numpy as np
import matplotlib.pyplot as plt
import control as ctrl
import csv_reader as csv


def graph_Bode(H, title, color, tau):
    GdB = 20*np.log10(np.abs(H))
    Phi = np.angle(H, deg=True)

    # Superimpose on the measured points
    plt.subplot(2,1,1)
    plt.semilogx(f_axis, GdB, color+'-', label=title)
    add_tau(tau, color)
    plt.ylabel("Gain (dB)")
    plt.grid(True, which="both")
    plt.legend(loc="lower left")

    # And the phase
    plt.subplot(2,1,2)
    plt.semilogx(f_axis, Phi, color+'-', label=title)
    add_tau(tau, color)
    plt.xlabel("frequency (Hz)")
    plt.ylabel("Phase (°)")
    plt.grid(True, which="both")

def add_tau(tau, color):
    plt.axvline(1/tau, color=color, linestyle=':', linewidth=3)

def aff_graph():
    plt.tight_layout()
    plt.show()

# Q1.1. Paramètres du système

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

print("L_tot",L_tot)
print("R_tot",R_tot)

tau_e = R_tot/L_tot
tau_m = f/J
temp = (1-4*(L_tot*J/(K**2+R_tot*f)))
print("signe delta", temp)
tau2 = -1/2 *(temp)**(1/2)
#tau1 = tau_m / (1+K**2/(R*f))
tau1 = (L_tot*f+J*R_tot)/(K**2+R_tot*f) - tau2
#tau2 = tau_e / (1+K**2/(R*f))


tau3 = 20*10**(-3)

print("Constante de temps : ")
print(f"tau_e = {tau_e} s, tau_m = {tau_m} s\n")
print(f"tau1 = {tau1} s, tau2 = {tau2} s, tau3 = {tau3} s\n")

H0 = K
print("Gains : ")
print(f"H0 = {H0} V/rad/s, K3 = {K3}, K_T = {K_T} V/rad/s  \n")

# Q1.3. Fonctions de transfert

p = ctrl.tf('s')

def H1(p):
    return K / ((R_tot+L_tot*p)*(f+J*p)+K**2)

print(f"FT MCC seule = {H1(p)}\n")

def H2(p):
    return K / (R_tot*f+K**2+(R_tot*J+L_tot*f)*p)
print(f"FT  Vitesse/Tension seule = {H2(p)}\n")

def H3(p):
    return 1 / (R_tot+L_tot*p)
print(f"FT Courant/Tension = {H3(p)}\n")

def T(p):
    return K3*K_T*K / ((R_tot+L_tot*p))
print(f"FT système complet = {T(p)}\n")

def T2(p):
    return K3*K_T*K / ((1+tau3*p)*(f+J*p)*(R_tot+L_tot*p))
# Q1.4. Tracé des Bodes

f_axis = np.logspace(0, 7, 1000)
w_axis = 2*np.pi*f_axis
p = 1j*w_axis

H1 = H1(p)
H2 = H2(p)
H3 = H3(p)
T = T(p)
T2 = T2(p)


L = [
    (H1, "FT MCC seule", 'b', tau1),
    (H2, "FT  Vitesse/Tension seule", 'r', tau2),
    (H3, "FT Courant/Tension", 'g', tau3),
    (T, "FT système complet", 'y', tau2),
    (T2, "FT système complet 2", 'b', tau2)
]
for l in L:
    graph_Bode(l[0], l[1], l[2], l[3])
aff_graph()

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
    add_tau([tau1, tau2, tau3])

    # And the phase
    plt.subplot(2,1,2)
    plt.semilogx(f_axis, Phi, color+'-', label=title)
    add_tau([tau1, tau2, tau3])
    plt.xlabel("frequency (Hz)")
    plt.ylabel("Phase (°)")
    plt.grid(True, which="both")
    add_tau([tau1, tau2, tau3])

def add_tau(L_tau):
    for i in range(len(L_tau)):
        plt.axvline(1/L_tau[i], linestyle=':')
        plt.text(1/L_tau[i], 0, f"tau{i+1}", color='b')

def aff_graph():
    plt.tight_layout()
    plt.show()

def main():
    # Q1.1. Paramètres du système

    R = 0.37
    L = 0.6*10**(-3)
    K = 0.12
    f = 6*10**(-4)
    J = 0.003

    L_ext = 60*10**(-3)
    R_ext = 3

    K3 = 4.8
    K_omega = 0.005

    # Q1.2. Calcul des constantes et des gains – à controler avec des prints
    L_tot = L+L_ext
    R_tot = R+R_ext

    print("L_tot",L_tot)
    print("R_tot",R_tot)

    tau_e = R_tot/L_tot
    tau_m = f/J
    """
    temp = (1-4*(L_tot*J/(K**2+R_tot*f)))
    print("signe delta", temp)
    tau2 = -1/2 *(temp)**(1/2)
    #tau1 = tau_m / (1+K**2/(R*f))
    tau1 = (L_tot*f+J*R_tot)/(K**2+R_tot*f) - tau2
    #tau2 = tau_e / (1+K**2/(R*f))
    """

    tau1 = tau_e
    tau2 = tau_m

    tau3 = 20*10**(-3)

    print("Constante de temps : ")
    print(f"tau_e = {tau_e} s, tau_m = {tau_m} s\n")
    print(f"tau1 = {tau1} s, tau2 = {tau2} s, tau3 = {tau3} s\n")

    H0 = K**2 / (R_tot+f)
    K_T = K3*K**2*K_omega

    print("Gains : ")
    print(f"H0 = {H0} V/rad/s, K3 = {K3}, K_T = {K_T} V/rad/s  \n")

    # Q1.3. Fonctions de transfert

    p = ctrl.tf('s')

    def H1(p):
        return H0 / ((1+tau_e*p)*(1+tau_m*p))

    print(f"FT MCC seule = {H1(p)}\n")

    def H2(p):
        return H0 / ((1+tau_e*p)*(1+tau_m*p))
    print(f"FT  Vitesse/Tension seule = {H2(p)}\n")

    def H_I(p):
        return 1/R_tot / (1+tau_e*p)
    print(f"FT Courant/Tension = {H_I(p)}\n")

    def T(p):
        return K_T / ((1+tau_e*p)*(1+tau_m*p)*(1+tau3*p))
    print(f"FT système complet = {T(p)}\n")

    # Q1.4. Tracé des Bodes

    f_axis = np.logspace(-3, 7, 1000)
    w_axis = 2*np.pi*f_axis
    p = 1j*w_axis

    G_H1 = H1(p)
    G_H2 = H2(p)
    G_I = H_I(p)
    G_T = T(p)

    L = [
        (G_H1, "FT MCC seule", 'b'),
        (G_H2, "FT  Vitesse/Tension seule", 'r'),
        (G_I, "FT Courant/Tension", 'g'),
        (G_T, "FT système complet", 'y'),
    ]

    if aff[0]:
        for l in L:
            graph_Bode(l[0], l[1], l[2])
        aff_graph()


    # Q3.1. Marge de gain et de phase

    den = np.polymul([tau1, 1], [tau2, 1])
    G_I = ctrl.TransferFunction([H0], den)
    den = np.polymul(den, [tau3, 1])
    G_T = ctrl.TransferFunction([K_T], den)

    den = np.polymul([tau1, 1], [tau2, 1])
    den = np.polymul(den, [tau3, 1])

    if aff[1]:

        T_gm, T_pm, T_wg, T_wp = ctrl.margin(G_T)
        T_gm = - 20*np.log10(T_gm)
        print(f"Marge de gain de T (dB): {T_gm}")


        # Superposition sur le diagramme de Bode
        plt.figure(5, figsize=(6,4))
        ctrl.bode_plot(G_T, dB=True, Hz=False, deg=True, grid=True)


        # Ajouter lignes verticales et horizontales pour montrer les marges
        plt.subplot(2,1,1)
        plt.axvline(T_wp, color='r', linestyle='--', label=f'ωp={T_wp:.2f} rad/s')
        plt.axhline(0, color='r', linestyle='-')
        plt.axvline(T_wg, color='g', linestyle='--', label=f'ωg={T_wg:.2f} rad/s')
        plt.axhline(T_gm, color='g', linestyle='-', label=f'gm={T_gm:.2f} dB')
        plt.legend()


        # Ajout d'une flèche pour montrer la marge de gain
        plt.annotate('', # Pas de texte
            xy=(T_wg, T_gm), # Point de destination
            xytext=(T_wg, 0), # Point de départ
            arrowprops=dict(arrowstyle="->", color="green", lw=4, linestyle="-")
        )
        plt.title("Bode système complet")
        aff_graph()

        # Plot the Black-Nichols chart
        ctrl.nichols_plot(G_T)
        plt.plot()

        # Ajouter lignes verticales et horizontales pour montrer les marges
        plt.axvline(-180, color='g', linestyle='--', label=f'ωg={T_wg:.2f} rad/s')
        plt.axhline(T_gm, color='g', linestyle='-', label=f'gm={T_gm:.2f} dB')

        # Ajout d'une flèche pour montrer la marge de gain
        plt.annotate('', # Pas de texte
            xy=(T_wg, T_gm), # Point de destination
            xytext=(T_wg, 0), # Point de départ
            arrowprops=dict(arrowstyle="->", color="green", lw=4, linestyle="-")
        )

        plt.legend()
        plt.title("Black-Nichols système complet")
        aff_graph()

    if aff[2]:
        print("G_T", G_T)
        print("G_I", G_I)
        # Q4.2. Exemple de fonction permettant d’analyser les courbes
        def analyze_step_response(t, y):
            # Valeur finale de la réponse indicielle
            y_final = y[-1]
            # Premier pic
            idx_peak = np.argmax(y)
            t_peak = t[idx_peak]
            y_peak = y[idx_peak]

            # Dépassement
            if ((y_final != 0) & (y_peak > y_final)):
                overshoot = ((y_peak - y_final) / y_final) * 100
            else:
                overshoot = 0

            # Temps de réponse à 5%
            outside = np.where((y < 0.95*y_final) | (y > 1.05*y_final))[0]
            if len(outside) > 0:
                t_resp = t[outside[-1]]
                y_resp = y[outside[-1]]
            else:
                t_resp = None
                y_resp = None
            return t_peak, y_peak, overshoot, t_resp, y_resp

        for L_H in [(G_T,"T",'g'), (G_I, "H_I", 'b')]:
            # Q4.1. Tracé et calcul des temps/overshoot/…
            t_T, y_T = ctrl.step_response(L_H[0])
            plt.plot(t_T, y_T, color=L_H[2], label=L_H[1])
            t_peak, y_peak, overshoot, t_resp, y_resp = analyze_step_response(t_T, y_T)
            print(L_H[1],t_peak, y_peak, overshoot, t_resp, y_resp)

            # Ajout des temps de réponse à 5% / flèches sur la courbe
            plt.axhline(y=0.95 * y_T[-1], color='r', linestyle='--')
            plt.axhline(y=1.05 * y_T[-1], color='r', linestyle='--')
            plt.axvline(t_resp, color=L_H[2], linestyle='--', lw=1)
            plt.plot(t_resp, y_resp, L_H[2]+'o')
            plt.annotate(f"t_5% = {t_resp:.2f}s",
            xy=(t_resp, y_resp),
            xytext=(t_resp-0.1, y_resp-0.5),
            arrowprops=dict(arrowstyle="->", color=L_H[2]))

            # Et le premier pic / flèches sur la courbe
            plt.plot(t_peak, y_peak, L_H[2]+'o')
            plt.annotate(f"t_p = {t_peak:.2f}s\n(y={y_peak:.2f})",
            xy=(t_peak, y_peak),
            xytext=(t_peak-0.1, y_peak-0.5),
            arrowprops=dict(arrowstyle="->", color=L_H[2]))

            plt.title(L_H[1]+" Impulse Response")
            plt.xlabel("time (s)")
            plt.ylabel("amplitude")
        aff_graph()



if __name__=="__main__":
    #parameter of which chart while be printed
    aff = (0, 0, 1, 1)
    main()
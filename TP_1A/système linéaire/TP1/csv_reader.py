# Créé par redwo, le 01/10/2026 en Python 3.7

import pandas as pd
import numpy as np

#lis les données d'un fichier csv
def lire_csv_oscilloscope(file_path, n_signal, n_mesure):

    data = pd.read_csv(file_path, ";", dtype=float)

    signal_data = {}
    for i in range(n_signal):
        name = data.columns[i]
        signal_data[name] = data.iloc[0:(n_mesure+1), i].to_numpy()

    print(signal_data)
    return signal_data
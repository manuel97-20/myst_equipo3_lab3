"""
# -- --------------------------------------------------------------------------------------------------- -- #
# -- project: A SHORT DESCRIPTION OF THE PROJECT                                                         -- #
# -- script: main.py : python script with the main functionality                                         -- #
# -- author: YOUR GITHUB USER NAME                                                                       -- #
# -- license: GPL-3.0 License                                                                            -- #
# -- repository: YOUR REPOSITORY URL                                                                     -- #
# -- --------------------------------------------------------------------------------------------------- -- #
"""
import functions as fn
import data as dt
import datetime
import pandas as pd
import numpy as np

prueba_size = fn.f_pip_size('xauusd')
tiempos = fn.f_columnas_tiempos(dt.archivo)
pips = fn.f_columnas_pips(tiempos)
diccionario = fn.f_estadisticas_ba(dt.archivo)
evcap = fn.f_evolucion_capital(dt.archivo)
mad = fn.f_estadisticas_mad(evcap)

# Saber si al cerrar una operacion ganadora se quedo abierta una con perdida flotante
ot = [(pd.to_datetime(dt.archivo['Open Time'])[i]) for i in np.arange(0, len(dt.archivo), 1)]
ct = [(pd.to_datetime(dt.archivo['Close Time'])[i]) for i in np.arange(0, len(dt.archivo), 1)]
gn = []
ocp = []
for i in np.arange(0, len(dt.archivo), 1):
    if ot[i] >= ot[i - 1] and ct[i] > ct[i - 1] and ot[i] < ct[i - 1] and dt.archivo.Profit[i - 1] >= 0 and \
            dt.archivo.Profit[i] < 0:
        ocp.append(i)  # Posicion de operaciones complementarias con perdida flotante
        gn.append(i - 1)  # Posicion de la operacion ganadora (ancla)

# Punto de referencia:

ratop=1
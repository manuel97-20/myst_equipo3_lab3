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
import pandas as pd
import numpy as np

archivo = fn.f_leer_archivo('c:/Users/luzitaifi/Documents/Micro_Estructuras_Trading/Lab_3/myst_equipo3_lab3/Statement' \
                    '.csv')#Statement
prueba_size = fn.f_pip_size('xauusd')
tiempos = fn.f_columnas_tiempos(archivo)
pips = fn.f_columnas_pips(tiempos)
diccionario = fn.f_estadisticas_ba(archivo)
evcap = fn.f_evolucion_capital(archivo)
mad = fn.f_estadisticas_mad(evcap)
diseff=fn.f_be_de(archivo)
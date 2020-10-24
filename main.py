
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
prueba_size = fn.f_pip_size('xauusd')
tiempos = fn.f_columnas_tiempos(dt.archivo)
pips = fn.f_columnas_pips(tiempos)
diccionario = fn.f_estadisticas_ba(dt.archivo)
evcap=fn.f_evolucion_capital(dt.archivo)
print(evcap)



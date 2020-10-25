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
evcap = fn.f_evolucion_capital(dt.archivo)
print(evcap)

# ---------Drawdowm
punto_partida = dpp['profit_acm_d'].max()  # Obtener el punto maximo
renglon_max = dpp[dpp['profit_acm_d'].isin([punto_partida])]  # Obtener en que renglon esta el maximo
fecha_maxima = str(renglon_max['timestamp'])  # Fecha del maximo
df_drawdown = dpp.iloc[:29]  # Cortar el dataframe manualmente
min_drawdown = df_drawdown['profit_acm_d'].min()  # Obtener el punto minimo
renglon_min = df_drawdown[df_drawdown['profit_acm_d'].isin([min_drawdown])]  # Obtener el renglon del punto minimo
fecha_min = str(renglon_min['timestamp'])  # Fecha minima
drawn_down = (min_drawdown - punto_partida) / punto_partida  # Formula de drawdown
v = [fecha_min, fecha_maxima, drawn_down]
print(v)

# ----------Drawup
df_drawup = dpp.iloc[28:]  # Cortar el dataframe manualmente
min_drawup = df_drawup['profit_acm_d'].min()  # Obtener el punto minimo
renglon_min2 = df_drawup[df_drawup['profit_acm_d'].isin([min_drawup])]  # Obtener el renglon del punto minimo
fecha_min2 = str(renglon_min2['timestamp'])  # Fecha minima
drawn_up = (punto_partida - min_drawup) / min_drawup  # Formula de drawup
v2 = [fecha_maxima, fecha_min2, drawn_up]
print(v2)

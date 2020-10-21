"""
# -- --------------------------------------------------------------------------------------------------- -- #
# -- project: A SHORT DESCRIPTION OF THE PROJECT                                                         -- #
# -- script: functions.py : python script with general functions                                         -- #
# -- author: YOUR GITHUB USER NAME                                                                       -- #
# -- license: GPL-3.0 License                                                                            -- #
# -- repository: YOUR REPOSITORY URL                                                                     -- #
# -- --------------------------------------------------------------------------------------------------- -- #
"""
#%%
import numpy as np
import data as dt
import pandas as pd

# %% aqui hacemos la función del multiplicador
def f_pip_size(ticker_f):
    oanda_instruments =dt.oanda_instruments

    ticker_up = ticker_f.upper()
    if ticker_up == 'WTICO':

        indx = np.concatenate(np.where(ticker_up == oanda_instruments.index))[0]
        temp = oanda_instruments['PipLocation'].iloc[indx]
        if temp == -4:
            mult = 10000
        elif temp == -2:
            mult = 100
        elif temp == 0:
            mult = 1
    elif ticker_up == 'BTCUSD':
        mult = 100

    else:
        ticker_up = ticker_up[:3] + '.' + ticker_up[3:]  # ponemos todos en mayusculas

        indx = np.concatenate(np.where(ticker_up == oanda_instruments.index))[0]
        temp = oanda_instruments['PipLocation'].iloc[indx]
        if temp == -4:
            mult = 10000
        elif temp == -2:
            mult = 100
        elif temp == 0:
            mult = 1
    return mult

#%%
#Aquí ponemos la función para calcular los segundos transcurridos

def f_columnas_tiempos(df_data):
    open_time = pd.to_datetime(df_data['openTime'])
    close_time = pd.to_datetime(df_data['closeTime'])
    delta = [(close_time[i] - open_time[i]).total_seconds() for i in range(len(df_data['openTime']))]
    #Hay que regresar todo el data frame
    df_data['Tiempo'] = delta
    return df_data

#%%
#Aquí ponemos la función para obtener lo que concierne a pips
def f_columnas_pips(archivo):
    pips = []
    pips_acum = []
    profit_acum = []
    for i in range(len(archivo)):
        if i == 0:
            if archivo['Type'].iloc[i] == 'buy':
                pips.append(
                    (archivo['closePrice'].iloc[i] - archivo['openPrice'].iloc[i]) * f_pip_size(archivo['Symbol'].iloc[i]))
            else:
                pips.append(
                    (archivo['openPrice'].iloc[i] - archivo['closePrice'].iloc[i]) * f_pip_size(archivo['Symbol'].iloc[i]))
            pips_acum.append(pips[0])
            profit_acum.append(archivo['Profit'].iloc[0])

        else:
            if archivo['Type'].iloc[i] == 'buy':
                pips.append(
                    (archivo['closePrice'].iloc[i] - archivo['openPrice'].iloc[i]) * f_pip_size(archivo['Symbol'].iloc[i]))

            else:
                pips.append(
                    (archivo['openPrice'].iloc[i] - archivo['closePrice'].iloc[i]) * f_pip_size(archivo['Symbol'].iloc[i]))

            pips_acum.append(pips_acum[i - 1] + pips[i])
            profit_acum.append(profit_acum[i - 1] + archivo['Profit'].iloc[i])

    archivo['pips'] = pips
    archivo['pips_acum'] = pips_acum
    archivo['profit_acum'] = profit_acum
    return archivo

#%% Aquí hacemos la función para estadistica basica
def f_estadisticas_ba(archivo):
    medida = ['Ops totales', 'Ganadoras', 'Ganadoras_c', 'Ganadoras_v',
              'Perdedoras', 'Perdedoras_c', 'Perdedoras_v', 'Mediana (Profit)', 'Mediana (Pips)', 'r_efectividad',
              'r_proporcion',
              'r_efectividad_c', 'r_efectividad_v'] #hacemos una lista con todo lo necesario en medida

    ops_totales = len(archivo)
    Ganadoras = np.sum([True for i in range(len(archivo)) if archivo['Profit'].iloc[i] > 0])
    Ganadoras_c = np.sum(
        [True for i in range(len(archivo)) if archivo['Profit'].iloc[i] > 0 and archivo['Type'].iloc[i] == 'buy'])
    Ganadoras_v = np.sum(
        [True for i in range(len(archivo)) if archivo['Profit'].iloc[i] > 0 and archivo['Type'].iloc[i] == 'sell'])
    Perdedoras = np.sum([True for i in range(len(archivo)) if archivo['Profit'].iloc[i] < 0])
    Perdedoras_c = np.sum(
        [True for i in range(len(archivo)) if archivo['Profit'].iloc[i] < 0 and archivo['Type'].iloc[i] == 'buy'])
    Perdedoras_v = np.sum(
        [True for i in range(len(archivo)) if archivo['Profit'].iloc[i] < 0 and archivo['Type'].iloc[i] == 'sell'])
    mediana_profit = np.median(archivo['Profit'])
    mediana_pips = np.median(archivo['pips'])
    r_efectividad = Ganadoras / ops_totales
    r_proporcion = Ganadoras / Perdedoras
    r_efectividad_c = Ganadoras_c / ops_totales
    r_efectividad_v = Ganadoras_v / ops_totales

    valor = [ops_totales, Ganadoras, Ganadoras_c, Ganadoras_v, Perdedoras, Perdedoras_c, Perdedoras_v, mediana_profit,
             mediana_pips, r_efectividad, r_proporcion, r_efectividad_c, r_efectividad_v]

    descripcion = ['Operaciones totales', 'Operaciones ganadoras', 'Operaciones ganadoras de compra',
                   'Operaciones ganadoras de venta',
                   'Operaciones perdedoras', 'Operaciones perdedoras de compra', 'Operaciones perdedoras de venta',
                   'Mediana de profit de operaciones', 'Mediana de pips de operaciones',
                   'Ganadoras Totales/Operaciones Totales',
                   'Ganadoras Totales/Perdedoras Totales', 'Ganadoras Compras/Operaciones Totales',
                   'Ganadoras Ventas/Operaciones Totales']

    df = pd.DataFrame({'medida': medida, 'valor': valor, 'descripcion': descripcion})
    df

    # antes que nada hay obtener los tickers unicos


    unicos = np.unique(archivo['Symbol'])  # listo ya tenemos los unicos
    rank = []
    for i in range(len(unicos)):
        positives = 0
        negatives = 0
        for j in range(len(archivo)):
            if unicos[i] == archivo['Symbol'].iloc[j] and archivo['Profit'].iloc[j] > 0:
                positives += 1
            elif unicos[i] == archivo['Symbol'].iloc[j] and archivo['Profit'].iloc[j] < 0:

                negatives += 1

        total = negatives + positives
        rank.append(positives / total)

    df_2 = pd.DataFrame({'symbol': unicos, 'rank': rank})
    df_2 = df_2.sort_values(by='rank', ascending=False)


    final = {'df_1_tabla': df, 'df_2_ranking': df_2}
    return final

# termina la parte 1
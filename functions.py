"""
# -- --------------------------------------------------------------------------------------------------- -- #
# -- project: A SHORT DESCRIPTION OF THE PROJECT                                                         -- #
# -- script: functions.py : python script with general functions                                         -- #
# -- author: YOUR GITHUB USER NAME                                                                       -- #
# -- license: GPL-3.0 License                                                                            -- #
# -- repository: YOUR REPOSITORY URL                                                                     -- #
# -- --------------------------------------------------------------------------------------------------- -- #
"""
# %%
import numpy as np
import data as dt
import pandas as pd
import datetime
from datetime import datetime


# %% aqui hacemos la función del multiplicador
def f_pip_size(ticker_f):
    oanda_instruments = dt.oanda_instruments

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


# %%
# Aquí ponemos la función para calcular los segundos transcurridos

def f_columnas_tiempos(df_data):
    open_time = pd.to_datetime(df_data['openTime'])
    close_time = pd.to_datetime(df_data['closeTime'])
    delta = [(close_time[i] - open_time[i]).total_seconds() for i in range(len(df_data['openTime']))]
    # Hay que regresar todo el data frame
    df_data['Tiempo'] = delta
    return df_data


# %%
# Aquí ponemos la función para obtener lo que concierne a pips
def f_columnas_pips(archivo):
    pips = []
    pips_acum = []
    profit_acum = []
    for i in range(len(archivo)):
        if i == 0:
            if archivo['Type'].iloc[i] == 'buy':
                pips.append(
                    (archivo['closePrice'].iloc[i] - archivo['openPrice'].iloc[i]) * f_pip_size(
                        archivo['Symbol'].iloc[i]))
            else:
                pips.append(
                    (archivo['openPrice'].iloc[i] - archivo['closePrice'].iloc[i]) * f_pip_size(
                        archivo['Symbol'].iloc[i]))
            pips_acum.append(pips[0])
            profit_acum.append(archivo['Profit'].iloc[0])

        else:
            if archivo['Type'].iloc[i] == 'buy':
                pips.append(
                    (archivo['closePrice'].iloc[i] - archivo['openPrice'].iloc[i]) * f_pip_size(
                        archivo['Symbol'].iloc[i]))

            else:
                pips.append(
                    (archivo['openPrice'].iloc[i] - archivo['closePrice'].iloc[i]) * f_pip_size(
                        archivo['Symbol'].iloc[i]))

            pips_acum.append(pips_acum[i - 1] + pips[i])
            profit_acum.append(profit_acum[i - 1] + archivo['Profit'].iloc[i])

    archivo['pips'] = pips
    archivo['pips_acum'] = pips_acum
    archivo['profit_acum'] = profit_acum
    return archivo


# %% Aquí hacemos la función para estadistica basica
def f_estadisticas_ba(archivo):
    medida = ['Ops totales', 'Ganadoras', 'Ganadoras_c', 'Ganadoras_v',
              'Perdedoras', 'Perdedoras_c', 'Perdedoras_v', 'Mediana (Profit)', 'Mediana (Pips)', 'r_efectividad',
              'r_proporcion',
              'r_efectividad_c', 'r_efectividad_v']  # hacemos una lista con todo lo necesario en medida

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


# Inicio Parte 2:Métricas de Atribución al Desempeño

# Primer output: Evolucion del capital.(Luz)

def f_evolucion_capital(dt_data):
    # Columna timestamp
    # Quitar el horario a las fechas.
    dt_data['openTime'] = pd.to_datetime(dt_data['openTime'])
    dt_data['openTime'] = dt_data['openTime'].dt.strftime('%Y-%m-%d')
    dpp = pd.DataFrame(columns=['timestamp', 'profit_d', 'profit_acm_d'])
    uu = dt_data['openTime'].unique()
    dpp['timestamp'] = uu
    # Columna profit_d
    pff = []
    for i in range(len(uu)):
        pf = (dt_data[dt_data['openTime'] == dpp['timestamp'][i]]['Profit'])
        pff.append(pf.sum())
    dpp['profit_d'] = pff
    # Columna profit_acm_d
    pacm = dpp['profit_d'].cumsum()
    dpp['profit_acm_d'] = 100000 + pacm
    return dpp


# Segundo output: MAD(Luz)

# Sharpe:

def f_estadisticas_mad(new_df):
    renlog = np.log(new_df['profit_acm_d'] / new_df['profit_acm_d'].shift()).dropna()
    prra = renlog.mean() * 360
    rf = .05
    dva = renlog.std()
    shp = (prra - rf) / dva

    # Draw Down
    maxcap = new_df['profit_acm_d'].max()
    w = new_df[new_df.profit_acm_d == maxcap].index
    f = w[0]
    if f < (len(new_df['profit_acm_d']) - 1):
        fi = new_df['timestamp'][f]
        mincap = new_df['profit_acm_d'][f:].min()
        ff = new_df['timestamp'][new_df[new_df.profit_acm_d == mincap].index[0]]
        drawn_down = (mincap - maxcap) / maxcap

    else:
        evcapn = new_df.shift().dropna().reset_index()
        nmaxcap = evcapn['profit_acm_d'].max()
        wn = evcapn[evcapn.profit_acm_d == nmaxcap].index
        fn = wn[0]
        fi = evcapn['timestamp'][fn]
        nmincap = evcapn['profit_acm_d'][fn:].min()
        ff = evcapn['timestamp'][evcapn[evcapn.profit_acm_d == nmincap].index[0]]
        drawn_down = (nmincap - nmaxcap) / nmaxcap

    # Draw Up

    mincap = new_df['profit_acm_d'].min()
    w = new_df[new_df.profit_acm_d == mincap].index
    f = w[0]
    if f < (len(new_df['profit_acm_d']) - 1):
        fiu = new_df['timestamp'][f]
        maxcap = new_df['profit_acm_d'][f:].max()
        ffu = new_df['timestamp'][new_df[new_df.profit_acm_d == maxcap].index[0]]
        drawn_up = (maxcap - mincap)

    else:
        evcapn = new_df.shift().dropna().reset_index()
        nmincap = evcapn['profit_acm_d'].min()
        wn = evcapn[evcapn.profit_acm_d == nmincap].index
        fn = wn[0]
        fiu = evcapn['timestamp'][fn]
        nmaxcap = evcapn['profit_acm_d'][fn:].min()
        ffu = evcapn['timestamp'][evcapn[evcapn.profit_acm_d == nmaxcap].index[0]]
        drawn_up = (nmaxcap - nmincap)

    # Data frame MAD
    mad = pd.DataFrame(columns=['metrica', 'valor', 'descripción'])
    mad['metrica'] = ['sharpe', 'drawdown_capi', 'drawup_capi']
    mad['valor'] = [shp, [fi, ff, drawn_down], [fiu, ffu, drawn_up]]
    mad['descripción'] = ['Muestra el rendimiento extra por encima de la tasa libre de riesgo que puede esperarse en '
                          'una inversion respecto al riesgo que se asume. '
                          'Un sharpe alto significa que se obtuvo un retorno sobre rf mucho mayor al riesgo que se '
                          'contrae.',
                          'Representa la "racha" de en la que se presento una perdida drastica despues de haber '
                          'llegado al maximo punto de evolucion de capital '
                          'en un periodo de inversion. ', 'Señara el lapso de tiempo donde se tuvo una alba continua '
                                                          'despues de haber tenido la caida maxima del periodo que se '
                                                          'analiza']
    return mad

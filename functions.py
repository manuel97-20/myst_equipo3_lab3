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
import json
from datetime import timedelta                            # diferencia entre datos tipo tiempo
from oandapyV20 import API                                # conexion con broker OANDA
import oandapyV20.endpoints.instruments as instruments    # informacion



def f_leer_archivo(ruta_archivo):
    archivo = pd.read_csv(ruta_archivo, header=0, skip_blank_lines=True)
    archivo = archivo.dropna().reset_index(drop=True)
    archivo = archivo.rename(columns={'Price.1': 'Close Price'}, inplace=False)
    archivo['Close Price'] = pd.to_numeric(archivo['Close Price'])
    archivo['Price'] = pd.to_numeric(archivo['Price'])
    archivo['Profit'] = [i.replace(" ", "") for i in archivo['Profit']]
    archivo['Profit'] = pd.to_numeric(archivo['Profit'])
    archivo['Item'] = [archivo['Item'].iloc[i].replace('-e', '') for i in range(len(archivo))]
    archivo['Item'] = [i.replace('wticousd', 'wtico') for i in archivo['Item']]

    return archivo


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
    open_time = pd.to_datetime(df_data['Open Time'])
    close_time = pd.to_datetime(df_data['Close Time'])
    delta = [(close_time[i] - open_time[i]).total_seconds() for i in range(len(df_data['Open Time']))]
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
                    (archivo['Close Price'].iloc[i] - archivo['Price'].iloc[i]) * f_pip_size(
                        archivo['Item'].iloc[i]))
            else:
                pips.append(
                    (archivo['Price'].iloc[i] - archivo['Close Price'].iloc[i]) * f_pip_size(
                        archivo['Item'].iloc[i]))
            pips_acum.append(pips[0])
            profit_acum.append(archivo['Profit'].iloc[0])

        else:
            if archivo['Type'].iloc[i] == 'buy':
                pips.append(
                    (archivo['Close Price'].iloc[i] - archivo['Price'].iloc[i]) * f_pip_size(
                        archivo['Item'].iloc[i]))

            else:
                pips.append(
                    (archivo['Price'].iloc[i] - archivo['Close Price'].iloc[i]) * f_pip_size(
                        archivo['Item'].iloc[i]))

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

    unicos = np.unique(archivo['Item'])  # listo ya tenemos los unicos
    rank = []
    for i in range(len(unicos)):
        positives = 0
        negatives = 0
        for j in range(len(archivo)):
            if unicos[i] == archivo['Item'].iloc[j] and archivo['Profit'].iloc[j] > 0:
                positives += 1
            elif unicos[i] == archivo['Item'].iloc[j] and archivo['Profit'].iloc[j] < 0:

                negatives += 1

        total = negatives + positives
        rank.append(positives / total)

    df_2 = pd.DataFrame({'symbol': unicos, 'rank': rank})
    df_2 = df_2.sort_values(by='rank', ascending=False)

    final = {'df_1_tabla': df, 'df_2_ranking': df_2}
    return final


# termina la parte 1


# Inicio Parte 2:Métricas de Atribución al Desempeño

# Primer output: Evolucion del capital.

def f_evolucion_capital(dt_data):
    # Columna timestamp
    # Quitar el horario a las fechas.
    sd = pd.DataFrame(columns=['t'])
    sd['t'] = pd.to_datetime(dt_data['Open Time'])
    sd['t'] = sd['t'].dt.strftime('%Y-%m-%d')
    dpp = pd.DataFrame(columns=['timestamp', 'profit_d', 'profit_acm_d'])
    uu = sd['t'].unique()
    dpp['timestamp'] = uu

    # Columna profit_d
    pff = []
    for i in range(len(uu)):
        pf = (dt_data[sd['t'] == dpp['timestamp'][i]]['Profit'])
        pff.append(pf.sum())
    dpp['profit_d'] = pff
    # Columna profit_acm_d
    pacm = dpp['profit_d'].cumsum()
    dpp['profit_acm_d'] = 100000 + pacm
    return dpp


# Segundo output: MAD(Luz)

# Sharpe:

def f_estadisticas_mad(new_df):
    relo = np.diff(np.log(new_df['profit_acm_d']))
    rf = .05 / 300
    dvd = relo.std()
    shp = round(np.mean(relo - rf) / dvd, 5)

    # Draw Down
    lid = []
    for i in np.arange(1, len(new_df['profit_acm_d']), 1):
        if new_df['profit_acm_d'][i] < new_df['profit_acm_d'][i - 1] and new_df['profit_acm_d'][i] < \
                new_df['profit_acm_d'][0]:
            lid.append(i)
            ww = (lid)
    drawn_down = new_df['profit_acm_d'][ww[-1]] - new_df['profit_acm_d'][ww[0]]
    fi = new_df['timestamp'][ww[0]]
    ff = new_df['timestamp'][ww[-1]]

    # Draw Up
    li = []
    for i in np.arange(1, len(new_df['profit_acm_d']), 1):
        if new_df['profit_acm_d'][i] > new_df['profit_acm_d'][i - 1]:
            li.append(i)
            w = (li)
    drawn_up = new_df['profit_acm_d'][w[-1]] - new_df['profit_acm_d'][w[0] - 1]
    fiu = new_df['timestamp'][w[0] - 1]
    ffu = new_df['timestamp'][w[-1]]

    # Data frame MAD
    mad = pd.DataFrame(columns=['metrica', 'valor', 'descripción'])
    mad['metrica'] = ['sharpe', 'drawdown_capi', 'drawup_capi']
    mad['valor'] = [shp, [fi, ff, drawn_down], [fiu, ffu, drawn_up]]
    mad['descripción'] = ['Muestra el rendimiento extra por encima de la tasa libre de riesgo que puede esperarse en '
                          'una inversión respecto al riesgo que se asume. '
                          'Un sharpe alto significa que se obtuvo un retorno sobre rf mucho mayor al riesgo que se '
                          'contrae.',
                          'Representa la "racha" de en la que se presentó una perdida drástica después de haber '
                          'llegado al máximo punto de evolución de capital '
                          'en un periodo de inversión. ', 'Señara el lapso de tiempo donde se tuvo un alba continua '
                                                          'después de haber tenido la caída Máxima del periodo que se '
                                                          'analiza'
                          ]
    return mad


# Operaciones.
def f_be_de(dt_data):
    ot = [(pd.to_datetime(dt_data['Open Time'])[i]) for i in np.arange(0, len(dt_data), 1)]
    ct = [(pd.to_datetime(dt_data['Close Time'])[i]) for i in np.arange(0, len(dt_data), 1)]
    # Saber si al cerrar una operacion ganadora se quedo abierta una con perdida flotante
    gn = []
    ocp = []
    tyg = []
    tyc = []
    for i in np.arange(0, len(dt_data), 1):
        if ct[i] > ct[i - 1] and ot[i] < ct[i - 1] and dt_data.Profit[i - 1] >= 0 and (
                ct[i - 1] - ot[i - 1]).total_seconds() > 910:
            ocp.append(i)  # Posicion de operaciones complementarias con perdida flotante
            gn.append(i - 1)  # Posicion de la operacion ganadora (ancla)
            tyg.append(dt_data.Type[i - 1])
            tyc.append(dt_data.Type[i])



    # -- --------------------------------------------------------- FUNCION: Descargar precios -- #
    # -- Descargar precios historicos con OANDA

    def f_precios_masivos(p0_fini, p1_ffin, p2_gran, p3_inst, p4_oatk, p5_ginc):
        """
        Parameters
        ----------
        p0_fini
        p1_ffin
        p2_gran
        p3_inst
        p4_oatk
        p5_ginc

        Returns
        -------
        dc_precios

        Debugging
        ---------

        """

        def f_datetime_range_fx(p0_start, p1_end, p2_inc, p3_delta):
            """

            Parameters
            ----------
            p0_start
            p1_end
            p2_inc
            p3_delta

            Returns
            -------
            ls_resultado

            Debugging
            ---------
            """

            ls_result = []
            nxt = p0_start

            while nxt <= p1_end:
                ls_result.append(nxt)
                if p3_delta == 'minutes':
                    nxt += timedelta(minutes=p2_inc)
                elif p3_delta == 'hours':
                    nxt += timedelta(hours=p2_inc)
                elif p3_delta == 'days':
                    nxt += timedelta(days=p2_inc)

            return ls_result

        # inicializar api de OANDA

        api = API(access_token=p4_oatk)

        gn = {'S30': 30, 'S10': 10, 'S5': 5, 'M1': 60, 'M5': 60 * 5, 'M15': 60 * 15,
              'M30': 60 * 30, 'H1': 60 * 60, 'H4': 60 * 60 * 4, 'H8': 60 * 60 * 8,
              'D': 60 * 60 * 24, 'W': 60 * 60 * 24 * 7, 'M': 60 * 60 * 24 * 7 * 4}

        # -- para el caso donde con 1 peticion se cubran las 2 fechas
        if int((p1_ffin - p0_fini).total_seconds() / gn[p2_gran]) < 4999:

            # Fecha inicial y fecha final
            f1 = p0_fini.strftime('%Y-%m-%dT%H:%M:%S')
            f2 = p1_ffin.strftime('%Y-%m-%dT%H:%M:%S')

            # Parametros pra la peticion de precios
            params = {"granularity": p2_gran, "price": "M", "dailyAlignment": 16, "from": f1,
                      "to": f2}

            # Ejecutar la peticion de precios
            a1_req1 = instruments.InstrumentsCandles(instrument=p3_inst, params=params)
            a1_hist = api.request(a1_req1)

            # Para debuging
            # print(f1 + ' y ' + f2)
            lista = list()

            # Acomodar las llaves
            for i in range(len(a1_hist['candles']) - 1):
                lista.append({'TimeStamp': a1_hist['candles'][i]['time'],
                              'Open': a1_hist['candles'][i]['mid']['o'],
                              'High': a1_hist['candles'][i]['mid']['h'],
                              'Low': a1_hist['candles'][i]['mid']['l'],
                              'Close': a1_hist['candles'][i]['mid']['c']})

            # Acomodar en un data frame
            r_df_final = pd.DataFrame(lista)
            r_df_final = r_df_final[['TimeStamp', 'Open', 'High', 'Low', 'Close']]
            r_df_final['TimeStamp'] = pd.to_datetime(r_df_final['TimeStamp'])

            return r_df_final

        # -- para el caso donde se construyen fechas secuenciales
        else:

            # hacer series de fechas e iteraciones para pedir todos los precios
            fechas = f_datetime_range_fx(p0_start=p0_fini, p1_end=p1_ffin, p2_inc=p5_ginc,
                                         p3_delta='minutes')

            # Lista para ir guardando los data frames
            lista_df = list()

            for n_fecha in range(0, len(fechas) - 1):

                # Fecha inicial y fecha final
                f1 = fechas[n_fecha].strftime('%Y-%m-%dT%H:%M:%S')
                f2 = fechas[n_fecha + 1].strftime('%Y-%m-%dT%H:%M:%S')

                # Parametros pra la peticion de precios
                params = {"granularity": p2_gran, "price": "M", "dailyAlignment": 16, "from": f1,
                          "to": f2}

                # Ejecutar la peticion de precios
                a1_req1 = instruments.InstrumentsCandles(instrument=p3_inst, params=params)
                a1_hist = api.request(a1_req1)

                # Para debuging
                print(f1 + ' y ' + f2)
                lista = list()

                # Acomodar las llaves
                for i in range(len(a1_hist['candles']) - 1):
                    lista.append({'TimeStamp': a1_hist['candles'][i]['time'],
                                  'Open': a1_hist['candles'][i]['mid']['o'],
                                  'High': a1_hist['candles'][i]['mid']['h'],
                                  'Low': a1_hist['candles'][i]['mid']['l'],
                                  'Close': a1_hist['candles'][i]['mid']['c']})

                # Acomodar en un data frame
                pd_hist = pd.DataFrame(lista)
                pd_hist = pd_hist[['TimeStamp', 'Open', 'High', 'Low', 'Close']]
                pd_hist['TimeStamp'] = pd.to_datetime(pd_hist['TimeStamp'])

                # Ir guardando resultados en una lista
                lista_df.append(pd_hist)

            # Concatenar todas las listas
            r_df_final = pd.concat([lista_df[i] for i in range(0, len(lista_df))])

            # resetear index en dataframe resultante porque guarda los indices del dataframe pasado
            r_df_final = r_df_final.reset_index(drop=True)

            return r_df_final
    gns = [14, 9, 6]
    #ocps = [15, 10, 7]

    if gn[0] == gns[0]:
        ff = "2020-10-06 11:16:20"
        fi = "2020-10-05 00:24:27"
        OA_In = "EUR_USD";
    if gn[0] == gns[1]:
        ff = "2020-10-01 16:24:16"
        fi = "2020-09-28 21:58:28"
        OA_In = "WTICO_USD"
    if gn[0] == gns[2]:
        ff = "2020-10-05 00:28:34"
        fi = "2020-09-30 00:17:15"
        OA_In ="AUD_USD"
    OA_Gn = "D";  # Granularidad de velas
    fini = pd.to_datetime(fi).tz_localize('America/Mexico_City');  # Fecha inicial
    ffin = pd.to_datetime(ff).tz_localize('America/Mexico_City');  # Fecha
    OA_Ak = "90fb85dd7f0d7dc632de8e58ae42f263-7883ae215e6ff58d58aa33d95dfbb1e9"
    data = f_precios_masivos(p0_fini=fini, p1_ffin=ffin, p2_gran=OA_Gn, p3_inst=OA_In, p4_oatk=OA_Ak, p5_ginc=4900)
    tyo = dt_data.Type[ocp[0]]
    nc = np.array(data.Close[-1:])
    no = dt_data.Price[ocp[0]]
    nc = nc.astype(np.float)
    s = (dt_data.Size[gn[0]])
    apca = 100000 * 0.0001
    if tyo == "sell":
        p = no - nc
    else:
        p = nc - no
    p_value = apca * nc * p

    if p > 0:
        res=pd.DataFrame({'ocurrencias': [0], 'status_quo':['0%'], 'aversion_perdida':['0%'], 'sensibilidad_decreciente':['NO']})

        ocurrencia_1 = {'cantidad': 0, 'ocurrencia_1': {'timestamp': 'Ninguno', 'operaciones': {
            'Ganadora': {'intrumento': 'Ninguno', 'volumen': 'Ninguno', 'sentido': 'Ninguno',
                         'profit_ganadora': 'Ninguno'},
            'Perdedora': {'intrumento': 'Ninguno', 'volumen': 'Ninguno', 'sentido': 'Ninguno',
                          'profit_perdedora': 'Ninguno'}}},
                        'resultados': res}
    else:

        res=pd.DataFrame({'ocurrencias':[len(gn)], 'status_quo':[0], 'aversion_perdida':[1], 'sensibilidad_decreciente':[1]})

        if round(float((apca * nc * p)), 2) / dt_data.profit_acum[gn[0]] < dt_data.Profit[gn[0]] / dt_data.profit_acum[
            gn[0]]:
            res.status_quo='100%'
        else:
            res.status_quo = '0%'
        if round(float((apca * nc * p)), 2)/dt_data.Profit[gn[0]] >2:
            res.aversion_perdida='100%'
        else:
            res.aversion_perdida = '0%'

        if round(float((apca * nc * p)), 2)/dt_data.Profit[gn[0]] >2 and dt_data.Profit[gn[0]]<dt_data.Profit[gn[0]+1]:
            res.sensibilidad_decreciente= 'Sí'
        else:
            res.sensibilidad_decreciente='No'

        ocurrencia_1 = {'ocurrencias':
            {'cantidad': len(gn), 'ocurrencia_1': {'timestamp': dt_data['Close Time'][gn[0]], 'operaciones': {
                'Ganadora': {'intrumento': (dt_data.Item[gn[0]]).upper(), 'volumen': 'Ninguno',
                             'sentido': dt_data.Type[gn[0]],
                             'profit_ganadora': dt_data.Profit[gn[0]]},
                'Perdedora': {'intrumento': (dt_data.Item[ocp[0]]).upper(), 'volumen': 'Ninguno',
                              'sentido': (dt_data.Type[ocp[0]]),
                              'profit_perdedora': round(float((apca * nc * p)), 2)}}},
             'ratio_cp_profit_acm': round(float((apca * nc * p)), 2) / dt_data.profit_acum[gn[0]],
             'ratio_cg_profit_acm': dt_data.Profit[gn[0]] / dt_data.profit_acum[gn[0]],
             'ratio_cp_cg': round(float((apca * nc * p)), 2) / dt_data.Profit[gn[0]]},
                        'resultados': res}


    return (ocurrencia_1)


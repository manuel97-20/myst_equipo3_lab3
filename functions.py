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


    ticker_up = ticker_f.upper()
    if ticker_up == 'WTICO':

        indx = np.concatenate(np.where(ticker_up == dt.oanda_instruments.index))
        temp = dt.oanda_instruments['PipLocation'].iloc[indx]

    else:
        ticker_up = ticker_up[:3] + '.' + ticker_up[3:]  # ponemos todos en mayusculas

        indx = np.where(ticker_up == dt.oanda_instruments.index)
        print(indx)
        temp = dt.oanda_instruments['PipLocation'].iloc[indx]

    return ticker_up,indx

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

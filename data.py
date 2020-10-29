"""
# -- --------------------------------------------------------------------------------------------------- -- #
# -- project: A SHORT DESCRIPTION OF THE PROJECT                                                         -- #
# -- script: data.py : python script for data collection                                                 -- #
# -- author: YOUR GITHUB USER NAME                                                                       -- #
# -- license: GPL-3.0 License                                                                            -- #
# -- repository: YOUR REPOSITORY URL                                                                     -- #
# -- --------------------------------------------------------------------------------------------------- -- #
"""
import pandas as pd

oanda_instruments = r'C:\Users\manue\Documents\Documentos\Microestructura y sistemas de trading\myst_equipo3_lab3\Oanda_Instruments.csv'
oanda_instruments = pd.read_csv(oanda_instruments,
                                header=0, sep=',', index_col=0, parse_dates=False,
                                skip_blank_lines=True)

archivo = archivo = r'C:\Users\manue\Documents\Documentos\Microestructura y sistemas de trading\myst_equipo3_lab3\Statement.csv'
archivo = pd.read_csv(archivo, header=0, skip_blank_lines=True)
archivo = archivo.dropna().reset_index(drop=True)
archivo = archivo.rename(columns = {'Price.1': 'Close Price'}, inplace = False)
archivo['Close Price'] = pd.to_numeric(archivo['Close Price'])
archivo['Price'] = pd.to_numeric(archivo['Price'])
archivo['Profit'] = [i.replace(" ", "") for i in archivo['Profit']]
archivo['Profit'] = pd.to_numeric(archivo['Profit'])
archivo['Item'] = [archivo['Item'].iloc[i].replace('-e', '') for i in range(len(archivo))]
archivo['Item'] = [i.replace('wticousd', 'wtico') for i in archivo['Item']]


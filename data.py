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

oanda_instruments = 'c:/Users/luzitaifi/Documents/Micro_Estructuras_Trading/Lab_3/myst_equipo3_lab3/Oanda_Instruments' \
                    '.csv '
oanda_instruments = pd.read_csv(oanda_instruments,
                                header=0, sep=',', index_col=0, parse_dates=False,
                                skip_blank_lines=True)
archivo = archivo = 'c:/Users/luzitaifi/Documents/Micro_Estructuras_Trading/Lab_3/myst_equipo3_lab3' \
                    '/archivo_tradeview_1.csv '
archivo = pd.read_csv(archivo, header=0)

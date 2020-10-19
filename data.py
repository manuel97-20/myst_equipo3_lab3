
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
oanda_instruments = r'C:\Users\manue\Documents\Documentos\Microestructura y sistemas de trading/Oanda_instruments.csv'
oanda_instruments = pd.read_csv(oanda_instruments,
                                  header=0)
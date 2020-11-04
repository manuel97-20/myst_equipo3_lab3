
"""
# -- --------------------------------------------------------------------------------------------------- -- #
# -- project: A SHORT DESCRIPTION OF THE PROJECT                                                         -- #
# -- script: visualizations.py : python script with data visualization functions                         -- #
# -- author: YOUR GITHUB USER NAME                                                                       -- #
# -- license: GPL-3.0 License                                                                            -- #
# -- repository: YOUR REPOSITORY URL                                                                     -- #
# -- --------------------------------------------------------------------------------------------------- -- #
"""

import plotly.graph_objects as go
import plotly.express as px
import main as mn
import numpy as np

rank = mn.diccionario['df_2_ranking']

labels = rank['symbol']
values = rank['rank']

# pull is given as a fraction of the pie radius
fig_1 = go.Figure(data=[go.Pie(labels=labels, values=values, pull=[0.2,0.2,0,0,0,0,0])])
fig_1.update_layout(title='Ranking')
fig_1.show()


# Add data
timestamp = mn.evcap['timestamp']
draw_down_x = timestamp.iloc[1:9]
draw_up_x =timestamp.iloc[4:]
profit_acum = mn.evcap['profit_acm_d']
draw_down_y = profit_acum.iloc[1:9]
draw_up_y = profit_acum.iloc[4:]
fig = go.Figure()
# Create and style traces
fig.add_trace(go.Scatter(x=timestamp, y=profit_acum, name='Profit Acum',
                     line=dict(color='black', width=4)))
fig.add_trace(go.Scatter(x=draw_down_x, y=draw_down_y, name = 'draw_down',
                        line=dict(color='red', width=4, dash='dot')))
fig.add_trace(go.Scatter(x=draw_up_x, y=draw_up_y, name='draw_up',
                         line=dict(color='green', width=4,
                              dash='dot')))

fig.update_layout(title='Average High and Low Temperatures in New York',
                   xaxis_title='Month',
                   yaxis_title='Temperature (degrees F)')


fig.show()



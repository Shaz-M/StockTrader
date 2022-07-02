import plotly.graph_objects as go
from plotly.offline import plot

import pandas as pd

def getChart():
    df =  pd.DataFrame([[1, 2], [3, 4]], columns=['Date','Price'])
    fig = go.Figure([go.Scatter(x=df['Date'], y=df['Price'])])
    plot_div = plot(fig,output_type='div', include_plotlyjs=False)
    return plot_div
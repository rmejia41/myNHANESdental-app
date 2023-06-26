from dash import Dash, html, dcc, Input, Output  # pip install dash
import dash_bootstrap_components as dbc
import pandas as pd
import plotly_express as px
import numpy as np

import altair as alt                        # pip install altair

import matplotlib.pyplot as plt             # pip install matplotlib
import mpld3                                # pip install mpld3

from bokeh.plotting import figure           # pip install Bokeh
from bokeh.resources import CDN
from bokeh.embed import file_html
from bokeh.models import ColumnDataSource


# bring data into app
df = pd.read_csv('https://github.com/rmejia41/open_datasets/raw/main/caries_nhanes_demo_cariesonly.csv')
#print(df.columns)

  #Set up Dash app
app = Dash(__name__, external_stylesheets=['https://codepen.io/chriddyp/pen/bWLwgP.css'])
server = app.server


# Set up the page layout
app.layout = dbc.Container([
    html.H1("Dasboard: Correlation Between Dental Caries Indicators and Age, NHANES, 1999-2004"),

    html.Iframe(
        id='scatterplots',
        srcDoc=None, # here is where we will put the graph we make
        style={'border-width': '5', 'width': '100%', 'height': '500px'}),

    html.H5("Select Y column for graph", className='mt-2'),
    dcc.Dropdown(
        id='mydropdown',
        value='Total Caries Indicators',
        options=[{'label': col, 'value': col} for col in df.columns])
])

# Create interactivity between dropdown and graph
@app.callback(
    Output(component_id='scatterplots', component_property='srcDoc'),
    Input(component_id='mydropdown', component_property='value'))
def plot_data(selected_ycol):
    print(f"User Selected this dropdown value: {selected_ycol}")

    # Altair graphing library----------------------------------------------
    # chart = alt.Chart(df).mark_circle().encode(
    #     x='Poverty',
    #     y=selected_ycol,
    #     tooltip=selected_ycol).interactive()
    # html_altair = chart.to_html()

    # Matplotlib graphing library------------------------------------------
    colvalue = df[selected_ycol]
    fig, ax = plt.subplots()
    ax.scatter(x=df.Age, y=colvalue, color='red')
    ax.set_xlabel("Age", fontsize=14)
    ax.set_ylabel(selected_ycol, fontsize=14)
    ax.grid(color='lightgray', alpha=0.7)
    html_matplotlib = mpld3.fig_to_html(fig)


    # Bokeh graphing library-----------------------------------------------
    # sourcedata = ColumnDataSource(df.copy())
    # plot = figure(x_axis_label='Poverty', y_axis_label=selected_ycol)
    # plot.scatter(x='Poverty', y=selected_ycol, source=sourcedata)
    # html_bokeh = file_html(plot, CDN)

    return html_matplotlib

if __name__ == '__main__':
    app.run_server(debug=True, port=8001)



import dash
from dash import Dash,html,dash_table,dcc,Input,Output,callback
import pandas as pd 
import plotly.express as px

from Data_Prediction_Plus_Analysis import VolumeAnalysis

volumeanalysis=VolumeAnalysis()
volumeanalysis.daily_volume_change()
volumeanalysis.corrleation_volume_change()
volumeanalysis.correlation_with_stock_price()
change_daily=volumeanalysis.change_table()

dash.register_page(__name__)


layout=html.Div([

    html.H2(children="Volume Change Per Day",style={"textAlign":"center"}),

    dcc.Dropdown(id="vol_ids",options=["Total","BMO","Scotiabank","National Bank of Canada","RBC","TD","CIBC"],value="Total",style={"width":"58%"}),

    dcc.Graph(id='vol_graphs')

])

@callback( 
    Output("vol_graphs","figure"),
    Input("vol_ids","value")
)

def volumne_graph(ticker):
    if ticker!="Total":
        figure=px.line(change_daily,x="Date",y=ticker)
        figure.update_layout(plot_bgcolor='#FFFFFF',paper_bgcolor='#FFFFFF',font_color="#000000")
    else:
        figure=px.line(change_daily,x="Date",y=change_daily.columns)
        figure.update_layout(plot_bgcolor='#FFFFFF',paper_bgcolor='#FFFFFF',font_color="#000000")
    return figure
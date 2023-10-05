import dash
from dash import Dash,html,dash_table,dcc,Input,Output,callback
import pandas as pd 
import plotly.express as px


dash.register_page(__name__,path="/")

layout=html.Div([
  #  html.H1(children="Stock Analysis",style={"textAlign":"center"}),

    html.H2(children="Thank you for using my DashBoard!",style={"textAlign":"center"}),

    html.H2(children="This dashboard has plots for Predictions (ARIMA) and analysis of daily returns and volume change!",style={"textAlign":"center"}),


])
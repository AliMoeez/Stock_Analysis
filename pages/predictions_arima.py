import dash
from dash import Dash,html,dash_table,dcc,Input,Output,callback
import pandas as pd 
import plotly.express as px


from  Data_Prediction_Plus_Analysis import Prediction

prediction=Prediction()
prediction.SARIMA_model()
all_arima,all_arima_forecast=prediction.arima_predictions()


dash.register_page(__name__)


layout=html.Div([

    html.H2(children="Arima Predictions",style={"textAlign":"center"}),

    dcc.Dropdown(id="TS Prediction ARIMA ids",options=["BMO","Scotiabank","National Bank of Canada","RBC","TD","CIBC"],value="BMO",style={"width":"58%"}),

    dcc.Graph(id="TS Prediction ARIMA")
    
])

@callback(
    Output("TS Prediction ARIMA","figure"),
    Input("TS Prediction ARIMA ids","value")
)

#def display_time_series(ticker):
#    figure=px.line(all_arima,x="Date",y=ticker)
#    return figure

def display_time_series_forecast(ticker):
    figure=px.line(all_arima_forecast,x="Date",y=ticker)
    return figure
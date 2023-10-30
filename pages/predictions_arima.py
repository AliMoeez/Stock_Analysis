import dash
from dash import Dash,html,dash_table,dcc,Input,Output,callback
import pandas as pd 
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go
from  Data_Prediction_Plus_Analysis import Prediction

prediction=Prediction()
prediction.SARIMA_model()
prediction.confidence_interval()
all_arima,all_arima_forecast,arima_ci_upper,arima_ci_lower=prediction.arima_predictions()


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

def display_time_series(ticker):
    figure=make_subplots(rows=1,cols=1)
    figure.update_layout(plot_bgcolor='#FFFFFF',paper_bgcolor='#FFFFFF',font_color="#000000")
    figure.append_trace(go.Scatter(x=all_arima["Date"],y=all_arima[ticker],mode="lines",name="Data",),row=1,col=1)
    figure.append_trace(go.Scatter(x=all_arima_forecast["Date"],y=all_arima_forecast[ticker],mode="lines",name="Forecast"),row=1,col=1)

    figure.append_trace(go.Scatter(x=arima_ci_upper["Date"],y=arima_ci_upper[ticker],mode="lines",
                                name="Forecast CI",marker=dict(color="grey"),
                                line=dict(width=1)),row=1,col=1)
    
    figure.append_trace(go.Scatter(x=arima_ci_lower["Date"],y=arima_ci_lower[ticker],mode="lines",
                                name="Forecast CI",marker=dict(color="grey"),
                                line=dict(width=1),fillcolor='rgba(51,51,52,0.3)',fill='tonexty'),row=1,col=1)

    return figure



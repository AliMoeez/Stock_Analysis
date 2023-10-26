import dash
from dash import Dash,html,dash_table,dcc,Input,Output,callback
import pandas as pd 
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go

from Data_Prediction_Plus_Analysis import NeuralNetowrkAnalysis

neuralnetworkanalysis=NeuralNetowrkAnalysis()
neuralnetworkanalysis.add_timeline()
#neuralnetworkanalysis.data_conslidation()
#neuralnetworkanalysis.data_into_array()
#neuralnetworkanalysis.model()
#neuralnetworkanalysis.model_compile()
#neuralnetworkanalysis.model_predict()
neural_network_model_df=neuralnetworkanalysis.model_df()
#neural_netowrk_model_df_prediction=neuralnetworkanalysis.model_df_prediction()

dash.register_page(__name__)

layout=html.Div([

    html.H2(children="Neural Network Stock Predictions",style={"textAlign:center"}),

    dcc.Dropdown(id="NNDD",options={"BMO","Scotiabank","National Bank of Canada","RBC","TD","CIBC"},value="BMO",style={"width:50%"}),

    dcc.Graph(id="NN Graph")
    
])


@callback(
    Output("NN Graph","figure"),
    Input("NNDD","value")
)

def show_neural_network(ticker):
    figure=make_subplots(rows=1,columns=1)
    figure.update_layout(plot_bgcolor="#484848",paper_bgcolor="#484848",font_color="#FFFFFF")
    figure.append_trace(go.Scatter(x=neural_network_model_df["Time"],y=neural_network_model_df[ticker],mode="lines",name="Data"),row=1,col=1)
  #  figure.append_trace(go.scatter(x=neural_netowrk_model_df_prediction["Time"],y=neural_network_model_df[ticker],mode="lines",name="Data"),row=1,col=1)
    return figure


#def display_time_series(ticker):
#    figure=make_subplots(rows=1,cols=1)
#    figure.update_layout(plot_bgcolor='#484848',paper_bgcolor='#484848',font_color="#FFFFFF")
#    figure.append_trace(go.Scatter(x=all_arima["Date"],y=all_arima[ticker],mode="lines",name="Data",),row=1,col=1)



import dash
from dash import Dash,html,dash_table,dcc,Input,Output,callback
import pandas as pd 
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go

from Data_Prediction_Plus_Analysis import NeuralNetworkAnalysis

neuralnetworkanalysis1=NeuralNetworkAnalysis()
neuralnetworkanalysis1.add_timeline()
neuralnetworkanalysis1.data_conslidation()
neuralnetworkanalysis1.data_into_array()
neuralnetworkanalysis1.model()
neuralnetworkanalysis1.model_compile()
neuralnetworkanalysis1.model_predict()
neuralnetworkanalysis1.model_plot()
neural_network_model_df=neuralnetworkanalysis1.model_df()
neural_netowrk_model_df_prediction=neuralnetworkanalysis1.model_df_prediction()

dash.register_page(__name__)

layout=html.Div([

    html.H2(children="Neural Network Stock Predictions",style={"textAlign":"center"}),

    dcc.Dropdown(id="NNDD",options=["BMO","Scotiabank","National Bank of Canada","RBC","TD","CIBC"],value="BMO",style={"width":"50%"}),

    dcc.Graph(id="NN Graph")
    
])


@callback(
    Output("NN Graph","figure"),
    Input("NNDD","value")
)

def show_neural_network(ticker):
    figure=make_subplots(rows=1,cols=1)
    figure.update_layout(plot_bgcolor="#FFFFFF",paper_bgcolor="#FFFFFF",font_color="#000000")
    figure.append_trace(go.Scatter(x=neural_network_model_df["Time"],y=neural_network_model_df[ticker],mode="lines",name="Data"),row=1,col=1)
    figure.append_trace(go.Scatter(x=neural_netowrk_model_df_prediction["Time"],y=neural_netowrk_model_df_prediction[ticker],mode="lines",name="Prediction"),row=1,col=1)
    return figure
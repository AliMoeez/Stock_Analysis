from dash import Dash,html,dash_table,dcc,Input,Output
import pandas as pd 
import plotly.express as px

from Data_Prediction_Plus_Analysis import StockReturn,Volume_Analysis,Predictions

stockreturn=StockReturn()
stockreturn.data_consolidation()
stockreturn.daily_stock_return()
stockreturn.yearly_stock_return()
all_daily_returns=stockreturn.df_all_daily_return()

app=Dash(__name__)

app.layout=html.Div([
    html.H1(children="Stock Analysis",style={"textAlign":"center"}),

    html.H2(children="Daily Stock Return Per Company",style={"textAlign":"center"}),


    dcc.Dropdown(id="DSRPC", options=["Total","BMO","Scotiabank","National Bank of Canada","RBC","TD","CIBC"],value="Total",style={"width":"58%"}),

    dcc.Graph(id="DSRPC Graph")


])


@app.callback(
    Output("DSRPC Graph","figure"),
    Input("DSRPC","value")
)

def show_daily_stock_return(ticker):
    df_daily_stock_return=all_daily_returns
    if ticker!="Total":
        figure=px.line(df_daily_stock_return,x="Date",y=ticker)
    else:
        figure=px.line(df_daily_stock_return,x="Date",y=df_daily_stock_return.columns,labels={"value":"All Companies"})
    return figure


if __name__=='__main__':
    app.run(debug=True)



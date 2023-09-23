from dash import Dash,html,dash_table,dcc
import pandas as pd 
import plotly.express as px

from Data_Prediction_Plus_Analysis import MaxMin

maxmin=MaxMin()
maxmin.max_open()
test=maxmin.plotly_return()

app=Dash(__name__)

app.layout=html.Div([
    html.H1(children="Stock Analysis",style={"textAlign":"center"}),

    html.H2(children="Graph 1 Sets",style={"textAlign":"left"}),

   # figs=px.scatter(test)

    dcc.Graph(figure={
        'data':[
            {'x': list(test.keys()),'y': list(test.values()),'type':'bar'}
        ],
        'layout':{
            'title':"Max Open Prices",
            
        }
    })

     


  #  dash_table.DataTable(data=df_rbc.to_dict("records"),page_size=5,
  #                       style_header={ 'backgroundColor':'rgb(28,28,28)', 'color':'white'},
  #                       style_data={'backgroundColor':'rgb(72,72,72)','color':'white'})
])



if __name__=='__main__':
    app.run(debug=True)
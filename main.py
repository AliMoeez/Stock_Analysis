import dash
from dash import Dash,html,dash_table,dcc,Input,Output
import pandas as pd 
import plotly.express as px
import plotly.graph_objects as go


app=Dash(__name__,use_pages=True)

app.layout=html.Div([

    html.H1(children="Stock Analysis",style={"textAlign":"center"}),

    html.H2(children="Press Below To Find The Dashbaord Of Your Liking!",style={"textAlign":"center"}),

    html.Div([
    html.Div(
        dcc.Link(f"{page['name']}",href=page["relative_path"]),
    style={"width":"20%","display":"inline-block"}) for page in dash.page_registry.values()

    ]),
    dash.page_container
])

if __name__=='__main__':
    app.run(debug=True)

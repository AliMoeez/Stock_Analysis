import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd 


df_1=pd.DataFrame(data={
    "One":[1,2,3,4],
    "Two":[121,123,241,123]
})

df_2=pd.DataFrame(data={
    "One":[4,5,6,7,8],
    "Two":[175,121,123,123,123]
})

df_3_up=pd.DataFrame(data={
    "One":[4,5,6,7,8],
    "Two":[195,151,173,183,183]
})

df_4_lo=pd.DataFrame(data={
    "One":[4,5,6,7,8],
    "Two":[125,111,113,113,123]
})


fig=make_subplots(rows=1,cols=1)

fig.append_trace(go.Scatter(x=df_1["One"],y=df_1["Two"],mode="lines",name="Data",),row=1,col=1)
fig.append_trace(go.Scatter(x=df_2["One"],y=df_2["Two"],mode="lines",name="Forecast"),row=1,col=1)

fig.append_trace(go.Scatter(x=df_3_up["One"],y=df_3_up["Two"],mode="lines",
                            name="Forecast CI",marker=dict(color="grey"),
                            line=dict(width=1)),row=1,col=1)
fig.append_trace(go.Scatter(x=df_4_lo["One"],y=df_4_lo["Two"],mode="lines",
                            name="Forecast CI",marker=dict(color="grey"),
                            line=dict(width=1),fillcolor='rgba(10,10,10,0.3)',fill='tonexty'),row=1,col=1)

fig.show()
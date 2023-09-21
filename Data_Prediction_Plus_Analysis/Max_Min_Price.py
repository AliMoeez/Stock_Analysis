import pandas as pd
import matplotlib.pyplot as plt

#lode csv files using pyarrow engine to make the csv files load faster
df_rbc=pd.read_csv(r"Data\Data_Sets\RBC_TO.csv", engine="pyarrow")
df_scotia=pd.read_csv(r"Data\Data_Sets\BNS.TO.csv",engine="pyarrow")
df_cibc=pd.read_csv(r"Data\Data_Sets\CIBC.TO.csv",engine="pyarrow")
df_naboc=pd.read_csv(r"Data\Data_Sets\NABOC.TO.csv",engine="pyarrow")
df_td=pd.read_csv(r"Data\Data_Sets\TD.TO.csv",engine="pyarrow")

class MaxMin:
    def __init__(self):
        self.df_rbc=df_rbc ; self.df_scotia=df_scotia ; self.df_cibc=df_cibc ; self.df_naboc=df_naboc ; self.df_td=df_td

    def max_open(self):      
        #find the maximum open prices of  each company
        self.rbc_max_open=max(df_rbc["Open"]) ; self.scotia_max_open=max(df_scotia["Open"]) ;self.cibc_max_open=max(df_cibc["Open"])  
        self.naboc_max_open=max(df_naboc["Open"]) ; self.td_max_open=max(df_td["Open"])
    
    def min_open(self):
        #find the minimum open prices of each company
        self.rbc_min_open=min(df_rbc["Open"]) ; self.scotia_min_open=min(df_scotia["Open"]) ; self.cibc_min_open=min(df_cibc["Open"]) 
        self.naboc_min_open=min(df_naboc["Open"]) ; self.td_min_open=min(df_td["Open"])

    def max_close(self):
        #find the maximum close prices of  each company
        self.rbc_max_open=max(df_rbc["Close"]) ; self.scotia_max_open=max(df_scotia["Close"]) ; self.cibc_max_open=max(df_cibc["Close"]) 
        self.naboc_max_open=max(df_naboc["Close"]) ; self.td_max_open=max(df_td["Close"])

    def min_close(self):
        #find the minimum close prices of each company
        self.rbc_min_open=min(df_rbc["Close"]) ; self.scotia_min_open=min(df_scotia["Close"]) ; self.cibc_min_open=min(df_cibc["Close"]) 
        self.naboc_min_open=min(df_naboc["Close"]) ; self.td_min_open=min(df_td["Close"])

    def graphs(self):
        #vislizations using matplotlib
        pass

maxmin=MaxMin()
maxmin.max_open()
maxmin.min_open()
maxmin.max_close()
maxmin.min_close()
maxmin.graphs()





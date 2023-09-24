#Stock return is defined as ((P1-P0)+Div)/P0 where P1=End Price, P0=Start Price, Div=Divedends
#This program will compute the daily stock return + divideends (on applicable dates) and produce
#A daily return for stock which will be plotted. A total yearly stock return will be computed  and graphed as well

import pandas as pd
import numpy as np 
import math 

class StockReturn:
    def __init__(self):
        #Lode stock csv files using pyarrow for faster loading times
        self.df_bmo=pd.read_csv(r"Data\Stock Prices\BMO.TO.csv", engine="pyarrow")  ; self.df_rbc=pd.read_csv(r"Data\Stock Prices\RBC_TO.csv", engine="pyarrow") 
        self.df_scotia=pd.read_csv(r"Data\Stock Prices\BNS.TO.csv",engine="pyarrow") ; self.df_cibc=pd.read_csv(r"Data\Stock Prices\CIBC.TO.csv",engine="pyarrow") 
        self.df_naboc=pd.read_csv(r"Data\Stock Prices\NABOC.TO.csv",engine="pyarrow")  ; self.df_td=pd.read_csv(r"Data\Stock Prices\TD.TO.csv",engine="pyarrow")
        #Lode dividened csv files using pyarrow for faster loading times
        self.df_bmo_div=pd.read_csv(r"Data\Dividends\BMO.TO (1).csv", engine="pyarrow")  ; self.df_rbc_div=pd.read_csv(r"Data\Dividends\RY.TO.csv", engine="pyarrow") 
        self.df_scotia_div=pd.read_csv(r"Data\Dividends\BNS.TO (1).csv",engine="pyarrow") ; self.df_cibc_div=pd.read_csv(r"Data\Dividends\CIBC.TO (1).csv",engine="pyarrow") 
        self.df_naboc_div=pd.read_csv(r"Data\Dividends\NABOC.TO (1).csv",engine="pyarrow") ; self.df_td_div=pd.read_csv(r"Data\Dividends\TD.TO (1).csv",engine="pyarrow")

    def data_consolidation(self):
        #Combine each stock with its divdend by create a dataframe that includes the stock prices and divdends for each company
        #Use a left join on Date to join all values from the stock df and corresponding values from the divdends table
        self.df_bmo_total=pd.merge(self.df_bmo,self.df_bmo_div,on="Date",how="left")
        self.df_scotia_total=pd.merge(self.df_bmo,self.df_scotia_div,on="Date",how="left")
        self.df_naboc_total=pd.merge(self.df_bmo,self.df_naboc_div,on="Date",how="left")
        self.df_rbc_total=pd.merge(self.df_bmo,self.df_rbc_div,on="Date",how="left")
        self.df_cibc_total=pd.merge(self.df_bmo,self.df_cibc_div,on="Date",how="left")
        self.df_td_total=pd.merge(self.df_bmo,self.df_td_div,on="Date",how="left")

    def daily_stock_return(self):
        #computing daily stock returns including the divdends for each company

        self.df_bmo_total["Dividends"]=self.df_bmo_total["Dividends"].replace(np.nan,0)

        for i in self.df_bmo_total["Open"]:
            for j in self.df_bmo_total["Close"]:
                    print(i-j)
    
stockreturn=StockReturn()
stockreturn.data_consolidation()
stockreturn.daily_stock_return()



#Stock return is defined as ((P1-P0)+Div)/P0 where P1=End Price, P0=Start Price, Div=Divedends
#This program will compute the daily stock return + divideends (on applicable dates) and produce
#A daily return for stock which will be plotted. A total yearly stock return will be computed and graphed as well

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
        self.df_scotia_total=pd.merge(self.df_scotia,self.df_scotia_div,on="Date",how="left")
        self.df_naboc_total=pd.merge(self.df_naboc,self.df_naboc_div,on="Date",how="left")
        self.df_rbc_total=pd.merge(self.df_rbc,self.df_rbc_div,on="Date",how="left")
        self.df_cibc_total=pd.merge(self.df_cibc,self.df_cibc_div,on="Date",how="left")
        self.df_td_total=pd.merge(self.df_td,self.df_td_div,on="Date",how="left")

    def daily_stock_return(self):
        #computing daily stock returns including the divdends for each company
        #replace al NaN values with 0 to make computation of daily stock returns easier
        self.df_bmo_total["Dividends"]=self.df_bmo_total["Dividends"].replace(np.nan,0) ; self.df_scotia_total["Dividends"]=self.df_scotia_total["Dividends"].replace(np.nan,0)
        self.df_naboc_total["Dividends"]=self.df_naboc_total["Dividends"].replace(np.nan,0) ; self.df_rbc_total["Dividends"]=self.df_rbc_total["Dividends"].replace(np.nan,0)
        self.df_cibc_total["Dividends"]=self.df_cibc_total["Dividends"].replace(np.nan,0) ; self.df_td_total["Dividends"]=self.df_td_total["Dividends"].replace(np.nan,0)
        #Use the stock return formula on each df by creating a new colum which stores the computations of the daily return
        self.df_bmo_total["Daily Returns"]=((self.df_bmo_total["Close"]-self.df_bmo_total["Open"]+self.df_bmo_total["Dividends"])/self.df_bmo_total["Open"])*100  ; self.df_scotia_total["Daily Returns"]=((self.df_scotia_total["Close"]-self.df_scotia_total["Open"]+self.df_scotia_total["Dividends"])/self.df_scotia_total["Open"])*100
        self.df_naboc_total["Daily Returns"]=((self.df_naboc_total["Close"]-self.df_naboc_total["Open"]+self.df_naboc_total["Dividends"])/self.df_naboc_total["Open"])*100 ; self.df_rbc_total["Daily Returns"]=((self.df_rbc_total["Close"]-self.df_rbc_total["Open"]+self.df_rbc_total["Dividends"])/self.df_rbc_total["Open"])*100
        self.df_cibc_total["Daily Returns"]=((self.df_cibc_total["Close"]-self.df_cibc_total["Open"]+self.df_cibc_total["Dividends"])/self.df_cibc_total["Open"])*100 ; self.df_td_total["Daily Returns"]=((self.df_td_total["Close"]-self.df_td_total["Open"]+self.df_td_total["Dividends"])/self.df_td_total["Open"])*100

    def yearly_stock_return(self):
        #compuitng the yearly stock return including dividends for each company
        #formula will take the closing price less the open price plus dividends divided by the open price times 100 to get the return
        self.bmo_total_dividend=sum(self.df_bmo_total["Dividends"]) ; self.bmo_open_price=self.df_bmo_total["Open"].iloc[0] ; self.bmo_close_price=self.df_bmo_total["Close"].iloc[-1]
        self.bmo_yearly_stock_return=round(((self.bmo_close_price-self.bmo_open_price+self.bmo_total_dividend)/self.bmo_open_price)*100,4)
        
        self.scotia_total_dividend=sum(self.df_scotia_total["Dividends"]) ; self.scotia_open_price=self.df_scotia_total["Open"].iloc[0] ; self.scotia_close_price=self.df_scotia_total["Close"].iloc[-1]
        self.scotia_yearly_stock_return=round(((self.scotia_close_price-self.scotia_open_price+self.scotia_total_dividend)/self.scotia_open_price)*100,4)
        
        self.naboc_total_dividend=sum(self.df_naboc_total["Dividends"]) ; self.naboc_open_price=self.df_naboc_total["Open"].iloc[0] ; self.naboc_close_price=self.df_naboc_total["Close"].iloc[-1]
        self.naboc_yearly_stock_return=round(((self.naboc_close_price-self.naboc_open_price+self.naboc_total_dividend)/self.naboc_open_price)*100,4)
        
        self.rbc_total_dividend=sum(self.df_rbc_total["Dividends"]) ; self.rbc_open_price=self.df_rbc_total["Open"].iloc[0] ; self.rbc_close_price=self.df_rbc_total["Close"].iloc[-1]
        self.rbc_yearly_stock_return=round(((self.rbc_close_price-self.rbc_open_price+self.rbc_total_dividend)/self.rbc_open_price)*100,4)
        
        self.cibc_total_dividend=sum(self.df_cibc_total["Dividends"]) ; self.cibc_open_price=self.df_cibc_total["Open"].iloc[0] ; self.cibc_close_price=self.df_cibc_total["Close"].iloc[-1]
        self.cibc_yearly_stock_return=round(((self.cibc_close_price-self.cibc_open_price+self.cibc_total_dividend)/self.cibc_open_price)*100,4)
        
        self.td_total_dividend=sum(self.df_td_total["Dividends"]) ; self.td_open_price=self.df_td_total["Open"].iloc[0] ; self.td_close_price=self.df_td_total["Close"].iloc[-1]
        self.td_yearly_stock_return=round(((self.td_close_price-self.td_open_price+self.td_total_dividend)/self.td_open_price)*100,4)

    def df_all_daily_return(self):
        self.df_all_returns=pd.DataFrame(
            data={
            "Date":self.df_bmo_total["Date"],
            "BMO":self.df_bmo_total["Daily Returns"],
            "Scotiabank":self.df_scotia_total["Daily Returns"],
            "National Bank of Canada":self.df_naboc_total["Daily Returns"],
            "RBC":self.df_rbc_total["Daily Returns"],
            "TD":self.df_td_total["Daily Returns"],
            "CIBC":self.df_cibc_total["Daily Returns"]
        })

        return self.df_all_returns
    


stockreturn=StockReturn()
stockreturn.data_consolidation()
stockreturn.daily_stock_return()
stockreturn.yearly_stock_return()
stockreturn.df_all_daily_return()



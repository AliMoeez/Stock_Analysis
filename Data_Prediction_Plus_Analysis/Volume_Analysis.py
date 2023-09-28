#Idea is to check the volume changes in the stock in the one year time period to see if their is a trend
#between the firms. That is does the volume change in conjuction for these firms or is this process entirely indepedent of one another.
#Then this will be related to stock prices. For example do higher volume changes imply bigger price increases? Or do lower volume changes
#imply lower prices ?

import pandas as pd

#import stock_return file to get the daily stock returns from the StockReturn class
from Stock_Return import StockReturn

class VolumeAnalysis(StockReturn):
    def __init__(self):
        #lode the relevant functions from the StockReturn class
        super().__init__() ; super().data_consolidation() ; super().daily_stock_return()

    def daily_volume_change(self):
        #add a new column into each dataframes that calcualtes the daily volume change
        self.df_bmo_total["Volume Change"]=self.df_bmo_total["Volume"].pct_change().dropna()
        self.df_scotia_total["Volume Change"]=self.df_scotia_total["Volume"].pct_change().dropna()
        self.df_naboc_total["Volume Change"]=self.df_naboc_total["Volume"].pct_change().dropna()
        self.df_rbc_total["Volume Change"]=self.df_rbc_total["Volume"].pct_change().dropna()
        self.df_cibc_total["Volume Change"]=self.df_cibc_total["Volume"].pct_change().dropna()
        self.df_td_total["Volume Change"]=self.df_td_total["Volume"].pct_change().dropna()

    def corrleation_volume_change(self):
        #find the correlation of all the df Volume Change columns to seee if volume of these stocks move indepednely or depednelty of each other
        #first need to combine all of the volume change values into a df and then find their correlation by using a correlation matrix
      #  pd.set_option('display.max_columns',None)
        self.df_volume_change={"BMO":self.df_bmo_total["Volume Change"], "Scotiabank": self.df_scotia_total["Volume Change"],
                               "National Bank": self.df_naboc_total["Volume Change"], "RBC": self.df_rbc_total["Volume Change"],
                               "CIBC": self.df_cibc_total["Volume Change"],"TD": self.df_td_total["Volume Change"]}
        self.df_volume_change=pd.DataFrame(self.df_volume_change)
        self.df_volume_correlation=self.df_volume_change.corr()

    def correlation_with_stock_price(self):
        #find the correlation of each stock return with its change in its volume change to see if stock pricee changes 
        #correlate with changes in volume changes
        self.df_bmo_volume_stock_change={"Daily Returns":self.df_bmo_total["Daily Returns"],"Volume Change":self.df_bmo_total["Volume Change"]} ; self.df_scotiabank_volume_stock_change={"Daily Returns":self.df_scotia_total["Daily Returns"],"Volume Change":self.df_scotia_total["Volume Change"]}
        self.df_naboc_volume_stock_change={"Daily Returns":self.df_naboc_total["Daily Returns"],"Volume Change":self.df_naboc_total["Volume Change"]} ; self.df_rbc_volume_stock_change={"Daily Returns":self.df_rbc_total["Daily Returns"],"Volume Change":self.df_rbc_total["Volume Change"]}
        self.df_cibc_volume_stock_change={"Daily Returns":self.df_cibc_total["Daily Returns"],"Volume Change":self.df_cibc_total["Volume Change"]} ; self.df_td_volume_stock_change={"Daily Returns":self.df_td_total["Daily Returns"],"Volume Change":self.df_td_total["Volume Change"]}

        self.df_bmo_volume_stock_change=pd.DataFrame(self.df_bmo_volume_stock_change) ; self.df_scotiabank_volume_stock_change=pd.DataFrame(self.df_scotiabank_volume_stock_change)
        self.df_naboc_volume_stock_change=pd.DataFrame(self.df_naboc_volume_stock_change) ; self.df_rbc_volume_stock_change=pd.DataFrame(self.df_rbc_volume_stock_change)
        self.df_cibc_volume_stock_change=pd.DataFrame(self.df_cibc_volume_stock_change) ; self.df_td_volume_stock_change=pd.DataFrame(self.df_td_volume_stock_change)

        self.df_bmo_volume_stock_change_correlation=self.df_bmo_volume_stock_change.corr() ; self.df_scotiabank_volume_stock_change_correlation=self.df_scotiabank_volume_stock_change.corr()
        self.df_naboc_volume_stock_change_correlation=self.df_naboc_volume_stock_change.corr() ; self.df_rbc_volume_stock_change_correlation=self.df_rbc_volume_stock_change.corr()
        self.df_cibc_volume_stock_change_correlation=self.df_cibc_volume_stock_change.corr() ; self.df_td_volume_stock_change_correlation=self.df_td_volume_stock_change.corr()
        #found that their is little correlation between volume change and stock returns. In general it apppears that
        #There is a very slight negative correlation between volume change and stock return. That is as volume change goes up
        #the return goes down or vice versa. But again this correlation is small.

        print(self.df_bmo_volume_stock_change_correlation)
        print(self.df_scotiabank_volume_stock_change_correlation)
        print(self.df_naboc_volume_stock_change_correlation)
        print(self.df_rbc_volume_stock_change_correlation)
        print(self.df_cibc_volume_stock_change_correlation)
        print(self.df_td_volume_stock_change_correlation)


volumeanalysis=VolumeAnalysis()
volumeanalysis.daily_volume_change()
volumeanalysis.corrleation_volume_change()
volumeanalysis.correlation_with_stock_price()
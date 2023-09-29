#This class will find predictions for each stock using its open prices. A SARIMA model will
#be used in this analysis that accounts for seasonality.

import pandas as pd
from statsmodels.tsa.arima.model import ARIMA
from statsmodels.graphics.tsaplots import plot_predict
from statsmodels.graphics.tsaplots import plot_acf,plot_pacf
from statsmodels.tsa.stattools import adfuller
from sklearn.metrics import mean_squared_error,mean_absolute_error,mean_absolute_percentage_error
import matplotlib.pyplot as plt

from Stock_Return import StockReturn

class Prediction(StockReturn):
    def __init__(self):
        super().__init__() ; super().data_consolidation() ; super().daily_stock_return()

    def plot_for_trend_and_seasonlity(self):
        #Plot the data using date on the x aics and the open price on the y axis to check for trend and seasonality
        fig,ax=plt.subplots(2,3)
        ax[0,0].plot(self.df_bmo_total["Date"],self.df_bmo_total["Open"]) ; ax[0,1].plot(self.df_scotia_total["Date"],self.df_scotia_total["Open"])
        ax[0,2].plot(self.df_naboc_total["Date"],self.df_naboc_total["Open"]) ; ax[1,0].plot(self.df_rbc_total["Date"],self.df_rbc_total["Open"])
        ax[1,1].plot(self.df_td_total["Date"],self.df_td_total["Open"]) ; ax[1,2].plot(self.df_cibc_total["Date"],self.df_cibc_total["Open"])
        #See that all but the national bank have a downward trend (though national bank seems to be trending downward in the latter portions of the data). Differencing will be used to eliminate the trend
        #It should be noted that around November-April these stocks experience their peak and drop off significantly
        #afterwards (other than National Bank) indicating seasonality for the stocks. This is seen can be related to findings
        #in https://ca.style.yahoo.com/stock-market-seasonality-trends-hint-164522716.html#:~:text=From%20October%20through%20May%2C%20an,lack%20of%20clear%20trend%20direction.
        #which state rallies occur from October-May and a volatility of prices afterwards

    def plot_acf_adfuller_function(self,column:str):
        #This function will plot acf's and produce adfuller's given some column input
        self.adfuller_list=[]
        self.df_list=[self.df_bmo_total[column],self.df_scotia_total[column],self.df_naboc_total[column],self.df_rbc_total[column],self.df_td_total[column],self.df_cibc_total[column]]
        self.df_list_name=["BMO","Scotiabank","National Bank Of Canada","RBC","TD","CIBC"]
        fig,ax=plt.subplots(2,3)
        plot_acf(self.df_bmo_total[column],ax=ax[0,0]) ; plot_acf(self.df_scotia_total[column],ax=ax[0,1]) ; plot_acf(self.df_naboc_total[column],ax=ax[0,2])
        plot_acf(self.df_rbc_total[column],ax=ax[1,0]) ; plot_acf(self.df_td_total[column],ax=ax[1,1]) ; plot_acf(self.df_cibc_total[column],ax=ax[1,2])
        for idx,df in enumerate(self.df_list): self.adfuller_list.append( (self.df_list_name[idx],round(adfuller(df)[1],4)))

    def plot_acf_adfuller(self):
        #Now going to plot the ACF,PACF and get the Adfuller p-value to figure out if their is autocorrelation in the data. 
        #If we find autocorrelation we will difference to remove it 
        Prediction.plot_acf_adfuller_function(self,"Open")
        #Can see that in the acf that autocorrelation is present as lags do not drop off and instead drop off very slowly. 
        #This is further accounted for by a high p-values for the Adfuller test (>0.05) indicating that autocorrelation is present
        #The same result would be noted in the pacf

    def differencing_data(self):
        #The data will be differenced in order to remove any trends that are in the data sets. A differencing factor of one will be used
        self.df_bmo_total["Differenced Open"]=self.df_bmo_total["Open"].diff() ; self.df_scotia_total["Differenced Open"]=self.df_scotia_total["Open"].diff()
        self.df_naboc_total["Differenced Open"]=self.df_naboc_total["Open"].diff() ; self.df_rbc_total["Differenced Open"]=self.df_rbc_total["Open"].diff()
        self.df_td_total["Differenced Open"]=self.df_td_total["Open"].diff() ; self.df_cibc_total["Differenced Open"]=self.df_cibc_total["Open"].diff()
        
        fig,ax=plt.subplots(2,3)
        ax[0,0].plot(self.df_bmo_total["Date"],self.df_bmo_total["Differenced Open"]) ; ax[0,1].plot(self.df_scotia_total["Date"],self.df_scotia_total["Differenced Open"])
        ax[0,2].plot(self.df_naboc_total["Date"],self.df_naboc_total["Differenced Open"]) ; ax[1,0].plot(self.df_rbc_total["Date"],self.df_rbc_total["Differenced Open"])
        ax[1,1].plot(self.df_td_total["Date"],self.df_td_total["Differenced Open"]) ; ax[1,2].plot(self.df_cibc_total["Date"],self.df_cibc_total["Differenced Open"])

        self.df_bmo_total["Differenced Open"]=self.df_bmo_total["Differenced Open"].fillna(0) ; self.df_scotia_total["Differenced Open"]=self.df_scotia_total["Differenced Open"].fillna(0)
        self.df_naboc_total["Differenced Open"]=self.df_naboc_total["Differenced Open"].fillna(0) ; self.df_rbc_total["Differenced Open"]=self.df_rbc_total["Differenced Open"].fillna(0)
        self.df_td_total["Differenced Open"]=self.df_td_total["Differenced Open"].fillna(0) ; self.df_cibc_total["Differenced Open"]=self.df_cibc_total["Differenced Open"].fillna(0)
        #As we can see differencing does indeed remove the trend

    def new_plot_acf_adfuller(self):
        #Check to see if differncing improved the results of the ACF and the adfullter p-values
        Prediction.plot_acf_adfuller_function(self,"Differenced Open")
        plt.show()
        #See that now the ACF drops off after the first lag indicating low autocorrrelation and all p-values are <0.05 or (0.0) indicating that
        #Autocorrelation has been removed by differcing. The same results will come from a PACF

    


prediction=Prediction()
prediction.plot_for_trend_and_seasonlity()
prediction.plot_acf_adfuller()
prediction.differencing_data()
prediction.new_plot_acf_adfuller()

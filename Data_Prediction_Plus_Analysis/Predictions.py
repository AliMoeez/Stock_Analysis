#This class will find predictions for each stock using its open prices. A SARIMA model will
#be used in this analysis that accounts for seasonality.

import pandas as pd
from statsmodels.tsa.statespace.sarimax import SARIMAX
from statsmodels.graphics.tsaplots import plot_predict
from statsmodels.graphics.tsaplots import plot_acf,plot_pacf
from statsmodels.tsa.stattools import adfuller
from sklearn.metrics import mean_squared_error,mean_absolute_error,mean_absolute_percentage_error
import matplotlib.pyplot as plt
from pmdarima import auto_arima

from .Stock_Return import StockReturn

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

        fig,ax=plt.subplots(2,3)
        plot_pacf(self.df_bmo_total[column],ax=ax[0,0]) ; plot_pacf(self.df_scotia_total[column],ax=ax[0,1]) ; plot_pacf(self.df_naboc_total[column],ax=ax[0,2])
        plot_pacf(self.df_rbc_total[column],ax=ax[1,0]) ; plot_pacf(self.df_td_total[column],ax=ax[1,1]) ; plot_pacf(self.df_cibc_total[column],ax=ax[1,2])

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
      #  plt.show()
        #See that now the ACF drops off after the first lag indicating low autocorrrelation and all p-values are <0.05 or (0.0) indicating that
        #Autocorrelation has been removed by differcing. The same results will come from a PACF
    
    def SARIMA_model(self):
        #Looking at the original ACF and PACF we see that the ACF for all figures decays slowly in a exponential matter towards zero, and
        #the PACF has a large spike at lag 1 and drops to around 0 for all of the companies. This means we use a ARIMA(p,d,0) model.
        #We will do a SARIMA(0,1,0)(1,0,0)365 since differcing removed our trend and it was noted that a AR term will be used which
        #is seansonal due to the slow decay of the ACF and quick decay of the PACF after lag 1.
        self.df_bmo_sarimax=SARIMAX(self.df_bmo_total["Open"],order=(1,0,0),seasonal_order=(1,0,0,30)).fit() 

        self.df_scotia_sarimax=SARIMAX(self.df_scotia_total["Open"],order=(0,1,0),seasonal_order=(1,0,0,30)).fit()
        self.df_naboc_sarimax=SARIMAX(self.df_naboc_total["Open"],order=(0,1,0),seasonal_order=(1,0,0,30)).fit() ; self.df_rbc_sarimax=SARIMAX(self.df_rbc_total["Open"],order=(0,1,0),seasonal_order=(1,0,0,30)).fit()
        self.df_td_sarimax=SARIMAX(self.df_td_total["Open"],order=(0,1,0),seasonal_order=(1,0,0,30)).fit() ; self.df_cibc_sarimax=SARIMAX(self.df_cibc_total["Open"],order=(0,1,0),seasonal_order=(1,0,0,30)).fit()

        self.df_bmo_sarimax_forecast=self.df_bmo_sarimax.forecast(len(self.df_bmo_total["Open"])) ; self.df_scotia_sarimax_forecast=self.df_scotia_sarimax.forecast(len(self.df_scotia_total["Open"]))
        self.df_naboc_sarimax_forecast=self.df_naboc_sarimax.forecast(len(self.df_naboc_total["Open"])) ; self.df_rbc_sarimax_forecast=self.df_rbc_sarimax.forecast(len(self.df_rbc_total["Open"]))
        self.df_td_sarimax_forecast=self.df_td_sarimax.forecast(len(self.df_td_total["Open"])) ; self.df_cibc_sarimax_forecast=self.df_cibc_sarimax.forecast(len(self.df_cibc_total["Open"]))

    def auto_SARIMA_model(self):
        #Can use auto_arima to create a automatic arima model based on AIC characteristics
        self.df_bmo_auto_sarimax=auto_arima(y=self.df_bmo_total["Open"],m=12) ; self.df_scotia_auto_sarimax=auto_arima(y=self.df_scotia_total["Open"],m=12)
        self.df_naboc_auto_sarimax=auto_arima(y=self.df_naboc_total["Open"],m=12) ; self.df_rbc_auto_sarimax=auto_arima(y=self.df_rbc_total["Open"],m=12)
        self.df_td_auto_sarimax=auto_arima(y=self.df_td_total["Open"],m=12) ; self.df_cibc_auto_sarimax=auto_arima(y=self.df_cibc_total["Open"],m=12)
        
        self.df_bmo_auto_sarimax_forecast=self.df_bmo_auto_sarimax.predict(n_periods=len(self.df_bmo_total["Open"])) ; self.df_scotia_auto_sarimax_forecast=self.df_scotia_auto_sarimax.predict(n_periods=len(self.df_scotia_total["Open"]))
        self.df_naboc_auto_sarimax_forecast=self.df_naboc_auto_sarimax.predict(n_periods=len(self.df_naboc_total["Open"])) ; self.df_rbc_auto_sarimax_forecast=self.df_rbc_auto_sarimax.predict(n_periods=len(self.df_rbc_total["Open"]))
        self.df_td_auto_sarimax_forecast=self.df_td_auto_sarimax.predict(n_periods=len(self.df_td_total["Open"])) ; self.df_cibc_auto_sarimax_forecast=self.df_cibc_auto_sarimax.predict(n_periods=len(self.df_cibc_total["Open"]))

    def SARIMA_model_mse_mae_mape(self):
        #Calculate The MSE,MAE,MAPE for all the firms for the SARIMA model so we can compare it to the MSE,MAE,MAPE of the Auto SARIMA model where lower values of MSE,MAE,MAPE are indicative of a better model
        self.df_bmo_sarimax_mse=mean_squared_error(self.df_bmo_total["Open"],self.df_bmo_sarimax_forecast)  ; self.df_bmo_sarimax_mae=mean_absolute_error(self.df_bmo_total["Open"],self.df_bmo_sarimax_forecast) ; self.df_bmo_sarimax_mape=mean_absolute_percentage_error(self.df_bmo_total["Open"],self.df_bmo_sarimax_forecast)
        self.df_scotia_sarimax_mse=mean_squared_error(self.df_scotia_total["Open"],self.df_scotia_sarimax_forecast) ; self.df_scotia_sarimax_mae=mean_absolute_error(self.df_scotia_total["Open"],self.df_scotia_sarimax_forecast) ; self.df_scotia_sarimax_mape=mean_absolute_percentage_error(self.df_scotia_total["Open"],self.df_scotia_sarimax_forecast)
        self.df_naboc_sarimax_mse=mean_squared_error(self.df_naboc_total["Open"],self.df_naboc_sarimax_forecast) ; self.df_naboc_sarimax_mae=mean_absolute_error(self.df_naboc_total["Open"],self.df_naboc_sarimax_forecast) ; self.df_naboc_sarimax_mape=mean_absolute_percentage_error(self.df_naboc_total["Open"],self.df_naboc_sarimax_forecast)
        self.df_rbc_sarimax_mse=mean_squared_error(self.df_rbc_total["Open"],self.df_rbc_sarimax_forecast) ; self.df_rbc_sarimax_mae=mean_absolute_error(self.df_rbc_total["Open"],self.df_rbc_sarimax_forecast) ; self.df_rbc_sarimax_mape=mean_absolute_percentage_error(self.df_rbc_total["Open"],self.df_rbc_sarimax_forecast)
        self.df_td_sarimax_mse=mean_squared_error(self.df_td_total["Open"],self.df_td_sarimax_forecast) ; self.df_td_sarimax_mae=mean_absolute_error(self.df_td_total["Open"],self.df_td_sarimax_forecast) ; self.df_td_sarimax_mape=mean_absolute_percentage_error(self.df_td_total["Open"],self.df_td_sarimax_forecast)
        self.df_cibc_sarimax_mse=mean_squared_error(self.df_cibc_total["Open"],self.df_cibc_sarimax_forecast) ; self.df_cibc_sarimax_mae=mean_absolute_error(self.df_cibc_total["Open"],self.df_cibc_sarimax_forecast) ; self.df_cibc_sarimax_mape=mean_absolute_percentage_error(self.df_cibc_total["Open"],self.df_cibc_sarimax_forecast)

        self.df_bmo_sarima_mse_mae_mape_list=["BMO","SARIMA",self.df_bmo_sarimax_mse,self.df_bmo_sarimax_mae,self.df_bmo_sarimax_mape]
        self.df_scotia_sarima_mse_mae_mape_list=["Scotiabank","SARIMA",self.df_scotia_sarimax_mse,self.df_scotia_sarimax_mae,self.df_scotia_sarimax_mape]
        self.df_naboc_sarima_mse_mae_mape_list=["National Bank","SARIMA",self.df_naboc_sarimax_mse,self.df_naboc_sarimax_mae,self.df_naboc_sarimax_mape]
        self.df_rbc_sarima_mse_mae_mape_list=["RBC","SARIMA",self.df_rbc_sarimax_mse,self.df_rbc_sarimax_mae,self.df_rbc_sarimax_mape]
        self.df_td_sarima_mse_mae_mape_list=["TD","SARIMA",self.df_td_sarimax_mse,self.df_td_sarimax_mae,self.df_td_sarimax_mape]
        self.df_cibc_sarima_mse_mae_mape_list=["CIBC","SARIMA",self.df_cibc_sarimax_mse,self.df_cibc_sarimax_mae,self.df_cibc_sarimax_mape]

        self.df_SARIMA_mse_mae_mape_list=[self.df_bmo_sarima_mse_mae_mape_list,self.df_scotia_sarima_mse_mae_mape_list,self.df_naboc_sarima_mse_mae_mape_list, self.df_rbc_sarima_mse_mae_mape_list, self.df_td_sarima_mse_mae_mape_list,self.df_cibc_sarima_mse_mae_mape_list]

    def auto_SARIMA_model_mse_mae_mape(self):
        self.df_bmo_auto_sarimax_mse=mean_squared_error(self.df_bmo_total["Open"],self.df_bmo_auto_sarimax_forecast) ; self.df_bmo_auto_sarimax_mae=mean_absolute_error(self.df_bmo_total["Open"],self.df_bmo_auto_sarimax_forecast) ; self.df_bmo_auto_sarimax_mape=mean_absolute_percentage_error(self.df_bmo_total["Open"],self.df_bmo_auto_sarimax_forecast)
        self.df_naboc_auto_sarimax_mse=mean_squared_error(self.df_naboc_total["Open"],self.df_naboc_auto_sarimax_forecast) ; self.df_naboc_auto_sarimax_mae=mean_absolute_error(self.df_naboc_total["Open"],self.df_naboc_auto_sarimax_forecast) ; self.df_naboc_auto_sarimax_mape=mean_absolute_percentage_error(self.df_naboc_total["Open"],self.df_naboc_auto_sarimax_forecast)
        self.df_scotia_auto_sarimax_mse=mean_squared_error(self.df_scotia_total["Open"],self.df_scotia_auto_sarimax_forecast) ; self.df_scotia_auto_sarimax_mae=mean_absolute_error(self.df_scotia_total["Open"],self.df_scotia_auto_sarimax_forecast) ; self.df_scotia_auto_sarimax_mape=mean_absolute_percentage_error(self.df_scotia_total["Open"],self.df_scotia_auto_sarimax_forecast)
        self.df_rbc_auto_sarimax_mse=mean_squared_error(self.df_rbc_total["Open"],self.df_rbc_auto_sarimax_forecast) ; self.df_rbc_auto_sarimax_mae=mean_absolute_error(self.df_rbc_total["Open"],self.df_rbc_auto_sarimax_forecast) ; self.df_rbc_auto_sarimax_mape=mean_absolute_percentage_error(self.df_rbc_total["Open"],self.df_rbc_auto_sarimax_forecast)
        self.df_td_auto_sarimax_mse=mean_squared_error(self.df_td_total["Open"],self.df_td_auto_sarimax_forecast) ; self.df_td_auto_sarimax_mae=mean_absolute_error(self.df_td_total["Open"],self.df_td_auto_sarimax_forecast) ; self.df_td_auto_sarimax_mape=mean_absolute_percentage_error(self.df_td_total["Open"],self.df_td_auto_sarimax_forecast)
        self.df_cibc_auto_sarimax_mse=mean_squared_error(self.df_cibc_total["Open"],self.df_cibc_auto_sarimax_forecast) ; self.df_cibc_auto_sarimax_mae=mean_absolute_error(self.df_cibc_total["Open"],self.df_cibc_auto_sarimax_forecast) ; self.df_cibc_auto_sarimax_mape=mean_absolute_percentage_error(self.df_cibc_total["Open"],self.df_cibc_auto_sarimax_forecast)

        self.df_bmo_auto_arima_mse_mae_mape_list=["BMO","Auto SARIMA",self.df_bmo_auto_sarimax_mse,self.df_bmo_auto_sarimax_mae,self.df_bmo_auto_sarimax_mape]
        self.df_naboc_auto_arima_mse_mae_mape_list=["National Bank","Auto SARIMA",self.df_naboc_auto_sarimax_mse,self.df_naboc_auto_sarimax_mae,self.df_naboc_auto_sarimax_mape]
        self.df_scotia_auto_arima_mse_mae_mape_list=["Scotiabank","Auto SARIMA",self.df_scotia_auto_sarimax_mse,self.df_scotia_auto_sarimax_mae,self.df_scotia_auto_sarimax_mape]
        self.df_rbc_auto_arima_mse_mae_mape_list=["RBC","Auto SARIMA",self.df_rbc_auto_sarimax_mse,self.df_rbc_auto_sarimax_mae,self.df_rbc_auto_sarimax_mape]
        self.df_td_auto_arima_mse_mae_mape_list=["TD","Auto SARIMA",self.df_td_auto_sarimax_mse,self.df_td_auto_sarimax_mae,self.df_td_auto_sarimax_mape]
        self.df_cibc_auto_arima_mse_mae_mape_list=["CIBC","Auto SARIMA",self.df_cibc_auto_sarimax_mse,self.df_cibc_auto_sarimax_mae,self.df_cibc_auto_sarimax_mape]

        self.df_auto_arima_mse_mae_mape_list=[self.df_bmo_auto_arima_mse_mae_mape_list,self.df_naboc_auto_arima_mse_mae_mape_list,self.df_scotia_auto_arima_mse_mae_mape_list,self.df_rbc_auto_arima_mse_mae_mape_list,self.df_td_auto_arima_mse_mae_mape_list,self.df_cibc_auto_arima_mse_mae_mape_list]

    def display_company_mse_mae_mape(self,company:str):
        #This function will compare the results of the MAE,MSE and MAPE given some company input. Lower values are deemed to be better for MAE,MSE and MAPE
        for i in self.df_SARIMA_mse_mae_mape_list:
            for j in self.df_auto_arima_mse_mae_mape_list:
                if company==i[0] and company==j[0]:
                    print(i,j)
        #When these values are compared we see that all but RBC has better results in my model with respect to MAE,MSE and MAPE (atleast 2 of the 3 metrics is
        #less in the SARIMA model choosen by me).In the dashbaord the SARIMA and its forecast made by me will be used.

    def plot_residuals(self):
        #First we will get the SARIMA residuals and check if they are normally distributed before procdeeding to plotting the forecasts
        self.df_bmo_sarima_residuals=self.df_bmo_sarimax.resid[1:] ; self.df_naboc_sarima_residuals=self.df_naboc_sarimax.resid[1:] 
        self.df_scotia_sarima_residuals=self.df_scotia_sarimax.resid[1:] ; self.df_rbc_sarima_residuals=self.df_rbc_sarimax.resid[1:]
        self.df_td_sarima_residuals=self.df_td_sarimax.resid[1:] ; self.df_cibc_sarima_residuals=self.df_cibc_sarimax.resid[1:]

        fig,ax=plt.subplots(2,3)
        self.df_bmo_sarima_residuals.plot(kind='kde',ax=ax[0,0]) ; self.df_naboc_sarima_residuals.plot(kind='kde',ax=ax[0,1])
        self.df_scotia_sarima_residuals.plot(kind='kde',ax=ax[0,2]) ; self.df_rbc_sarima_residuals.plot(kind='kde',ax=ax[1,0])
        self.df_td_sarima_residuals.plot(kind='kde',ax=ax[1,1]) ; self.df_cibc_sarima_residuals.plot(kind='kde',ax=ax[1,2])
        #We see that all of the residuals are normally distriuted meaning we can proceed with plotting the forecast
    
    def plot_forecast(self):
        #In this function we will plot the predictions of the companies with their 95% confidecne internvals
        fig,ax=plt.subplots(2,3)
        
        self.df_bmo_total["Open"].plot(ax=ax[0,0])
        plot_predict(self.df_bmo_sarimax,200,275,ax=ax[0,0])

        self.df_scotia_total["Open"].plot(ax=ax[0,1])
        plot_predict(self.df_scotia_sarimax,200,275,ax=ax[0,1])
        
        self.df_naboc_total["Open"].plot(ax=ax[0,2])
        plot_predict(self.df_naboc_sarimax,200,275,ax=ax[0,2])
       
        self.df_rbc_total["Open"].plot(ax=ax[1,0])
        plot_predict(self.df_rbc_sarimax,200,275,ax=ax[1,0])
        
        self.df_td_total["Open"].plot(ax=ax[1,1])
        plot_predict(self.df_td_sarimax,200,275,ax=ax[1,1])

        self.df_cibc_total["Open"].plot(ax=ax[1,2])
        plot_predict(self.df_cibc_sarimax,200,275,ax=ax[1,2])
        
        plt.show()

       
                    
#prediction=Prediction()
#prediction.plot_for_trend_and_seasonlity()
#prediction.plot_acf_adfuller()
#prediction.differencing_data()
#prediction.new_plot_acf_adfuller()
#prediction.SARIMA_model()
#prediction.auto_SARIMA_model()
#prediction.SARIMA_model_mse_mae_mape()
#prediction.auto_SARIMA_model_mse_mae_mape()
#prediction.display_company_mse_mae_mape("RBC")
#prediction.plot_residuals()
#prediction.plot_forecast()

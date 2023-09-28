#This class will find predictions for each stock using its open prices. A SARIMA model will
#be used in this analysis that accounts for seasonality.

import pandas as pd
from statsmodels.tsa.arima.model import ARIMA
from statsmodels.graphics.tsaplots import plot_predict
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
        plt.show()
        """See that all but the national bank have a downward trend (though national bank seems to be trending downward in the latter portions of the data). Differencing will be used to eliminate the trend
         It should be noted that around November-April these stocks experience their peak and drop off significantly
         afterwards (other than National Bank) indicating seasonality for the stocks. This is seen can be related to findings
         in https://ca.style.yahoo.com/stock-market-seasonality-trends-hint-164522716.html#:~:text=From%20October%20through%20May%2C%20an,lack%20of%20clear%20trend%20direction.
         which state rallies occur from October-May and a volatility of prices afterwards"""

    
prediction=Prediction()
prediction.plot_for_trend_and_seasonlity()

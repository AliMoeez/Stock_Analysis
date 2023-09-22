import pandas as pd
pd.options.mode.chained_assignment=None

#best time to invest in this case, is the time where all the stock prices are generally at their lowest,
#followed by a time of a increase where one can make profits off going long.
#analysis will be done on the daily open price of the stock

#lode csv files using pyarrow engine to make the csv files load faster


class BestTimeInv:
    def __init__(self):
        self.df_rbc=pd.read_csv(r"Data\Data_Sets\RBC_TO.csv", engine="pyarrow")
        self.df_scotia=pd.read_csv(r"Data\Data_Sets\BNS.TO.csv",engine="pyarrow")
        self.df_cibc=pd.read_csv(r"Data\Data_Sets\CIBC.TO.csv",engine="pyarrow")
        self.df_naboc=pd.read_csv(r"Data\Data_Sets\NABOC.TO.csv",engine="pyarrow")
        self.df_td=pd.read_csv(r"Data\Data_Sets\TD.TO.csv",engine="pyarrow")

    def dataframe_cosolidation(self):
        self.df_rbc_date_open=self.df_rbc[["Date","Open"]]
        self.df_scotia_date_open=self.df_scotia[["Open"]]
        self.df_cibc_date_open=self.df_cibc[["Open"]]
        self.df_naboc_date_open=self.df_naboc[["Open"]]
        self.df_td_date_open=self.df_td[["Open"]]
        self.df_total=[self.df_rbc_date_open,self.df_scotia_date_open,self.df_cibc_date_open,self.df_naboc_date_open,self.df_td_date_open]
        self.df_titles=["RBC","SCOTIABANK","CIBC","NATIONAL BANK","TD"]

    def rename_columns(self):
        for i,col in enumerate(self.df_total):
            self.df_total[i].rename(columns={"Open":f"{self.df_titles[i]}_Open"},inplace=True)
        self.df_total=pd.concat(self.df_total,axis=1,join="inner")

    def lowest_price_period(self):
        for col in self.df_total:
            print(col)
        print(self.df_total.nsmallest(10,"RBC_Open"))

    

bestinvtime=BestTimeInv()
bestinvtime.dataframe_cosolidation()
bestinvtime.rename_columns()
bestinvtime.lowest_price_period()









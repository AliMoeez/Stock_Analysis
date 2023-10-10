import tensorflow as tf

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

class NeuralNetowrkAnalysis:
    def __init__(self):
        #Lode stock csv files using pyarrow for faster loading times
        self.df_bmo=pd.read_csv(r"Data\Stock Prices\BMO.TO.csv", engine="pyarrow")  ; self.df_rbc=pd.read_csv(r"Data\Stock Prices\RBC_TO.csv", engine="pyarrow") 
        self.df_scotia=pd.read_csv(r"Data\Stock Prices\BNS.TO.csv",engine="pyarrow") ; self.df_cibc=pd.read_csv(r"Data\Stock Prices\CIBC.TO.csv",engine="pyarrow") 
        self.df_naboc=pd.read_csv(r"Data\Stock Prices\NABOC.TO.csv",engine="pyarrow")  ; self.df_td=pd.read_csv(r"Data\Stock Prices\TD.TO.csv",engine="pyarrow")
        #Lode dividened csv files using pyarrow for faster loading times
        self.df_bmo_div=pd.read_csv(r"Data\Dividends\BMO.TO (1).csv", engine="pyarrow")  ; self.df_rbc_div=pd.read_csv(r"Data\Dividends\RY.TO.csv", engine="pyarrow") 
        self.df_scotia_div=pd.read_csv(r"Data\Dividends\BNS.TO (1).csv",engine="pyarrow") ; self.df_cibc_div=pd.read_csv(r"Data\Dividends\CIBC.TO (1).csv",engine="pyarrow") 
        self.df_naboc_div=pd.read_csv(r"Data\Dividends\NABOC.TO (1).csv",engine="pyarrow") ; self.df_td_div=pd.read_csv(r"Data\Dividends\TD.TO (1).csv",engine="pyarrow")





neuralnetworkanalysis=NeuralNetowrkAnalysis()
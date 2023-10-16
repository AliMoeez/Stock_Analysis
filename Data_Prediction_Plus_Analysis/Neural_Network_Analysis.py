import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import *
from tensorflow.keras.losses import MeanSquaredError
from tensorflow.keras.metrics import RootMeanSquaredError
from tensorflow.keras.optimizers import Adam

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler


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

    def add_timeline(self):
        
        self.x=0
        self.time_list=[]
        for i in range(len(self.df_bmo["Date"])):
            self.x+=1
            self.time_list.append(self.x)
        
        self.df_bmo["Time"]=self.time_list


    def data_conslidation(self):

        tf.random.set_seed(42)

        self.scaler=MinMaxScaler(feature_range=(0,1))

        self.df_bmo[["Time","Open"]]=self.scaler.fit_transform(self.df_bmo[["Time","Open"]])

        self.x_train,self.x_test,self.y_train,self.y_test=train_test_split(
        
        self.df_bmo["Time"],
        self.df_bmo["Open"],
        test_size=0.45,
        random_state=42
        
        )

    def model(self):
        self.model=Sequential()
        self.model.add(InputLayer((1,1)))
        self.model.add(LSTM(64))
        self.model.add(Dense(32,"relu"))
        self.model.add(Dense(16,"relu"))
    #    self.model.add(Dense(8,"relu"))
        self.model.add(Dense(1,"linear"))

    def model_compile(self):
        self.model.compile(loss='mse',optimizer=Adam(learning_rate=0.001))
        self.model.fit(x=self.x_train,y=self.y_train, validation_data=(self.x_test,self.y_test),
                       epochs=25,shuffle=True,batch_size=5,verbose=1)
        
    def model_predict(self):
        self.df_bmo[["Time","Open"]]=self.scaler.inverse_transform(self.df_bmo[["Time","Open"]])

        self.model_predict=self.model.predict(self.df_bmo["Open"])

        
        print(self.model_predict.shape)
        print(self.df_bmo[["Time","Open"]].shape)

        self.model_predict=self.scaler.inverse_transform(self.model_predict)
        self.x_train=self.scaler.inverse_transform([self.x_train])
        self.y_train=self.scaler.inverse_transform([self.y_train])


        self.model_predict=self.model_predict[::-1]




    def model_plot(self):
        fig,axes=plt.subplots(1,2)
        axes[0].plot(self.df_bmo["Time"],self.df_bmo["Open"],label="Original Data")
        axes[0].plot(self.df_bmo["Time"],self.model_predict,label="Predict Regular")
    #    axes[0].plot(self.df_bmo["Time"],self.model_predict_1,label="Predict Other")
        axes[0].legend()
        plt.show()


neuralnetworkanalysis=NeuralNetowrkAnalysis()
neuralnetworkanalysis.add_timeline()
neuralnetworkanalysis.data_conslidation()
neuralnetworkanalysis.model()
neuralnetworkanalysis.model_compile()
neuralnetworkanalysis.model_predict()
neuralnetworkanalysis.model_plot()
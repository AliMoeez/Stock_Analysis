import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import *
from tensorflow.keras.losses import MeanSquaredError
from tensorflow.keras.metrics import RootMeanSquaredError
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.layers import Dropout

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

        self.bmo_x_data=[] ; self.bmo_x_1=[]
        self.naboc_x_data=[] ; self.naboc_x_1=[]
        self.td_x_data=[] ; self.td_x_1=[]
        self.cibc_x_data=[] ; self.cibc_x_1=[]
        self.scotia_x_data=[] ; self.scotia_x_1=[]
        self.rbc_x_data=[] ; self.rbc_x_1=[]

        self.past_points_refered=10

    def add_timeline(self):
        
        self.x=0
        self.time_list=[]
        for i in range(len(self.df_bmo["Date"])):
            self.x+=1
            self.time_list.append(self.x)
        self.df_bmo["Time"]=self.time_list
        self.df_naboc["Time"]=self.time_list
        self.df_td["Time"]=self.time_list
        self.df_cibc["Time"]=self.time_list
        self.df_scotia["Time"]=self.time_list
        self.df_rbc["Time"]=self.time_list

    def data_conslidation(self):

        self.scaler=MinMaxScaler(feature_range=(0,1))

        self.df_bmo[["Time","Open"]]=self.scaler.fit_transform(self.df_bmo[["Time","Open"]])
        self.df_naboc[["Time","Open"]]=self.scaler.fit_transform(self.df_naboc[["Time","Open"]])
        self.df_td[["Time","Open"]]=self.scaler.fit_transform(self.df_td[["Time","Open"]])
        self.df_cibc[["Time","Open"]]=self.scaler.fit_transform(self.df_cibc[["Time","Open"]])
        self.df_scotia[["Time","Open"]]=self.scaler.fit_transform(self.df_scotia[["Time","Open"]])
        self.df_rbc[["Time","Open"]]=self.scaler.fit_transform(self.df_rbc[["Time","Open"]])

        self.bmo_x_train=self.df_bmo["Open"][:-170] ; self.bmo_x_test=self.df_bmo["Open"][170:]
        self.naboc_x_train=self.df_naboc["Open"][:-170] ; self.naboc_x_test=self.df_naboc["Open"][170:]
        self.td_x_train=self.df_td["Open"][:-170] ; self.td_x_test=self.df_td["Open"][170:]
        self.cibc_x_train=self.df_cibc["Open"][:-170] ; self.cibc_x_test=self.df_cibc["Open"][170:]
        self.scotia_x_train=self.df_scotia["Open"][:-170] ; self.scotia_x_test=self.df_scotia["Open"][170:]
        self.rbc_x_train=self.df_rbc["Open"][:-170] ; self.rbc_x_test=self.df_rbc["Open"][170:]

    def data_into_array(self):

        for i in range(self.past_points_refered,len(self.bmo_x_train)):
            self.bmo_x_data.append(self.bmo_x_train[i-self.past_points_refered:i]) ; self.bmo_x_1.append(self.bmo_x_train[i])
            self.naboc_x_data.append(self.naboc_x_train[i-self.past_points_refered:i]) ; self.naboc_x_1.append(self.naboc_x_train[i])
            self.td_x_data.append(self.td_x_train[i-self.past_points_refered:i]) ; self.td_x_1.append(self.td_x_train[i])
            self.cibc_x_data.append(self.cibc_x_train[i-self.past_points_refered:i]) ; self.cibc_x_1.append(self.cibc_x_train[i])
            self.scotia_x_data.append(self.scotia_x_train[i-self.past_points_refered:i]) ; self.scotia_x_1.append(self.scotia_x_train[i])
            self.rbc_x_data.append(self.rbc_x_train[i-self.past_points_refered:i]) ; self.rbc_x_1.append(self.rbc_x_train[i])
        
        self.bmo_x_data=np.array(self.bmo_x_data) ; self.bmo_x_1=np.array(self.bmo_x_1)
        self.rbc_x_data=np.array(self.rbc_x_data) ; self.rbc_x_1=np.array(self.rbc_x_1)
        self.naboc_x_data=np.array(self.naboc_x_data) ; self.naboc_x_1=np.array(self.naboc_x_1)
        self.cibc_x_data=np.array(self.cibc_x_data) ; self.cibc_x_1=np.array(self.cibc_x_1)
        self.scotia_x_data=np.array(self.scotia_x_data) ; self.scotia_x_1=np.array(self.scotia_x_1)
        self.td_x_data=np.array(self.td_x_data) ; self.td_x_1=np.array(self.td_x_1)

        self.bmo_x_data=self.bmo_x_data.reshape(self.bmo_x_data.shape[0],self.bmo_x_data.shape[1],1)
        self.rbc_x_data=self.rbc_x_data.reshape(self.rbc_x_data.shape[0],self.rbc_x_data.shape[1],1)
        self.naboc_x_data=self.naboc_x_data.reshape(self.naboc_x_data.shape[0],self.naboc_x_data.shape[1],1)
        self.cibc_x_data=self.cibc_x_data.reshape(self.cibc_x_data.shape[0],self.cibc_x_data.shape[1],1)
        self.scotia_x_data=self.scotia_x_data.reshape(self.scotia_x_data.shape[0],self.scotia_x_data.shape[1],1)
        self.td_x_data=self.td_x_data.reshape(self.td_x_data.shape[0],self.td_x_data.shape[1],1)

        tf.random.set_seed(42)

    def model(self):
        self.model=Sequential()
        self.model.add(LSTM(units=64, input_shape=(self.bmo_x_data.shape[1],1),return_sequences=True))
        self.model.add(LSTM(units=32))
        self.model.add(Dense(16,"relu"))
        self.model.add(Dense(1,"linear"))

    def model_compile(self):
        
        self.model.compile(loss='mse',optimizer=Adam(learning_rate=0.01))
        
        self.model.fit(x=self.bmo_x_data,y=self.bmo_x_1,
                        epochs=10,shuffle=True,batch_size=1,verbose=1)

        
    def model_predict(self):
        self.model_predict=self.model.predict(self.df_bmo["Open"])

   
        self.model_predict=pd.DataFrame(
            data={
                "Time":self.df_bmo["Time"],
                "Output":self.model_predict.flatten()

            }
        )

    def model_plot(self):
        fig,axes=plt.subplots(1,2)
        self.df_bmo[["Time","Open"]]=self.scaler.inverse_transform(self.df_bmo[["Time","Open"]])
        self.model_predict[["Time","Output"]]=self.scaler.inverse_transform(self.model_predict[["Time","Output"]])


        axes[0].plot(self.df_bmo["Time"],self.df_bmo["Open"],label="Original Data")
        axes[0].plot(self.df_bmo["Time"],self.model_predict["Output"],label="Predict Regular")
    #    axes[0].plot(self.df_bmo["Time"],self.model_predict_1,label="Predict Other")
        axes[0].legend()
        plt.show()


neuralnetworkanalysis=NeuralNetowrkAnalysis()
neuralnetworkanalysis.add_timeline()
neuralnetworkanalysis.data_conslidation()
neuralnetworkanalysis.data_into_array()
neuralnetworkanalysis.model()
neuralnetworkanalysis.model_compile()
neuralnetworkanalysis.model_predict()
neuralnetworkanalysis.model_plot()
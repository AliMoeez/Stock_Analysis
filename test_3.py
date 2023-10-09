from Data_Prediction_Plus_Analysis import Prediction


class CI(Prediction):
    def __init__(self):
        super().__init__() ; super().SARIMA_model()


    def values(self):
        self.df_bmo_confidence_interval=self.df_bmo_sarimax.get_forecast(len(self.df_bmo["Open"])).conf_int(alpha=0.05)
        self.df_naboc_confidence_interval=self.df_naboc_sarimax.get_forecast(len(self.df_naboc["Open"])).conf_int(alpha=0.05)
        self.df_rbc_confidence_interval=self.df_rbc_sarimax.get_forecast(len(self.df_rbc["Open"])).conf_int(alpha=0.05)
        self.df_td_confidence_interval=self.df_td_sarimax.get_forecast(len(self.df_td["Open"])).conf_int(alpha=0.05)
        self.df_scotia_confidence_interval=self.df_scotia_sarimax.get_forecast(len(self.df_scotia["Open"])).conf_int(alpha=0.05)
        self.df_cibc_confidence_interval=self.df_cibc_sarimax.get_forecast(len(self.df_cibc["Open"])).conf_int(alpha=0.05)

        print(self.df_bmo_confidence_interval)

        self.df_bmo_ci_lower=self.df_bmo_confidence_interval["lower Open"]
        self.df_naboc_ci_lower=self.df_naboc_confidence_interval["lower Open"]
        self.df_rbc_ci_lower=self.df_rbc_confidence_interval["lower Open"]
        self.df_td_ci_lower=self.df_td_confidence_interval["lower Open"]
        self.df_scotia_ci_lower=self.df_scotia_confidence_interval["lower Open"]
        self.df_cibc_ci_lower=self.df_cibc_confidence_interval["lower Open"]

        self.df_bmo_ci_upper=self.df_bmo_confidence_interval["upper Open"]
        self.df_naboc_ci_upper=self.df_naboc_confidence_interval["upper Open"]
        self.df_rbc_ci_upper=self.df_rbc_confidence_interval["upper Open"]
        self.df_td_ci_upper=self.df_td_confidence_interval["upper Open"]
        self.df_scotia_ci_upper=self.df_scotia_confidence_interval["upper Open"]
        self.df_cibc_ci_upper=self.df_cibc_confidence_interval["upper Open"]


        print(self.df_bmo_ci_lower)
        print(self.df_bmo_ci_upper)

ci=CI()
ci.values()
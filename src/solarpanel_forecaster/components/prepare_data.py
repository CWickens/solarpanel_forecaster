import pandas as pd
from solarpanel_forecaster.entity.config_entity import (
    TrainingDataPreparationConfig)


class PrepareData:
    def __init__(
            self,
            config_training: TrainingDataPreparationConfig):
        self.config_training = config_training

    def load_training_data(self):
        input_data_15minutely = self.config_training.input_data_15minutely
        input_data_hourly = self.config_training.input_data_hourly
        input_solis = self.config_training.input_solis

        df_15minutely = pd.read_pickle(input_data_15minutely)
        df_hourly = pd.read_pickle(input_data_hourly)
        df_solis = pd.read_pickle(input_solis)
        df_solis.index = df_solis.index.tz_localize('UTC')

        return df_15minutely, df_hourly, df_solis

    def load_inference_data(self):
        pass

    def merge_15minutely_and_hourly_data(self, df_15minutely, df_hourly):
        df_merge_metro = pd.merge(
            df_15minutely.resample('min').mean().interpolate(),
            df_hourly.resample('min').mean().interpolate(),
            left_index=True, right_index=True
            )
        return df_merge_metro

    def merge_metro_to_solis_for_training(self, df_metro_hist, df_solis_hist):

        df_merge_final = pd.merge(
            df_metro_hist,
            df_solis_hist['pac'].resample('min').mean().interpolate(),
            left_index=True, right_index=True
            )
        return df_merge_final

    def resample_data(self, df_merge_final):
        resample_time = self.config_training.resample

        df_resample = df_merge_final.resample(resample_time).mean()
        return df_resample

    def make_features(self, df):
        df['month'] = df.index.month
        df['day'] = df.index.day
        df['hour'] = df.index.hour
        return df

import json
from solarpanel_forecaster import logger
import pandas as pd
from solarpanel_forecaster.config.configuration import (
    LiveWeatherDataTransformationConfig)


class LiveWeatherDataTransformation:
    def __init__(
            self,
            config: LiveWeatherDataTransformationConfig):
        self.config = config

    def load(self):
        input_file = self.config.input_file

        with open(input_file, 'r') as f:
            logger.info(f"Loading {input_file}")
            data = json.load(f)
            self.data = data
            logger.info("Loading complete!")
        return data

    def save(self, df, path):
        logger.info(f"Saving to {path}")
        df.to_pickle(path)
        logger.info(("Save successful!"))

    def get_current_weather(self):
        data = self.data

        df = pd.DataFrame(data['0']['current'])
        df['time delay'] = 0
        return df

    def get_historical_weather(self):
        data = self.data

        dic_data = []
        for i in range(1, len(data)):
            temp_data = data[str(-1*i)]['data'][0]
            temp_data.update({'time delay': str(-1*i)})
            dic_data.append(temp_data)
        df = pd.DataFrame(dic_data)
        return df

    def get_actual_weather(self):

        df_current = self.get_current_weather()
        df_history = self.get_historical_weather()
        df = pd.concat([df_current, df_history], axis=0).reset_index(drop=True)
        return df

    def get_hourly_forecast(self):
        data = self.data
        hours_of_forecast = self.config.hours_of_forecast
        df = pd.DataFrame(data['0']['hourly'][0:hours_of_forecast])
        return df

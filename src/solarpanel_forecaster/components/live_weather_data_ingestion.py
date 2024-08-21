import urllib.parse
import requests
import datetime
import json
from solarpanel_forecaster import logger
from solarpanel_forecaster.entity.config_entity import (
    LiveWeatherDataIngestionConfig,
    OpenWeatherMapPrivateConfig)


class LiveWeatherDataIngestion:
    def __init__(
            self,
            config: LiveWeatherDataIngestionConfig,
            config_secret: OpenWeatherMapPrivateConfig):
        self.config = config
        self.config_secret = config_secret

    def get_unix_times_for_all_API_requests(self):
        hours_of_history = self.config.hours_of_history

        timestamp_list = []
        timestamp = datetime.datetime.now()
        for i in range(0, hours_of_history+1):
            timestamp_list.append(timestamp - datetime.timedelta(hours=i))
        return timestamp_list

    def make_url_current(self):
        base_url = self.config.base_url_forecast
        config_secret = self.config_secret

        params = {
            'lat': config_secret.lat,
            'lon': config_secret.lon,
            'apikey': config_secret.apikey
        }

        url = f"{base_url}?{urllib.parse.urlencode(params)}"
        return url

    def make_url_history(self, dt):
        base_url = self.config.base_url
        config_secret = self.config_secret

        params = {
            'lat': config_secret.lat,
            'lon': config_secret.lon,
            'dt': int(dt.timestamp()),
            'apikey': config_secret.apikey
        }

        url = f"{base_url}?{urllib.parse.urlencode(params)}"
        return url

    def download(self):
        local_data_file = self.config.local_data_file

        all_times = self.get_unix_times_for_all_API_requests()
        data = {}
        logger.info('Downloading data from OpenWeatherMap ...')
        for idx, dt in enumerate(all_times):
            if idx == 0:
                url = self.make_url_current()
            else:
                url = self.make_url_history(dt=dt)

            # Send GET request to the API
            response = requests.get(url)
            if response.status_code == 200:
                # Parse the JSON response
                data.update({-1*idx: response.json()})
            else:
                print(f"Error: {response.status_code}")
                print(response.text)  # Might contain additional error details

        with open(local_data_file, 'w') as f:
            json.dump(data, f)
            logger.info(f'Download successful! Saved to {local_data_file}')

        return data

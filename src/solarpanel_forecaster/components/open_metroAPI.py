from solarpanel_forecaster.entity.config_entity import (
    OpenMetroAPIConfig,
    OpenMetroHitoricalConfig,
    OpenMetroForecastConfig
    )

import openmeteo_requests
import requests_cache
import pandas as pd
from retry_requests import retry
from openmeteo_sdk.WeatherApiResponse import WeatherApiResponse
from solarpanel_forecaster import logger


class OpenMetroAPI:
    def __init__(
            self,
            config_API: OpenMetroAPIConfig,
            config_historical: OpenMetroHitoricalConfig,
            config_forecast: OpenMetroForecastConfig):
        self.config_API = config_API
        self.config_historical = config_historical
        self.config_forecast = config_forecast
    logger.info("Instantiating OpenMetroAPI class")

    def get_base_url_params(self):
        latitude = self.config_API.latitude
        longitude = self.config_API.longitude
        features_minutely_15 = self.config_API.features_minutely_15
        features_hourly = self.config_API.features_hourly

        base_url_params = {
            "latitude": latitude,
            "longitude": longitude,
            "minutely_15": features_minutely_15,
            "hourly": features_hourly,
            "timezone": "GMT"
        }
        return base_url_params

    def get_historical_api_client(self, base_url_params):
        start_date = self.config_historical.start_date
        end_date = self.config_historical.end_date

        # Setup the Open-Meteo API client with cache and retry on error
        cache_session = requests_cache.CachedSession('.cache', expire_after=3600)
        retry_session = retry(cache_session, retries=5, backoff_factor=0.2)
        openmeteo = openmeteo_requests.Client(session=retry_session)

        # Make sure all required weather variables are listed here
        # The order of variables in hourly or daily is important to assign them correctly below
        url = "https://historical-forecast-api.open-meteo.com/v1/forecast"
        params = {"start_date": start_date, "end_date": end_date}
        params.update(base_url_params)
        responses = openmeteo.weather_api(url, params=params)

        # Process first location. Add a for-loop for multiple locations or weather models
        response = responses[0]
        logger.info(
            f"Coordinates {response.Latitude()}°N {response.Longitude()}°E"
            )
        logger.info(f"Elevation {response.Elevation()} m asl")
        logger.info(
            f"Timezone {response.Timezone()} {response.TimezoneAbbreviation()}"
            )
        logger.info(
            f"Timezone difference to GMT+0 {response.UtcOffsetSeconds()} s")
        return response

    def get_forecast_api_client(self, base_url_params):
        past_days = self.config_forecast.past_days
        forecast_days = self.config_forecast.forecast_days

        # Setup the Open-Meteo API client with cache and retry on error
        cache_session = requests_cache.CachedSession('.cache', expire_after=3600)
        retry_session = retry(cache_session, retries=5, backoff_factor=0.2)
        openmeteo = openmeteo_requests.Client(session=retry_session)

        # Make sure all required weather variables are listed here
        # The order of variables in hourly or daily is important to assign them correctly below
        url = "https://api.open-meteo.com/v1/forecast"
        params = {
            "past_days": past_days,
            "forecast_days": forecast_days,
        }
        params.update(base_url_params)
        responses = openmeteo.weather_api(url, params=params)

        # Process first location. Add a for-loop for multiple locations or weather models
        response = responses[0]
        return response

    def extract_15_minutely_data(self, api_client: WeatherApiResponse) -> pd.DataFrame:
        features_minutely_15 = self.config_API.features_minutely_15

        # Process minutely_15 data. The order of variables needs to be the same as requested.
        minutely_15 = api_client.Minutely15()
        minutely_15_data = {"date": pd.date_range(
            start=pd.to_datetime(minutely_15.Time(), unit="s", utc=True),
            end=pd.to_datetime(minutely_15.TimeEnd(), unit="s", utc=True),
            freq=pd.Timedelta(seconds=minutely_15.Interval()),
            inclusive="left"
        )}

        for idx, feature_15 in enumerate(features_minutely_15):
            minutely_15_data[feature_15] = minutely_15.Variables(idx).ValuesAsNumpy()

        minutely_15_dataframe = pd.DataFrame(data=minutely_15_data)
        minutely_15_dataframe = minutely_15_dataframe.set_index('date')
        return minutely_15_dataframe

    def extract_hourly_data(self, api_client: WeatherApiResponse) -> pd.DataFrame:
        features_hourly = self.config_API.features_hourly

        # Process hourly data. The order of variables needs to be the same as requested.
        hourly = api_client.Hourly()

        hourly_data = {"date": pd.date_range(
            start=pd.to_datetime(hourly.Time(), unit="s", utc=True),
            end=pd.to_datetime(hourly.TimeEnd(), unit="s", utc=True),
            freq=pd.Timedelta(seconds=hourly.Interval()),
            inclusive="left"
            )
            }
        for idx, feature_hourly in enumerate(features_hourly):
            hourly_data[feature_hourly] = hourly.Variables(idx).ValuesAsNumpy()

        hourly_dataframe = pd.DataFrame(data=hourly_data)
        hourly_dataframe = hourly_dataframe.set_index('date')
        return hourly_dataframe

    def save_historical_data(self, df_15minuetly, df_hourly):
        local_data_file_15minutely = \
            self.config_historical.local_data_file_15minutely
        local_data_file_hourly = self.config_historical.local_data_file_hourly

        logger.info(f"Saving 15 minuetly historical data to\
                    {local_data_file_15minutely}")
        pd.to_pickle(df_15minuetly, local_data_file_15minutely)

        logger.info(f"Saving hourly historical data to\
                    {local_data_file_hourly}")
        pd.to_pickle(df_hourly, local_data_file_hourly)

    def save_forecast_data(self, df_15minuetly, df_hourly):
        local_data_file_15minutely = \
            self.config_forecast.local_data_file_15minutely
        local_data_file_hourly = self.config_forecast.local_data_file_hourly

        logger.info(f"Saving 15 minuetly forecast data to\
                    {local_data_file_15minutely}")
        pd.to_pickle(df_15minuetly, local_data_file_15minutely)

        logger.info(f"Saving hourly forecast data to {local_data_file_hourly}")
        pd.to_pickle(df_hourly, local_data_file_hourly)

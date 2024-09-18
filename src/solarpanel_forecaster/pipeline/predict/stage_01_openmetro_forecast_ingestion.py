from solarpanel_forecaster.config.configuration import ConfigurationManager
from solarpanel_forecaster.components.open_metroAPI import (
    OpenMetroAPI)
from solarpanel_forecaster import logger
import datetime
import pytz

STAGE_NAME = "STAGE 01: Read in open metro forecast data"


class ForecastOpenMetroAPIPipeline:
    def __init__(self) -> None:
        pass

    def main(self):
        config = ConfigurationManager()
        open_metro_api = OpenMetroAPI(
            config_API=config.get_open_metro_API_config(),
            config_historical=config.get_open_metro_hitorical_config(),
            config_forecast=config.get_open_metro_forecast_config())

        logger.info("Define open metro base url params")
        dic_base_url = open_metro_api.get_base_url_params()

        logger.info("Build Open metro forecast API client")
        forecast_API_client = open_metro_api.get_forecast_api_client(
            base_url_params=dic_base_url)

        utc_time = datetime.datetime.now(pytz.utc)
        logger.info(f'Live time is in "UTC" is {utc_time}')

        logger.info("Extracting 15 minutely data - including past_days")
        df_forecast_15minuetly = open_metro_api.extract_15_minutely_data(
            api_client=forecast_API_client)

        logger.info("Extracting hourly data - including past_days")
        df_forecast_hourly = open_metro_api.extract_hourly_data(
            api_client=forecast_API_client)

        logger.info("Remove past_days data")
        df_forecast_15minuetly = df_forecast_15minuetly[utc_time:]
        df_forecast_hourly = df_forecast_hourly.loc[utc_time:]

        logger.info("Saving forecast open metro data")
        open_metro_api.save_forecast_data(df_15minuetly=df_forecast_15minuetly,
                                          df_hourly=df_forecast_hourly)
        logger.info("Save Complete!")


if __name__ == '__main__':
    try:
        logger.info(f">>>>>> stage {STAGE_NAME} started <<<<<<")
        obj = ForecastOpenMetroAPIPipeline()
        obj.main()
        logger.info(
            f">>>>>> stage {STAGE_NAME} completed <<<<<<\n\nx==========x"
            )
    except Exception as e:
        logger.exception(e)
        raise e

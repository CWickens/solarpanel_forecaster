from solarpanel_forecaster.config.configuration import ConfigurationManager
from solarpanel_forecaster.components.open_metroAPI import (
    OpenMetroAPI)
from solarpanel_forecaster import logger

STAGE_NAME = "TRAINING PIPELINE STAGE 01: Read in open metro historical data"


class HistoricalOpenMetroAPIPipeline:
    def __init__(self) -> None:
        pass

    def main(self):
        config = ConfigurationManager()
        open_metro_API = OpenMetroAPI(
            config_API=config.get_open_metro_API_config(),
            config_historical=config.get_open_metro_hitorical_config(),
            config_forecast=config.get_open_metro_forecast_config()
            )

        logger.info("Define open metro base url params")
        dic_base_url = open_metro_API.get_base_url_params()

        logger.info("Build Open metro historcal API client")
        historical_API_client = open_metro_API.get_historical_api_client(
            base_url_params=dic_base_url
            )

        logger.info("Extracting 15 minutely data")
        df_hist_15minuetly = open_metro_API.extract_15_minutely_data(
            api_client=historical_API_client
            )

        logger.info("Extracting hourly data")
        df_hist_hourly = open_metro_API.extract_hourly_data(
            api_client=historical_API_client
            )

        logger.info("Saving historical open metro data")
        open_metro_API.save_historical_data(df_15minuetly=df_hist_15minuetly,
                                            df_hourly=df_hist_hourly)
        logger.info("Save Complete!")


if __name__ == '__main__':
    try:
        logger.info(f">>>>>> stage {STAGE_NAME} started <<<<<<")
        obj = HistoricalOpenMetroAPIPipeline()
        obj.main()
        logger.info(
            f">>>>>> stage {STAGE_NAME} completed <<<<<<\n\nx==========x"
            )
    except Exception as e:
        logger.exception(e)
        raise e

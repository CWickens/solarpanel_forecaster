from solarpanel_forecaster.config.configuration import ConfigurationManager
from solarpanel_forecaster.components.live_weather_data_ingestion import LiveWeatherDataIngestion
from solarpanel_forecaster import logger


STAGE_NAME = "live weather data ingestion stage"


class LiveWeatherDataIngestionPipeline:
    def __init__(self) -> None:
        pass

    def main(self):
        config = ConfigurationManager()
        live_weather_data_ingestion_config = \
            config.get_live_weather_data_ingestion_config()
        openweathermap_private_config = \
            config.get_openweathermap_private_config()
        live_weather_data_ingestion = LiveWeatherDataIngestion(
            config=live_weather_data_ingestion_config,
            config_secret=openweathermap_private_config)
        live_weather_data_ingestion.download()


if __name__ == '__main__':
    try:
        logger.info(f">>>>>> stage {STAGE_NAME} started <<<<<<")
        obj = LiveWeatherDataIngestionPipeline()
        obj.main()
        logger.info(f">>>>>> stage {STAGE_NAME} completed <<<<<<\n\nx==========x")
    except Exception as e:
        logger.exception(e)
        raise e




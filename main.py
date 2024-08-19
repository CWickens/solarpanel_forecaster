from solarpanel_forecaster import logger
from solarpanel_forecaster.pipeline.stage_01_live_weather_data_ingestion import (
    LiveWeatherDataIngestionPipeline
)


STAGE_NAME = "live weather data ingestion stage"
try:
    logger.info(f">>>>>> stage {STAGE_NAME} started <<<<<<")
    obj = LiveWeatherDataIngestionPipeline()
    obj.main()
    logger.info(f">>>>>> stage {STAGE_NAME} completed <<<<<<\n\nx==========x")
except Exception as e:
    logger.exception(e)
    raise e

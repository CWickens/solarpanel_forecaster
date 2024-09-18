from solarpanel_forecaster import logger
from solarpanel_forecaster.pipeline.predict.\
    stage_01_openmetro_forecast_ingestion import (
        ForecastOpenMetroAPIPipeline)


logger.info('-------- TRIGGERING PREDICTION PIPELINE! --------')

STAGE_NAME = "STAGE 01: Read in open metro forecast data"

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

logger.info('-------- PREDICTION PIPELINE RUN COMPLETED! --------')

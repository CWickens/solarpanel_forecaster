from solarpanel_forecaster import logger
from solarpanel_forecaster.pipeline.predict.\
    stage_01_openmetro_forecast_ingestion import (
        ForecastOpenMetroAPIPipeline)
from solarpanel_forecaster.pipeline.predict.\
    stage_02_prepare_data_and_predict import (
        PrepareDataPredictionPipeline)


def predict():
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

    STAGE_NAME = "STAGE 02: Prepare data and predict solar energy"

    try:
        logger.info(f">>>>>> stage {STAGE_NAME} started <<<<<<")
        obj = PrepareDataPredictionPipeline()
        obj.main()
        logger.info(
            f">>>>>> stage {STAGE_NAME} completed <<<<<<\n\nx==========x"
            )
    except Exception as e:
        logger(e)
        raise e

    logger.info('-------- PREDICTION PIPELINE RUN COMPLETED! --------')


if __name__ == '__main__':
    predict()

from solarpanel_forecaster import logger
from solarpanel_forecaster.pipeline.train.\
    stage_01_openmetro_historical_ingestion import (
        HistoricalOpenMetroAPIPipeline)
from solarpanel_forecaster.pipeline.train.\
    stage_02_solis_historical_data_ingestion import (
        SolisHistoricalDataIngestionPipeline)
from solarpanel_forecaster.pipeline.train.\
    stage_03_prepare_data_for_modeling import (
        PrepareDataTrainingPipeline)
from solarpanel_forecaster.pipeline.train.\
    stage_04_train_solar_model_xgboost import (
        XGBoostSolarTrainingPipeline)


def train_solar_prediction_model():
    logger.info('-------- TRIGGERING TRAINING PIPELINE! --------')

    STAGE_NAME = "STAGE 01: Read in open metro historical data"
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

    STAGE_NAME = "STAGE 02: Solis data ingestion"
    try:
        logger.info(f">>>>>> stage {STAGE_NAME} started <<<<<<")
        obj = SolisHistoricalDataIngestionPipeline()
        obj.main()
        logger.info(
            f">>>>>> stage {STAGE_NAME} completed <<<<<<\n\nx==========x"
            )
    except Exception as e:
        logger(e)
        raise e

    STAGE_NAME = "STAGE 03: Prepare data for modeling"
    try:
        logger.info(f">>>>>> stage {STAGE_NAME} started <<<<<<")
        obj = PrepareDataTrainingPipeline()
        obj.main()
        logger.info(
            f">>>>>> stage {STAGE_NAME} completed <<<<<<\n\nx==========x"
            )
    except Exception as e:
        logger(e)
        raise e

    STAGE_NAME = "STAGE 04: Train model"
    try:
        logger.info(f">>>>>> stage {STAGE_NAME} started <<<<<<")
        obj = XGBoostSolarTrainingPipeline()
        obj.main()
        logger.info(
            f">>>>>> stage {STAGE_NAME} completed <<<<<<\n\nx==========x"
            )
    except Exception as e:
        logger.exception(e)
        raise e

    logger.info('-------- TRAINING PIPELINE RUN COMPLETED! --------')


if __name__ == '__main__':
    train_solar_prediction_model()

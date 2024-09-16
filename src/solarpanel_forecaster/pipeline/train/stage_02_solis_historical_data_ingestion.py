from solarpanel_forecaster.config.configuration import ConfigurationManager
from solarpanel_forecaster.components.solis_data_ingestion import (
    SolisDataIngestion)
from solarpanel_forecaster import logger


STAGE_NAME = "Solis data ingestion"


class SolisHistoricalDataIngestionPipeline:
    def __init__(self) -> None:
        pass

    def main(self):
        config = ConfigurationManager()
        solis_data_ingestion_config = config.get_solis_data_ingestion_config()
        solis_private_config = config.get_solis_private_config()
        solis_data_ingestion = SolisDataIngestion(
            config=solis_data_ingestion_config,
            config_secret=solis_private_config)
        training_start_date = solis_data_ingestion_config.training_start_date
        training_end_date = solis_data_ingestion_config.training_end_date

        # data = solis_data_ingestion.get_todays_data()
        logger.info(f"Extract solis data from {training_start_date} to \
                    {training_end_date}")
        df = solis_data_ingestion.extract_full_daily_range(
            start_date=training_start_date,
            end_date=training_end_date
            )

        logger.info('Save traing solis')
        df.to_pickle(solis_data_ingestion_config.output_file_training)


if __name__ == '__main__':
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

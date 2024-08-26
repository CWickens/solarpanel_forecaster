from solarpanel_forecaster.config.configuration import ConfigurationManager
from solarpanel_forecaster.components.solis_data_ingestion import (
    SolisDataIngestion)
from solarpanel_forecaster import logger


STAGE_NAME = "Solis data ingestion"


class SolisDataIngestionPipeline:
    def __init__(self) -> None:
        pass

    def main(self):
        config = ConfigurationManager()
        solis_data_ingestion_config = config.get_solis_data_ingestion_config()
        solis_private_config = config.get_solis_private_config()
        solis_data_ingestion = SolisDataIngestion(
            config=solis_data_ingestion_config,
            config_secret=solis_private_config)
        data = solis_data_ingestion.get_todays_data()
        solis_data_ingestion.save(data=data)


if __name__ == '__main__':
    try:
        logger.info(f">>>>>> stage {STAGE_NAME} started <<<<<<")
        obj = SolisDataIngestionPipeline()
        obj.main()
        logger.info(
            f">>>>>> stage {STAGE_NAME} completed <<<<<<\n\nx==========x"
            )
    except Exception as e:
        logger(e)
        raise e

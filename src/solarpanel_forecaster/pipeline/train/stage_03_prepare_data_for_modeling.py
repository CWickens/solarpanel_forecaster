from solarpanel_forecaster.config.configuration import ConfigurationManager
from solarpanel_forecaster.components.prepare_data import (
    PrepareData)
from solarpanel_forecaster import logger

STAGE_NAME = "STAGE 03: Prepare data for modeling"


class PrepareDataTrainingPipeline:
    def __init__(self) -> None:
        pass

    def main(self):
        config = ConfigurationManager()
        config_training = config.get_training_data_preparation_config()

        prepare_data = PrepareData(config_training=config_training)
        logger.info("Load metro and solis data")
        df_15minutely, df_hourly, df_solis = prepare_data.load_training_data()
        logger.info("Merge 15 minutely and hourly metro data")
        df_merged_metro = prepare_data.merge_15minutely_and_hourly_data(
            df_15minutely, df_hourly)
        logger.info("Merge metro data to solis data")
        df_merge_all = prepare_data.merge_metro_to_solis_for_training(
            df_merged_metro, df_solis)
        logger.info(f"resample to {config_training.resample} hr")
        df_merge_all = prepare_data.resample_data(df_merge_all)
        logger.info('Make feaures')
        df_merge_all = prepare_data.make_features(df_merge_all)

        logger.info('Save Data')
        df_merge_all.to_pickle(config_training.output_file_train)
        logger.info('Saving complete')


if __name__ == '__main__':
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

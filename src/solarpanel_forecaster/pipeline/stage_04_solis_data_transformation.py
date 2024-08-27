from solarpanel_forecaster.config.configuration import ConfigurationManager
from solarpanel_forecaster.components.solis_data_transformation import (
    SolisDataTransformation
    )
from solarpanel_forecaster import logger

STAGE_NAME = "Solis data transformation"


class SolisDataTransformationPipeline:
    def __init__(self) -> None:
        pass

    def main(self):
        config = ConfigurationManager()
        solis_data_transformation_config =\
            config.get_solis_data_transformation_config()
        solis_data_transformation = SolisDataTransformation(
            config=solis_data_transformation_config)
        raw_data = solis_data_transformation.load()
        transformed_data = solis_data_transformation.transform(
            raw_data=raw_data)
        solis_data_transformation.save(transformed_data=transformed_data)


if __name__ == '__main__':
    try:
        logger.info(f">>>>>> stage {STAGE_NAME} started <<<<<<")
        obj = SolisDataTransformationPipeline()
        obj.main()
        logger.info(
            f">>>>>> stage {STAGE_NAME} completed <<<<<<\n\nx==========x"
            )
    except Exception as e:
        logger(e)
        raise e

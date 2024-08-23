from solarpanel_forecaster.config.configuration import ConfigurationManager
from solarpanel_forecaster.components.live_weather_data_transformation import (
    LiveWeatherDataTransformation)
from solarpanel_forecaster import logger


STAGE_NAME = "Live weather data transformation"


class LiveWeatherDataTransformationPipeline:
    def __init__(self) -> None:
        pass

    def main(self):
        config = ConfigurationManager()
        live_weather_data_transformation_config = \
            config.get_live_weather_data_transformation_config()
        live_weather_data_transformation = LiveWeatherDataTransformation(
            config=live_weather_data_transformation_config)
        live_weather_data_transformation.load()

        df_forecast = live_weather_data_transformation.get_hourly_forecast()
        df_actual = live_weather_data_transformation.get_actual_weather()

        live_weather_data_transformation.save(
            df_forecast,
            live_weather_data_transformation_config.output_file_forecast)
        live_weather_data_transformation.save(
            df_actual,
            live_weather_data_transformation_config.output_file_actuals)


if __name__ == '__main__':
    try:
        logger.info(f">>>>>> stage {STAGE_NAME} started <<<<<<")
        obj = LiveWeatherDataTransformationPipeline()
        obj.main()
        logger.info(
            f">>>>>> stage {STAGE_NAME} completed <<<<<<\n\nx==========x"
            )
    except Exception as e:
        logger(e)
        raise e

from solarpanel_forecaster.constants import (
    CONFIG_FILE_PATH,
    CONFIG_SECRET_FILE_PATH,
    PARAMS_FILE_PATH,
    SCHEMA_FILE_PATH
    )
from solarpanel_forecaster.utils.common import read_yaml, create_directories
from solarpanel_forecaster.entity.config_entity import (
    LiveWeatherDataIngestionConfig,
    OpenWeatherMapPrivateConfig,
    LiveWeatherDataTransformationConfig)


class ConfigurationManager:
    def __init__(
            self,
            config_filepath=CONFIG_FILE_PATH,
            config_secret_filepath=CONFIG_SECRET_FILE_PATH,
            params_filepath=PARAMS_FILE_PATH,
            schema_filepath=SCHEMA_FILE_PATH):

        self.config = read_yaml(config_filepath)
        self.config_secret = read_yaml(config_secret_filepath)
        self.params = read_yaml(params_filepath)
        self.schema = read_yaml(schema_filepath)

        create_directories([self.config.artifacts_root])

    def get_live_weather_data_ingestion_config(self) \
            -> LiveWeatherDataIngestionConfig:

        config = self.config.live_weather_data_ingestion

        create_directories([config.root_dir])

        live_weather_data_ingestion_config = LiveWeatherDataIngestionConfig(
            root_dir=config.root_dir,
            base_url=config.base_url,
            local_data_file=config.local_data_file,
            hours_of_history=config.hours_of_history,
            secret_info=config.secret_info
        )
        return live_weather_data_ingestion_config

    def get_openweathermap_private_config(self) -> OpenWeatherMapPrivateConfig:
        config_secret = self.config_secret.openweathermap_private

        openweathermap_private_config = OpenWeatherMapPrivateConfig(
            lat=config_secret.lat,
            lon=config_secret.lon,
            apikey=config_secret.apikey)
        return openweathermap_private_config

    def get_live_weather_data_transformation_config(self) \
            -> LiveWeatherDataTransformationConfig:
        config = self.config.live_weather_data_transformation

        create_directories([config.root_dir])

        live_weather_data_transformation_config = \
            LiveWeatherDataTransformationConfig(
                root_dir=config.root_dir,
                input_file=config.input_file,
                output_file=config.output_file
                )
        return live_weather_data_transformation_config

from solarpanel_forecaster.constants import (
    CONFIG_FILE_PATH,
    CONFIG_SECRET_FILE_PATH,
    PARAMS_FILE_PATH,
    SCHEMA_FILE_PATH
    )
from solarpanel_forecaster.utils.common import read_yaml, create_directories
from solarpanel_forecaster.entity.config_entity import (
    # LiveWeatherDataIngestionConfig,
    # OpenWeatherMapPrivateConfig,
    # LiveWeatherDataTransformationConfig,
    OpenMetroAPIConfig,
    OpenMetroHitoricalConfig,
    OpenMetroForecastConfig,
    SolisDataIngestionConfig,
    SolisPrivateConfig,
    SolisDataTransformationConfig
    )


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

    def get_open_metro_API_config(self) -> OpenMetroAPIConfig:
        config = self.config.open_metro_API

        create_directories([config.root_dir])

        open_metro_API_config = \
            OpenMetroAPIConfig(
                root_dir=config.root_dir,
                latitude=config.latitude,
                longitude=config.longitude,
                features_minutely_15=config.features_minutely_15,
                features_hourly=config.features_hourly
            )

        return open_metro_API_config

    def get_open_metro_hitorical_config(self) -> OpenMetroHitoricalConfig:
        config = self.config.open_metro_hitorical

        open_metro_hitorical_config = \
            OpenMetroHitoricalConfig(
                local_data_file_15minutely=config.local_data_file_15minutely,
                local_data_file_hourly=config.local_data_file_hourly,
                start_date=config.start_date,
                end_date=config.end_date
            )
        return open_metro_hitorical_config

    def get_open_metro_forecast_config(self) -> OpenMetroForecastConfig:
        config = self.config.open_metro_forecast

        open_metro_forecast_config = \
            OpenMetroForecastConfig(
                local_data_file_15minutely=config.local_data_file_15minutely,
                local_data_file_hourly=config.local_data_file_hourly,
                past_days=config.past_days,
                forecast_days=config.forecast_days
            )
        return open_metro_forecast_config

    def get_solis_data_ingestion_config(self) -> SolisDataIngestionConfig:
        config = self.config.solis_data_ingestion

        create_directories([config.root_dir])

        solis_data_ingestion_config = \
            SolisDataIngestionConfig(
                root_dir=config.root_dir,
                output_file=config.output_file,
                url=config.url,
                VERB=config.VERB,
                string_format=config.string_format,
                encoder=config.encoder,
                Content_Type=config.Content_Type,
                CanonicalizedResource=config.CanonicalizedResource
            )
        return solis_data_ingestion_config

    def get_solis_private_config(self) -> SolisPrivateConfig:
        config = self.config_secret.solis_private

        solis_private_config = SolisPrivateConfig(
            KeyId=config.KeyId,
            secretKey=config.secretKey,
            sn=config.sn
        )
        return solis_private_config

    def get_solis_data_transformation_config(self) -> \
            SolisDataTransformationConfig:
        config = self.config.solis_data_transformation

        solis_data_transformation_config = SolisDataTransformationConfig(
            root_dir=config.root_dir,
            input_file=config.input_file,
            output_file=config.output_file
        )
        return solis_data_transformation_config

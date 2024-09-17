from pathlib import Path
from dataclasses import dataclass


# @dataclass(frozen=True)
# class LiveWeatherDataIngestionConfig:
#     root_dir: Path
#     base_url: str
#     base_url_forecast: str
#     local_data_file: Path
#     hours_of_history: int
#     secret_info: Path


# @dataclass
# class OpenWeatherMapPrivateConfig:
#     lat: float
#     lon: float
#     apikey: str


# @dataclass(frozen=True)
# class LiveWeatherDataTransformationConfig:
#     root_dir: Path
#     input_file: Path
#     output_file_forecast: Path
#     output_file_actuals: Path
#     hours_of_forecast: int


@dataclass(frozen=True)
class OpenMetroAPIConfig:
    root_dir: Path
    latitude: float
    longitude: float
    features_minutely_15: list
    features_hourly: list


@dataclass(frozen=True)
class OpenMetroHitoricalConfig:
    local_data_file_15minutely: Path
    local_data_file_hourly: Path
    start_date: str
    end_date: str


@dataclass(frozen=True)
class OpenMetroForecastConfig:
    local_data_file_15minutely: Path
    local_data_file_hourly: Path
    past_days: float
    forecast_days: float


@dataclass(frozen=True)
class SolisDataIngestionConfig:
    root_dir: str
    output_file_training: str
    training_start_date: str
    training_end_date: str
    output_file_today: str
    url: str
    VERB: str
    string_format: str
    encoder: str
    Content_Type: str
    CanonicalizedResource: str


@dataclass(frozen=True)
class SolisPrivateConfig:
    KeyId: str
    secretKey: str
    sn: str


@dataclass(frozen=True)
class SolisDataTransformationConfig:
    root_dir: str
    input_file: Path
    output_file: Path


@dataclass(frozen=True)
class TrainingDataPreparationConfig:
    root_dir: Path
    input_data_15minutely: Path
    input_data_hourly: Path
    output_file_train: Path
    input_solis: Path
    resample: str
    target_var: str
    laggTime: list[int]
    lagged_features: list

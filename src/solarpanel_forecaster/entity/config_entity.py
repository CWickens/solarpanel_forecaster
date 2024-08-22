from pathlib import Path
from dataclasses import dataclass


@dataclass(frozen=True)
class LiveWeatherDataIngestionConfig:
    root_dir: Path
    base_url: str
    base_url_forecast: str
    local_data_file: Path
    hours_of_history: int
    secret_info: Path


@dataclass
class OpenWeatherMapPrivateConfig:
    lat: float
    lon: float
    apikey: str


@dataclass(frozen=True)
class LiveWeatherDataTransformationConfig:
    root_dir: Path
    input_file: Path
    output_file_forecast: Path
    output_file_actuals: Path
    hours_of_forecast: int

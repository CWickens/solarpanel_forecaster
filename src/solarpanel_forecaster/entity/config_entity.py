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


@dataclass(frozen=True)
class SolisDataIngestionConfig:
    root_dir: str
    output_file: str
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

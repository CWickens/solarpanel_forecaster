import pandas as pd
import json
from solarpanel_forecaster import logger
from solarpanel_forecaster.config.configuration import (
    SolisDataTransformationConfig
)


class SolisDataTransformation:
    def __init__(
            self,
            config: SolisDataTransformationConfig):
        self.config = config

    def load(self):
        input_file = self.config.input_file

        with open(input_file, 'r') as f:
            logger.info(f"Loading {input_file} ...")
            data = json.load(f)
            logger.info("Loading complete!")
        return data

    def save(self, transformed_data: pd.DataFrame):
        output_file = self.config.output_file

        logger.info(f"Saving to {output_file} ...")
        transformed_data.to_pickle(output_file)
        logger.info(("Save successful!"))

    def transform(self, raw_data):

        logger.info('processing data ...')
        df = pd.DataFrame(data=raw_data['data'])
        df['timeStr'] = pd.to_datetime(df['timeStr'])
        dfCP = df.copy().drop(columns=["dataTimestamp", "time", "pacStr"])
        dfCP = dfCP.select_dtypes(exclude=['object'])
        dfCP = dfCP.set_index("timeStr")
        logger.info('data processing complete')
        return dfCP

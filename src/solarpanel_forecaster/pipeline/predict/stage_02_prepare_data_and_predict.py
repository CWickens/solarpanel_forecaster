from solarpanel_forecaster.config.configuration import ConfigurationManager
from solarpanel_forecaster.components.prepare_data import (
    PrepareData)
from solarpanel_forecaster import logger
import pandas as pd
import pickle
import matplotlib.pyplot as plt

STAGE_NAME = "STAGE 02: Prepare data and predict solar energy"


class PrepareDataPredictionPipeline:
    def __init__(self) -> None:
        pass

    def main(self):
        config = ConfigurationManager()
        config_training = config.get_training_data_preparation_config()
        forecast_config = config.get_open_metro_forecast_config()
        XGBoost_config = config.get_xgboost_solar_config()

        logger.info("Load 15 minutely and hourly live metro forecast")
        df_15minutely = pd.read_pickle(
            forecast_config.local_data_file_15minutely)
        df_hourly = pd.read_pickle(forecast_config.local_data_file_hourly)

        prepare_data = PrepareData(config_training=config_training)

        logger.info("Merge 15 minutely and hourly metro data")
        df_merged = prepare_data.merge_15minutely_and_hourly_data(
            df_15minutely=df_15minutely, df_hourly=df_hourly)

        logger.info(f"resample to {config_training.resample} hr")
        df_merged = prepare_data.resample_data(df_merge_final=df_merged)

        logger.info('Make feaures')
        df_merged = prepare_data.make_features(df=df_merged)

        logger.info('Load xgboost model')
        with open(XGBoost_config.model_path, 'rb') as f:
            loaded_model = pickle.load(f)

        logger.info('Predict solar profile')
        df_merged['prediction'] = loaded_model.predict(df_merged)

        prediction_save_path =\
            'artifacts/04_model/xgboost_solar_prediction.pickle'
        logger.info(f'Save solar prediction to {prediction_save_path}')
        df_merged.to_pickle(prediction_save_path)
        logger.info('Saving complete!')

        logger.info('Plot solar energy prediction')
        fig, axs = plt.subplots(2, 1)
        fig.tight_layout(pad=4)

        df_merged['prediction'].plot(ax=axs[0])
        current_hourly_time = df_merged.index[0].strftime("%Y-%m-%d %H")
        forecast_days = forecast_config.forecast_days
        axs[0].set_title(
            f'+ {forecast_days}DAY Solar pannel energy\n \
                production forecast current time (UTC): {current_hourly_time}')

        df_merged.loc[:df_merged.index[0] + pd.Timedelta('1D')]['prediction']\
            .plot(ax=axs[1])
        axs[1].set_title(f'+ 24HR Solar pannel energy production forecast\n \
                     current time (UTC): {current_hourly_time}')

        plt.show()


if __name__ == '__main__':
    try:
        logger.info(f">>>>>> stage {STAGE_NAME} started <<<<<<")
        obj = PrepareDataPredictionPipeline()
        obj.main()
        logger.info(
            f">>>>>> stage {STAGE_NAME} completed <<<<<<\n\nx==========x"
            )
    except Exception as e:
        logger(e)
        raise e

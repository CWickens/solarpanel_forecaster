from solarpanel_forecaster.config.configuration import ConfigurationManager
from solarpanel_forecaster.components.xgboost_solar_training import (
   XGBoostSolarTraining)
from solarpanel_forecaster import logger
import matplotlib.pyplot as plt

STAGE_NAME = "STAGE 04: Train model"


class XGBoostSolarTrainingPipeline:
    def __init__(self) -> None:
        pass

    def main(self):
        config = ConfigurationManager()
        config_xgboost = config.get_xgboost_solar_config()

        xgboost_solar = XGBoostSolarTraining(config_xgboost=config_xgboost)

        logger.info('Read in historical data')
        df_hist = xgboost_solar.load_historical_data()
        logger.info('test/train split')
        X_train, X_test, y_train, y_test = xgboost_solar.make_train_test_set(
            df=df_hist)
        logger.info('Hyperparameter tunning')
        best_params = xgboost_solar.hyperparameter_tunning(
            X_train=X_train, y_train=y_train)
        logger.info('Retrian model using best params and test')
        final_model, y_pred, score = xgboost_solar.test_model(
            X_train=X_train,
            X_test=X_test,
            y_train=y_train,
            y_test=y_test,
            best_params=best_params)

        logger.info('Save model')
        xgboost_solar.save_model(model=final_model)
        logger.info('Save complete!')
        logger.info('Save training data')
        xgboost_solar.save_training_data(
            X_train=X_train,
            X_test=X_test,
            y_train=y_train,
            y_test=y_test)
        logger.info('Save complete!')

        # plot prediction vs actual for a particular region
        ix_start = 1500
        ix_end = 1900
        # Plot the true values
        plt.plot(y_test[ix_start:ix_end].reset_index(drop=True),
                 label='Actual Values')

        # Plot the predicted values
        plt.plot(y_pred[ix_start:ix_end], label='Predicted Values')

        # Add labels, title, and legend
        plt.xlabel('Time')
        plt.ylabel('W')
        plt.title('Actual vs. Predicted Values (sample region)')
        plt.legend()
        plt.show(block=False)


if __name__ == '__main__':
    try:
        logger.info(f">>>>>> stage {STAGE_NAME} started <<<<<<")
        obj = XGBoostSolarTrainingPipeline()
        obj.main()
        logger.info(
            f">>>>>> stage {STAGE_NAME} completed <<<<<<\n\nx==========x"
            )
    except Exception as e:
        logger.exception(e)
        raise e

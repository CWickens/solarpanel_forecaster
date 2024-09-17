import pandas as pd
from sklearn.model_selection import train_test_split, GridSearchCV
import xgboost as xgb
from solarpanel_forecaster.entity.config_entity import (
    XGBoostSolarConfig)
from sklearn.metrics import mean_squared_error
import pickle
from solarpanel_forecaster import logger


class XGBoostSolarTraining:
    def __init__(
            self,
            config_xgboost: XGBoostSolarConfig):
        self.config_xgboost = config_xgboost

    def load_historical_data(self):
        historical_data = self.config_xgboost.historical_data

        df = pd.read_pickle(historical_data)
        return df

    def make_train_test_set(self, df):
        test_size = self.config_xgboost.test_size
        target = self.config_xgboost.target

        features = [i for i in df.columns if i != target]
        X = df[features]
        y = df[target]

        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=test_size, shuffle=False)
        return X_train, X_test, y_train, y_test

    def hyperparameter_tunning(self, X_train, y_train):
        cv = self.config_xgboost.cv
        scoring = self.config_xgboost.scoring
        max_depth = self.config_xgboost.max_depth
        learning_rate = self.config_xgboost.learning_rate
        n_estimators = self.config_xgboost.n_estimators
        subsample = self.config_xgboost.subsample

        # Create XGBoost model
        xgb_model = xgb.XGBRegressor()

        # Hyperparameter grid
        param_grid = {
            'max_depth': max_depth,
            'learning_rate': learning_rate,
            'n_estimators': n_estimators,
            'subsample': subsample
        }

        # Grid Search
        grid_search = GridSearchCV(xgb_model, param_grid, cv=cv,
                                   scoring=scoring)
        grid_search.fit(X_train, y_train)

        # Best parameters
        best_params = grid_search.best_params_
        return best_params

    def test_model(self, X_train, X_test, y_train, y_test, best_params):

        # Train model with best parameters
        final_model = xgb.XGBRegressor(**best_params)
        final_model.fit(X_train, y_train)

        # Make predictions
        y_pred = final_model.predict(X_test)

        score = mean_squared_error(y_test, y_pred)
        logger.info(f'test RMSE: {score}')
        return final_model, y_pred, score

    def save_model(self, model):
        model_path = self.config_xgboost.model_path

        with open(model_path, 'wb') as f:
            pickle.dump(model, f)

    def save_training_data(self, X_train, X_test, y_train, y_test):
        X_train_data_path = self.config_xgboost.X_train_data_path
        X_test_data_path = self.config_xgboost.X_test_data_path
        y_train_data_path = self.config_xgboost.y_train_data_path
        y_test_data_path = self.config_xgboost.y_test_data_path

        X_train.to_pickle(X_train_data_path)
        X_test.to_pickle(X_test_data_path)
        y_train.to_pickle(y_train_data_path)
        y_test.to_pickle(y_test_data_path)

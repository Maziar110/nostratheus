from prometheus_api_client import PrometheusConnect
from datetime import timedelta, datetime
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.feature_selection import RFE
import config
import joblib
from os import path, mkdir
import pickle

prom = PrometheusConnect(url=config.prom_url)
file_directory = './trained_models/'


def data_extractor(metric):
    # # Real datetime period
    interval = timedelta(days=config.interval)
    end_time2 = datetime.now()
    start_time2 = end_time2 - interval
    chunk_size = timedelta(hours=config.chunk_size)

    metric_data = prom.get_metric_range_data(
        metric,  # this is the metric name and label config
        start_time=start_time2,
        end_time=end_time2,
        chunk_size=chunk_size,
    )

    a = metric_data[0]['values']
    x = []
    y = []
    for i in a:
        x.append(i[0])
        y.append(i[1])
    # print(x, y, sep='\n')
    x = np.asarray(x)
    y = np.asarray(y)

    y = y.astype(np.float)
    x = x.astype(np.float)
    # print(x)
    x_data = []

    for item in x:
        item = datetime.utcfromtimestamp(item)
        day = item.day
        weekday = item.weekday()
        sec_from_day = (item - item.replace(hour=0, minute=0, second=0, microsecond=0)).total_seconds()
        x_data.append([sec_from_day, day, weekday])

    x_data = np.asarray(x_data)
    # print(x_data)
    x_data = np.asarray(x_data)
    return [x_data, y]


def model_trainer_rfe(metric):
    data = data_extractor(metric)
    x = data[0]
    y = data[1]
    # # RFE (RandomForest Regression model)
    rfe = RFE(RandomForestRegressor(random_state=0, n_estimators=10000, max_depth=6))
    rfe.fit(x, y)
    # # # Test the model
    scored = rfe.score(x, y)
    # res = rfe.predict([x[15]])
    # # # save the trained model
    file_name = file_directory + str(metric) + '.joblib'

    # creates directory of trained files if doesn't exist
    if path.exists(file_directory):
        pass
    else:
        mkdir(file_directory)

    with open(file_name, 'wb') as file:
        joblib.dump(rfe, file)

    return scored


def train_models():
    """
    this method is going to train the model based on interval data and
     write down on file if it's not already exist
     """

    for metric in config.metrics:
        file_name = file_directory + str(metric) + '.joblib'
        if path.exists(file_name):
            print(f'Model for {metric} is already trained\n We are about to optimize data adding')
        else:
            try:
                score = model_trainer_rfe(metric)
                print(f'Model Trained successfully for {metric} the score: {score}')
            except Exception as e:
                print(e)
                print(f'Model {metric} did not train, check the error')


# print(train_models())



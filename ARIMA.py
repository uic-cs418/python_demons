import pandas as pd
import numpy as np
from pandas import datetime
from matplotlib import pyplot
from pandas.plotting import autocorrelation_plot
from statsmodels.tsa.arima_model import ARIMA

from sklearn.metrics import mean_squared_error
from loss import ape

def parser(x):
    return datetime.strptime(x, '%m/%d/%Y')

def bus_prediction():
    # Importing dataset
    folder_location = 'data'
    file_name = 'CTA_-_Ridership_-_Bus_Routes_-_Monthly_Day-Type_Averages___Totals.csv'
    bus = pd.read_csv(open(folder_location + '\\' + file_name), parse_dates=['Month_Beginning'], date_parser=parser)

    df = bus.loc[bus['route'] == '8']

    df = df.loc[:, ['Month_Beginning', 'MonthTotal']]
    df.set_index('Month_Beginning', inplace=True)

    # Rolling Predictions
    X = df.values
    size = len(X) - 12 # 1 year
    train, test = X[0:size], X[size:len(X)]
    test = [x[0] for x in test]
    history = [x for x in train]
    predictions = list()
    for t in range(len(test)):
        model = ARIMA(history, order=(8,1,0))
        model_fit = model.fit(disp=0)
        output = model_fit.forecast()
        yhat = output[0]
        predictions.append(yhat[0])
        obs = test[t]
        history.append(obs)
        # print('predicted=%f, expected=%f' % (yhat, obs))
    error = ape(test, predictions)
    print('Test Absolute Percentage Error: ' + str(round(error, 5)))

    # plot
    pyplot.title('2019 Ridership Prediction (Rolling) for the Halsted Bus Route')
    pyplot.plot(test, color='blue', label='Actual')
    pyplot.plot(predictions, color='red', label='Predicted')
    pyplot.legend(loc="upper left")
    pyplot.xticks(np.arange(12), ('J', 'F', 'M', 'A', 'M', 'J', 'J', 'A', 'S', 'O', 'N', 'D'))
    pyplot.xlabel('Months (2019)')
    pyplot.ylabel('Ridership')
    pyplot.show()

def train_prediction():
    # Importing dataset
    folder_location = 'data'
    file_name = 'CTA_-_Ridership_-__L__Station_Entries_-_Monthly_Day-Type_Averages___Totals.csv'
    trains = pd.read_csv(open(folder_location + '\\' + file_name), parse_dates=['month_beginning'], date_parser=parser)

    df = trains.loc[trains['stationame'] == 'Halsted-Orange']

    df = df.loc[:, ['month_beginning', 'monthtotal']]
    df.set_index('month_beginning', inplace=True)

    # Rolling Predictions
    X = df.values
    size = len(X) - 12 # 1 year
    train, test = X[0:size], X[size:len(X)]
    test = [x[0] for x in test]
    history = [x for x in train]
    predictions = list()
    for t in range(len(test)):
        model = ARIMA(history, order=(8,1,1))
        model_fit = model.fit(disp=0)
        output = model_fit.forecast()
        yhat = output[0]
        predictions.append(yhat[0])
        obs = test[t]
        history.append(obs)
        # print('predicted=%f, expected=%f' % (yhat, obs))
    error = ape(test, predictions)
    print('Test Absolute Percentage Error: ' + str(round(error, 5)))

    # plot
    pyplot.title('2019 Ridership Prediction (Rolling) for the Halsted Station')
    pyplot.plot(test, color='blue', label='Actual')
    pyplot.plot(predictions, color='red', label='Predicted')
    pyplot.legend(loc="upper left")
    pyplot.xticks(np.arange(12), ('J', 'F', 'M', 'A', 'M', 'J', 'J', 'A', 'S', 'O', 'N', 'D'))
    pyplot.xlabel('Months (2019)')
    pyplot.ylabel('Ridership')
    pyplot.show()
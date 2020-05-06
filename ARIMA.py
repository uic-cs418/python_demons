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

def list_bus_routes():
    # Importing dataset
    folder_location = 'data'
    file_name = 'CTA_-_Ridership_-_Bus_Routes_-_Monthly_Day-Type_Averages___Totals.csv'
    bus = pd.read_csv(open(folder_location + '\\' + file_name), parse_dates=['Month_Beginning'], date_parser=parser)
    return np.array(sorted(bus.route.unique().tolist()))

def list_train_stations():
    # Importing dataset
    folder_location = 'data'
    file_name = 'CTA_-_Ridership_-__L__Station_Entries_-_Monthly_Day-Type_Averages___Totals.csv'
    trains = pd.read_csv(open(folder_location + '\\' + file_name), parse_dates=['month_beginning'], date_parser=parser)
    return np.array(sorted(trains.stationame.unique().tolist()))
    
def bus_prediction(route_number):
    # Importing dataset
    folder_location = 'data'
    file_name = 'CTA_-_Ridership_-_Bus_Routes_-_Monthly_Day-Type_Averages___Totals.csv'
    bus = pd.read_csv(open(folder_location + '\\' + file_name), parse_dates=['Month_Beginning'], date_parser=parser)

    df = bus.loc[bus['route'] == route_number]

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
    #print('Test Absolute Percentage Error: ' + str(round(error, 5)))
    
    # Checking change
    avg_pred = sum(predictions) / len(predictions)
    #print('Average Pred: ' + str(avg_pred))
    avg_history = sum(history) / len(history)
    #print('Average History: ' + str(avg_history[0]))
    percent_change = avg_pred / avg_history
    #print('% change: ' + str(percent_change[0]))
    print('Prediction: ', end='')
    if(percent_change <= 0.98): 
        if(percent_change >= 0.95):
            print('Slight Decrease ', end='[')
        else:
            print('Heavy Decrease ', end='[')
    elif(percent_change >= 1.02):
        if(percent_change <= 1.05):
            print('Slight Increase ', end='[')
        else:
            print('Heavy Increase ', end='[')
    else:
        print('No significant change ', end='[')
    print('Prediction Accuracy: ' + str(round(100 - error, 2)) + ']')
    
    # plot
    pyplot.rcParams["figure.figsize"] = (14, 7) # (w, h)
    fig, axs = pyplot.subplots(nrows=1, ncols=2)
    fig.subplots_adjust(wspace=0.3)
    df.iloc[-60:-12].plot(ax=axs[0])
    axs[0].set_title('Average Monthly Ridership 2015-18')
    axs[0].set_xlabel('Month - Year')
    axs[0].set_ylabel('Ridership')
    axs[1].set_title('2019 Ridership Prediction (Rolling)')
    axs[1].plot(test, color='blue', label='Actual')
    axs[1].plot(predictions, color='red', label='Predicted')
    axs[1].legend(loc="upper left")
    axs[1].set_xticks(np.arange(12), ('J', 'F', 'M', 'A', 'M', 'J', 'J', 'A', 'S', 'O', 'N', 'D'))
    axs[1].set_xlabel('Months (2019)')
    axs[1].set_ylabel('Ridership')
    fig.suptitle('Average Monthly Ridership and Prediction for Bus Route: ' + str(route_number), fontsize=16)

def train_prediction(station_name):
    # Importing dataset
    folder_location = 'data'
    file_name = 'CTA_-_Ridership_-__L__Station_Entries_-_Monthly_Day-Type_Averages___Totals.csv'
    trains = pd.read_csv(open(folder_location + '\\' + file_name), parse_dates=['month_beginning'], date_parser=parser)

    df = trains.loc[trains['stationame'] == station_name]

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
    #print('Test Absolute Percentage Error: ' + str(round(error, 5)))

    # Checking change
    avg_pred = sum(predictions) / len(predictions)
    #print('Average Pred: ' + str(avg_pred))
    avg_history = sum(history) / len(history)
    #print('Average History: ' + str(avg_history))
    percent_change = avg_pred / avg_history
    #print('% change: ' + str(percent_change))
    print('Prediction: ', end='')
    if(percent_change <= 0.98): 
        if(percent_change >= 0.95):
            print('Slight Decrease ', end='[')
        else:
            print('Heavy Decrease ', end='[')
    elif(percent_change >= 1.02):
        if(percent_change <= 1.05):
            print('Slight Increase ', end='[')
        else:
            print('Heavy Increase ', end='[')
    else:
        print('No significant change ', end='[')
    print('Prediction Accuracy: ' + str(round(100 - error, 2)) + ']')
    
    # plot
    pyplot.rcParams["figure.figsize"] = (14, 7) # (w, h)
    fig, axs = pyplot.subplots(nrows=1, ncols=2)
    fig.subplots_adjust(wspace=0.3)
    df.iloc[-60:-12].plot(ax=axs[0])
    axs[0].set_title('Average Monthly Ridership 2015-18')
    axs[0].set_xlabel('Month - Year')
    axs[0].set_ylabel('Ridership')
    axs[1].set_title('2019 Ridership Prediction (Rolling)')
    axs[1].plot(test, color='blue', label='Actual')
    axs[1].plot(predictions, color='red', label='Predicted')
    axs[1].legend(loc="upper left")
    axs[1].set_xticks(np.arange(12), ('J', 'F', 'M', 'A', 'M', 'J', 'J', 'A', 'S', 'O', 'N', 'D'))
    axs[1].set_xlabel('Months (2019)')
    axs[1].set_ylabel('Ridership')
    fig.suptitle('Average Monthly Ridership and Prediction for ' + str(station_name) + ' Station', fontsize=16)
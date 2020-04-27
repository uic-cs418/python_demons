import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def all_monthly_ml(monthly):

    import statsmodels.formula.api as smf
    #Supervised Machine Learning to predcit the ridership over the years using Long Short-term Memory (LSTM)
    month_sum = monthly.groupby(['year','month'],as_index= False).sum()
    month_sum['date'] = pd.to_datetime(month_sum[['year', 'month']].assign(DAY=1))
    some = month_sum.loc[(month_sum.year == 2019) | (month_sum.year == 2018) | (month_sum.year == 2017)]
    month_sum['prev'] = month_sum['MonthTotal'].shift(1)
    month_sum = month_sum.dropna()
    month_sum['diff'] = month_sum['MonthTotal'] - month_sum['prev']
    # ax = month_sum.plot.line(x = 'date',y='diff')
    month_sum_spr = month_sum.drop(['prev','year','month','Avg_Weekday_Rides','Avg_Saturday_Rides','Avg_Sunday-Holiday_Rides'],axis=1)
    for inc in range(1,19):
        field_name = 'lag_' + str(inc)
        month_sum_spr[field_name] = month_sum_spr['diff'].shift(inc)
    month_sum_spr = month_sum_spr.dropna().reset_index(drop=True)
    model = smf.ols(formula='diff ~ lag_1 + lag_2 + lag_3 + lag_4+ lag_5 + lag_6 + lag_7 + lag_8 + lag_9 + lag_10 + lag_11 + lag_12 + lag_13 + lag_14 + lag_15 + lag_16 + lag_17  ', data=month_sum_spr)
    model_fit = model.fit()
    regression_adj_rsq = model_fit.rsquared_adj
    print(regression_adj_rsq)
    from sklearn.preprocessing import MinMaxScaler
    df_model = month_sum_spr.drop(['MonthTotal','date'],axis=1)
    train_set, test_set = df_model[0:-6].values, df_model[-6:].values
    #apply Min Max Scaler
    scaler = MinMaxScaler(feature_range=(-1, 1))
    scaler = scaler.fit(train_set)
    # reshape training set
    train_set = train_set.reshape(train_set.shape[0], train_set.shape[1])
    train_set_scaled = scaler.transform(train_set)# reshape test set
    test_set = test_set.reshape(test_set.shape[0], test_set.shape[1])
    test_set_scaled = scaler.transform(test_set)
    X_train, y_train = train_set_scaled[:, 1:], train_set_scaled[:, 0:1]
    X_train = X_train.reshape(X_train.shape[0], 1, X_train.shape[1])
    X_test, y_test = test_set_scaled[:, 1:], test_set_scaled[:, 0:1]
    X_test = X_test.reshape(X_test.shape[0], 1, X_test.shape[1])
    from keras.models import Sequential
    from keras.layers.core import Dense, Dropout
    from keras.layers.recurrent import LSTM
    model = Sequential()
    model.add(LSTM(4, batch_input_shape=(1, X_train.shape[1], X_train.shape[2]), stateful=True))
    model.add(Dense(1))
    model.compile(loss='mean_squared_error', optimizer='adam')
    model.fit(X_train, y_train, nb_epoch=100, batch_size=1, verbose=1, shuffle=False)
    y_pred = model.predict(X_test,batch_size=1)
    y_pred = y_pred.reshape(y_pred.shape[0], 1, y_pred.shape[1])
    pred_test_set = []
    for index in range(0,len(y_pred)):
        pred_test_set.append(np.concatenate([y_pred[index],X_test[index]],axis=1))
    pred_test_set = np.array(pred_test_set)
    pred_test_set = pred_test_set.reshape(pred_test_set.shape[0], pred_test_set.shape[2])#inverse transform
    pred_test_set_inverted = scaler.inverse_transform(pred_test_set)
    result_list = []
    dates = list(month_sum[-7:].date)
    train = list(month_sum[-7:].MonthTotal)
    for index in range(0,len(pred_test_set_inverted)):
        result_dict = {}
        result_dict['date'] = dates[index+1]
        result_dict['pred_value'] = int(pred_test_set_inverted[index][0] + train[index])
        result_dict['pred_value'] = result_dict['pred_value']
        result_list.append(result_dict)
    df_result = pd.DataFrame(result_list)
    print(df_result)
    return(month_sum , df_result)

def graph_all_bus(month_sum, df_result):
    df_pred = pd.merge(month_sum , df_result, on='date', how='left')
    ax = df_pred.plot.line(x = 'date',y=['MonthTotal','pred_value'])
    fig = plt.gcf()
    plt.xticks(fontsize =12)
    plt.yticks(fontsize = 12)
    fig.set_size_inches(16.5, 9.5)
    fig.savefig('test2png.png', dpi=100)
    return ax

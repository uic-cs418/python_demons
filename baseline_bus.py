def baseline(monthly):
    import pandas as pd
    import numpy as np
    route_group = monthly.groupby(['route'],as_index=False).count()
    # For All the routes which ran all the months of 19 years
    route_group = route_group.loc[route_group.routename == 228]
        # List of All such groups
    route_groups = route_group['route'].tolist()
        # DF with only such routes
    monthly = monthly.loc[monthly['route'].isin(route_groups)]
    train = monthly.loc[monthly.year <= 2018]
    test = monthly.loc[monthly.year == 2019]
    test = test.sort_values(by=['route'])
    mean = train.groupby(['route','month'],as_index = False).mean()
    prediction = mean.MonthTotal.astype(int)
    prediction = prediction.tolist()
    real = test.MonthTotal.tolist()
    avg_accuracy = 0
    for i in range(0,len(real)):
        accuracy = ((abs(real[i]- prediction[i]))/real[i])*100
        accuracy = 100 - accuracy
        avg_accuracy = ((avg_accuracy*i) + accuracy)/(i+1)
    return avg_accuracy

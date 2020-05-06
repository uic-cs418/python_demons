def bar_race(monthly):
    import pandas as pd
    race_df = monthly
    temp1  = race_df
    temp1['year'] = pd.DatetimeIndex(temp1['Month_Beginning']).year
    temp1 = temp1.drop(["Month_Beginning"],axis =1)
    temp1 = temp1.groupby(["routename","year"]).mean().unstack()
    #temp1 =temp1.nlargest(50,"MonthTotal")
    # routes = list(temp1["routename"])
    # routes
    temp1.columns = temp1.columns.get_level_values(1)
    temp1 = temp1.reset_index()
    temp1.to_csv('bar_race.csv', index=False)
    return temp1

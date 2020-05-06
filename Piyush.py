import pandas as pd
import numpy as np
from datetime import datetime
import calendar 
import seaborn as sns
import matplotlib.pyplot as plt

uniroute=[]

def data_preparation(data):
	days,years = findDay(data['date'])
	data['days']=days
	data['year']=years
	uniroute=data.route.unique()
	dgrp=data.groupby(['route','daytype','days','year']).sum()
	newDF = pd.DataFrame()
	notweek=[]
	inweek=[]
	# dgrp=dgrp.unstack()
	dgrp=dgrp.reset_index()
	for every in uniroute:
		dgrpr1=dgrp.loc[(dgrp['route']==every) & (dgrp['daytype']=='W')]
		size=dgrpr1.shape[0]

		if (size == 95):
			newDF=newDF.append(dgrpr1)
		else:
			notweek.append(every)
	return newDF

def createplot(newDF):
	years=[2013,2014,2015,2016,2017,2018,2019]
	nndf= newDF[newDF.year.isin(years)]
	nndf=nndf.groupby(['days','year']).mean()
	nndf=nndf.reset_index()
	y=sns.barplot(x="days",y="rides",hue="year",data=nndf,palette="plasma")
	plt.legend(title='Year',loc='center left',bbox_to_anchor=(1,0.5))
	plt.xlabel("Weekdays")
	plt.ylabel("Mean ridership for each year")
	plt.title("Mean Bus ridership for weekdays from 2013 - 2019")
	plt.show()


def findDay(dd): 
    daylist=[]
    yearlist=[]
    for date in dd:
        month, day, year = (int(i) for i in date.split('/'))  
        dayNumber = calendar.weekday(year, month, day) 
        days =["Monday", "Tuesday", "Wednesday", "Thursday", 
                             "Friday", "Saturday", "Sunday"] 
        daylist.append(days[dayNumber])
        yearlist.append(year)
    return daylist,yearlist
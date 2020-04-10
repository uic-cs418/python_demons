#!/usr/bin/env python
# coding: utf-8

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import sklearn
import os
import datetime
import calendar 
import matplotlib.ticker as ticker
import matplotlib.animation as animation
from IPython.display import HTML

pt = pd.DataFrame()
ax = ""

def data_cleaning(data):
    data = add_day(data)
    data = add_year(data)
    return data

def perform_eda(data):
    data = calc_mean_ridership(data)
    data = aggregating_over_day_of_week(data)
    return data

# Adding day column to see how ridership varies by the day
def add_day(data):
    day= []
    for index, value in data['date'].items():
        week_day= datetime.datetime.strptime(value, '%m/%d/%Y').weekday() 
        day.append(calendar.day_name[week_day])
    data['Day']=day
    return data


# Adding year column to aggregate over years to analyze trends in ridership
def add_year(data):
    data['year'] = pd.DatetimeIndex(data['date']).year
    return data


# Checking for missing values in the data
def check_misssing_values(data):
    return data.isna()


# Calculating the mean ridership for each day of the week for each bus
def calc_mean_ridership(data):
    data_mod = data.loc[:,['Day','rides','year']]
    data_mod = data_mod.loc[data_mod["year"]>2014,:]
    return data_mod

# Aggregating over day of the week
def aggregating_over_day_of_week(data):
    pivot=data.pivot_table(values="rides", index=["Day","year"], dropna=True, fill_value=0, aggfunc="mean")
    pivot['year'] = pivot.index
    pivot['Day'] = pivot.index
    l = []
    s=[]
    for index, value in pivot['year'].items():
        l.append(value[1])
        s.append(value[0])
    pivot['year'] = l
    pivot['Day'] = s
    return pivot


# ### The CTA train ridership has plummeted not just on weekends due to office holidays but also on weekdays due to the commuter movement to other competetive trains like metra 

def day_of_week(data):
    y=sns.barplot(x="Day",y="rides",hue="year",data=data,palette="viridis")
    plt.ylim(1000, 4500)
    plt.legend(title='Year',loc='center left',bbox_to_anchor=(1,0.5))
    plt.xlabel("Day of the week")
    plt.ylabel("Mean ridership for each year")
    plt.title("Mean train ridership for each day of the week over the past 4 years")
    plt.show()


# Animated bar plot 
def draw_barchart(year,pt,ax):
    #global pt
    dff = pt[pt['year'].eq(year)].sort_values(by='rides', ascending=False).head(10)
    #global ax
    ax.clear()
    ax.barh(dff['stationname'], dff['rides'])
    dx = dff['rides'].max() / 200
    for i, (value, name) in enumerate(zip(dff['rides'], dff['stationname'])):
        ax.text(value-dx, i,     name,           size=14, weight=600, ha='right', va='bottom')
        ax.text(value+dx, i,     f'{value:,.0f}',  size=14, ha='left',  va='center')
    # ... polished styles
    ax.text(1, 0.4, year, transform=ax.transAxes, color='#777777', size=46, ha='right', weight=800)
    ax.text(0, 1.06, 'rides', transform=ax.transAxes, size=12, color='#777777')
    ax.xaxis.set_major_formatter(ticker.StrMethodFormatter('{x:,.0f}'))
    ax.xaxis.set_ticks_position('top')
    ax.tick_params(axis='x', colors='#777777', labelsize=12)
    ax.set_yticks([])
    ax.margins(0, 0.01)
    ax.grid(which='major', axis='x', linestyle='-')
    ax.set_axisbelow(True)
    ax.text(0, 1.10, 'The most popular train stations in Chicago from 2001 to 2019',
            transform=ax.transAxes, size=24, weight=600, ha='left')  
    ax.text(0, 1.17, 'Note: Please hit the front arrow -> button to start the animation',
            transform=ax.transAxes, size=14, weight=600, ha='left')  
    plt.box(False)
    return

# EDA and slicing
def eda_animated_bar_plot(data):
    global pt
    L_year = data.loc[:,['year','rides','stationname','station_id']]
    pt = L_year.pivot_table(values="rides", index=["stationname","year"], dropna=True, fill_value=0, aggfunc="mean" )
    pt['year'] = pt.index
    pt['stationname'] = pt.index
    l = []
    s = []
    for index, value in pt['year'].items():
        l.append(value[1])
        s.append(value[0])
    pt['year'] = l
    pt['stationname'] = s
    
    # Visualization of the animated bar plot
    global ax
    fig, ax = plt.subplots(figsize=(15, 8))
    animator = animation.FuncAnimation(fig, draw_barchart, frames=range(2001, 2020))
    HTML(animator.to_jshtml())
    return
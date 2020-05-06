import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
monthly = pd.read_csv("data\\Bus_monthly(weekday,weekend,total).csv")

def clean(monthly):
    # Adding Year to the file
    monthly['year'] = pd.DatetimeIndex(monthly['Month_Beginning']).year
    # Adding Month to the file
    monthly['month'] = pd.DatetimeIndex(monthly['Month_Beginning']).month
    #Leap year Adjustment
    for i in range(0, len(monthly.index)):
        if((monthly.at[i,'month'] == 2) & (monthly.at[i,'year']  in ([2000, 2004, 2008, 2012, 2016, 2020]))):
            monthly.at[i,'MonthTotal'] = (monthly.at[i,'MonthTotal'] * 365)/366
    return(monthly)


def routes_drastic_change(monthly):
    # Grouping by route 
    route_group = monthly.groupby(['route'],as_index=False).count()
    # For All the routes which ran all the months of 19 years
    route_group = route_group.loc[route_group.routename == 228]
    # List of All such groups
    route_groups = route_group['route'].tolist()
    # DF with only such routes
    monthly_reg = monthly.loc[monthly['route'].isin(route_groups)]
    # All regular routes grouped by route and year
    group_route_year = monthly_reg.groupby(['route','year'],as_index = False).mean()
    #Normalizing all the Average Rides with respect to 2001
    normalized_avg = group_route_year
    for i in range (0,103):
        j = i*19
        avg_2001 = normalized_avg.at[j,'Avg_Weekday_Rides']
        for k in range (j, j+19):
            if(normalized_avg.at[k,'Avg_Weekday_Rides']>avg_2001):
                normalized_avg.at[k,'Avg_Weekday_Rides'] = normalized_avg.at[k,'Avg_Weekday_Rides']/avg_2001
            else:
                normalized_avg.at[k,'Avg_Weekday_Rides'] = avg_2001/normalized_avg.at[k,'Avg_Weekday_Rides']
    for i in range(0,103):
        j = i*19
        for k in range(j, j+19):
            normalized_avg.at[k,'Avg_Weekday_Rides'] = (1-normalized_avg.at[k,'Avg_Weekday_Rides'])*(1-normalized_avg.at[k,'Avg_Weekday_Rides'])
    max5 = []
    max_of_all = []
    for j in range(0,103):
        k = j*19
        max_local = 0
        for l in range(k, k+19):
            a = normalized_avg.at[l,'Avg_Weekday_Rides']
            if(a>max_local):
                max_local = a
        max_of_all.append(max_local)
    max_of_all2 = max_of_all.copy()
    for i in range(0,10):
        max_of5 = 0
        for m in range(0,len(max_of_all)):
            if(max_of_all[m]>max_of5):
                max_of5 = max_of_all[m]
        max_of_all.remove(max_of5)
        max5.append(max_of5)
    indexes = []
    for i in range(0,len(max5)):
        indexes.append(max_of_all2.index(max5[i]))
    route_list = [route_groups[i] for i in indexes]
    print(route_list) #All the regular routes with most drastic change in descending order of drasticity
    return route_list

def polar_vertex(monthly):
    #Finding Trend for Polar Vertex
    import seaborn as sns
    #Selecting for the month of January
    winter_df = monthly.loc[(monthly.month == 1)]
    year_df = monthly.groupby(['year'],as_index = False).sum()
    #Grouping Based on Year and then Month
    winter_df = winter_df.groupby(['year','month'],as_index = False).sum()
    # Finding Share of month of January out of Total Ridership in the year
    winter_df['percentage_share'] =  winter_df.MonthTotal*100/year_df.MonthTotal
    jan_1819 = winter_df.loc[(winter_df.year == 2018) | (winter_df.year == 2019)]
    diff = (jan_1819.at[17,'percentage_share'] - jan_1819.at[18,'percentage_share'])*100/jan_1819.at[17,'percentage_share']
    print(diff) #Difference between percentage share of JAN 2018 and JAN 2019 (Polar Vertex)
    ax = winter_df.plot.bar(x = 'year',y='percentage_share',legend = False)
    fig = plt.gcf()
    plt.xticks(fontsize =12,rotation='horizontal')
    plt.yticks(fontsize = 12)
    fig.set_size_inches(10, 4)
    fig.savefig('test1png.png', dpi=100)
    plt.ylim(0,12)
    plt.title('Ridership Percentage for January \n out of total ridership in the year ',loc='center',fontsize = 18,color = 'darkblue')
    plt.xlabel('\n X-axis : Years', fontsize =15)
    plt.ylabel('Y-axis : Ridership (in Perecent %) \n ', fontsize =15)
    plt.annotate("Heavy Snowing w.r.t. Decemeber",(13,7.45),clip_on=True,textcoords="offset points",xytext=(-140,+50),arrowprops=dict(arrowstyle="->", connectionstyle="arc3,rad=.2",color = 'black'),fontsize=15)
    plt.annotate("Polar Vertex",(18,7.43),textcoords="offset points",xytext=(-75,+30),arrowprops=dict(arrowstyle="->", connectionstyle="arc3,rad=.2",color = 'black'),fontsize=15)
    return (ax)

def Overall_graph_bus(monthly):
    year_df = monthly.groupby(['year'],as_index = False).sum()
    ax = year_df.plot.line(x='year',y = 'MonthTotal',linewidth=2.5, marker = 'D',color = 'limegreen',mec = 'black',mfc = 'gray',legend = False)
    fig = plt.gcf()
    x = year_df.year
    plt.xticks(x,fontsize =12)
    plt.yticks(fontsize = 12)
    fig.set_size_inches(10, 5)
    fig.savefig('1.png', dpi=100)
    plt.grid(color='gray', linestyle='-', linewidth=.5)
    plt.xlim(2000,2019.5)
    plt.ylim(210000000,340000000)
    plt.title('The Total Ridership of BUS from 2001-2019 \n ',loc='center',fontsize = 18,color = 'darkblue')
    plt.xlabel('\n X-axis : Years', fontsize =15)
    plt.ylabel('Y-axis : Total Ridership (* 100 million) \n ', fontsize =15)
    plt.annotate("Increased downtown routes",(2008,328000000),textcoords="offset points",xytext=(+20,-10),arrowprops=dict(arrowstyle="->", connectionstyle="arc3,rad=.2"),fontsize=15)
    plt.annotate("Large Service Cuts \n in South",(2010,303000000),textcoords="offset points",xytext=(-100,-50),arrowprops=dict(arrowstyle="->", connectionstyle="arc3,rad=.2"),fontsize=15)
    plt.annotate("UBER Started Operations in Chicago",(2012,313000000),textcoords="offset points",xytext=(+40,-15),arrowprops=dict(arrowstyle="->", connectionstyle="arc3,rad=.2"),fontsize=15)
    plt.annotate("Heavy Downtown \n Road Construction",(2016,256000000),textcoords="offset points",xytext=(-200,-40),arrowprops=dict(arrowstyle="->", connectionstyle="arc3,rad=.2"),fontsize=15)
    return(ax)




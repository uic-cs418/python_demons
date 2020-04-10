import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
# Adding Year to the file
monthly = pd.read_csv("Bus_monthly(weekday,weekend,total).csv")

def clean(monthly):
    monthly['year'] = pd.DatetimeIndex(monthly['Month_Beginning']).year
    # Adding Month to the file
    monthly['month'] = pd.DatetimeIndex(monthly['Month_Beginning']).month
    #Leap year Adjustment
    for i in range(0, len(monthly.index)):
        if((monthly.at[i,'month'] == 2) & (monthly.at[i,'year']  in ([2000, 2004, 2008, 2012, 2016, 2020]))):
            monthly.at[i,'MonthTotal'] = (monthly.at[i,'MonthTotal'] * 365)/366
    return(monthly)

def Overall_graph(monthly):
    year_df = monthly.groupby(['year'],as_index = False).sum()
    ax = year_df.plot.line(x='year',y = 'MonthTotal',linewidth=2.5, marker = 'D',color = 'limegreen',mec = 'black',mfc = 'gray',legend = False)
    fig = plt.gcf()
    x = year_df.year
    plt.xticks(x,fontsize =12)
    plt.yticks(fontsize = 12)
    fig.set_size_inches(12.5, 6.5)
    fig.savefig('test2png.png', dpi=100)
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

def gasvsbus(gas,year_df):
    #variation of GAS price in Chicago over the years
    
    gas['year'] = pd.DatetimeIndex(gas['Date']).year
    gas = gas.loc[~gas.year.isin([2000,2020])]
    gas.reset_index(inplace = True, drop = True)
    gas = gas.groupby(['year'],as_index = False).mean()

    #Co-relation of GAS prices and Ridreship
    a = year_df.MonthTotal
    b = gas.Price
    c = a.corr(b)
    display(c)

    ax = gas.plot.line(x = 'year',y = 'Price' ,linewidth=2.5, marker = 'o',color = 'black',mfc = 'white')
    year_df['MonthTotal1'] = year_df.MonthTotal/100000000
    year_df.plot.line(x='year',y = 'MonthTotal1',ax = ax,linewidth=2.5, marker = 'o',color = 'red',mec = 'black',mfc = 'white')
    fig = plt.gcf()
    x = year_df.year
    plt.xticks(x,fontsize =12)
    plt.yticks(fontsize = 12)
    fig.set_size_inches(12.5, 6.5)
    fig.savefig('test2png.png', dpi=100)
    plt.xlim(2000,2019.5)
    plt.ylim(1,4.5)
    plt.grid(color='gray', linestyle='-', linewidth=.3)
    plt.legend(loc= 'center right',title = "Correlation b/w Gas Price and Ridership",labels = ['Gas Price','Bus Ridership'],bbox_to_anchor=(1, .9),fontsize = 16)
    plt.title('Correlation Between Gas Prices in Chicago \n vs. CTA Bus Ridership ',loc='center',fontsize = 18,color = 'darkblue')
    plt.xlabel('\n Years', fontsize =15)
    plt.ylabel('GAS - Price in $/gallon \n Bus - Ridership in 100 Million ', fontsize =15)
    plt.show()
    return(ax)



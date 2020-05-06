import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
monthly = pd.read_csv("data\\Bus_monthly(weekday,weekend,total).csv")
gas = pd.read_csv('data\\gas.csv')


def gasvsbus(gas,monthly):
    #variation of GAS price in Chicago over the years
    year_df = monthly.groupby(['year'],as_index = False).sum()
    gas['year'] = pd.DatetimeIndex(gas['Date']).year
    gas = gas.loc[~gas.year.isin([2000,2020])]
    gas.reset_index(inplace = True, drop = True)
    gas = gas.groupby(['year'],as_index = False).mean()

    #Co-relation of GAS prices and Ridreship
    a = year_df.MonthTotal
    b = gas.Price
    c = a.corr(b)
    print("Correlation between Gas prices and Bus Ridership is ",c)

    ax = gas.plot.line(x = 'year',y = 'Price' ,linewidth=2.5, marker = 'o',color = 'black',mfc = 'white')
    year_df['MonthTotal1'] = year_df.MonthTotal/100000000
    year_df.plot.line(x='year',y = 'MonthTotal1',ax = ax,linewidth=2.5, marker = 'o',color = 'red',mec = 'black',mfc = 'white')
    fig = plt.gcf()
    x = year_df.year
    plt.xticks(x,fontsize =12)
    plt.yticks(fontsize = 12)
    fig.set_size_inches(12.5, 6.5)
    fig.savefig('2.png', dpi=100)
    plt.xlim(2000,2019.5)
    plt.ylim(1,4.5)
    plt.grid(color='gray', linestyle='-', linewidth=.3)
    plt.legend(loc= 'center right',title = "Correlation b/w Gas Price and Ridership",labels = ['Gas Price','Bus Ridership'],bbox_to_anchor=(1, .9),fontsize = 16)
    plt.title('Correlation Between Gas Prices in Chicago \n vs. CTA Bus Ridership ',loc='center',fontsize = 18,color = 'darkblue')
    plt.xlabel('\n Years', fontsize =15)
    plt.ylabel('GAS - Price in $/gallon \n Bus - Ridership in 100 Million ', fontsize =15)
    plt.show()
    return(ax)



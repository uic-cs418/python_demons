
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.pyplot import figure

def overall_cta(year):
    from matplotlib.pyplot import figure
    for i in range(0, len(year.index),4):
        year.at[i,'bus'] = (year.at[i,'bus'] * 365)/366
        year.at[i,'paratransit'] = year.at[i,'paratransit'] * (365/366)
        year.at[i,'rail'] = year.at[i,'rail'] * (365/366)
        year.at[i,'total'] = year.at[i,'total'] * (365/366)
    ax1 = year.plot.line(x='year',y= 'total',linewidth=2.5, marker = 'D',color = 'limegreen',mec = 'black',mfc = 'gray',legend = False)
    fig = plt.gcf()
    x = year.year
    plt.xticks(x,fontsize =11)
    fig.set_size_inches(18.5, 10.5)
    fig.savefig('3.png', dpi=100)
    plt.grid(color='gray', linestyle='-', linewidth=.5)
    plt.xlim(1987,2019)
    plt.title('The Total Ridership of CTA from 1988-2018 \n ',loc='center',fontsize = 18,color = 'darkblue')
    plt.xlabel('\n X-axis : Years', fontsize =15)
    plt.ylabel('\n Y-axis : Total Ridership (* 100 million) ', fontsize =15)
    plt.annotate("The Drastic Fall \n from 1990",(1993,460000000),textcoords="offset points",xytext=(-100,-70),arrowprops=dict(arrowstyle="->", connectionstyle="arc3,rad=.2"),fontsize=15)
    plt.annotate("UBER began its \n operations in Chicago",(2012,545000000),textcoords="offset points",xytext=(-30,+70),arrowprops=dict(arrowstyle="->", connectionstyle="arc3,rad=.2"),fontsize=15)
    plt.annotate("Multiple Service \n Cuts",(2010,516000000),textcoords="offset points",xytext=(0,-70),arrowprops=dict(arrowstyle="->", connectionstyle="arc3,rad=.2"),fontsize=15)
    return(ax1)

#The user imports the name of the stock and the corresponding data are imported using the yfinance library. After
#running the analysis using data since a fixed date and till today, the results are exported as a txt file. Also exported
#are two charts showing the progression of the stock's return for the first chart and how that compares to the msci's returns
#over the same span for the second chart.


from tkinter import *
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import yfinance as yf
from datetime import datetime

def disappear(a):
    a.place(x=0,y=0,width=0,height=0)

def OK():
    disappear(label2)
    disappear(entry1)
    disappear(entry2)
    label1.config(text='The file has been updated')
    label1.place(x=150, y=80, width=200, height=20)
    global path
    path=entry2.get()
    global name
    name=entry1.get()
    analysis()
    saving()

def analysis():
    stock = yf.Ticker(name)
    msci = yf.Ticker('msci')

    end_date = datetime.now().strftime('%Y-%m-%d')
    print(end_date)

    stock_hist = stock.history(start='2023-10-1', end=end_date)
    df = pd.DataFrame(stock_hist)
    df1 = df[['Open', 'Close']].copy()
    df1['daily return %'] = (df1['Close'] - df1['Open']) / df1['Open'] * 100
    df1 = round(df1, 2)

    msci_hist = msci.history(start='2023-10-1', end=end_date)
    df = pd.DataFrame(msci_hist)
    df2 = df[['Open', 'Close']].copy()
    df2['daily return %'] = (df2['Close'] - df2['Open']) / df2['Open'] * 100
    df2 = round(df2, 2)

    x = df2['daily return %'].tolist()

    y = df1['daily return %'].tolist()

    a, b = linear_regression(x, y)
    global data
    data = df1['daily return %'].describe()
    data = data.drop(['count', '25%', '50%', '75%'])
    data.loc[len(data)] = b

    data.index = ['average daily return: ', 'standard deviation:   ', 'lowest daily return:  ',
                  'highest daily return: ', 'beta coefficient:     ']
    print(a, b)
    print(data)
    plotting(df1,df2)
    saving()


def saving():
    global data
    global path
    data.to_csv(path + 'stock analysis.txt', sep=' ',header=False)

def plotting(df1,df2):
    global path
    df1['daily return %'].plot.bar(rot=1)
    plt.xticks([])
    plt.ylabel('daily returns of the stock(%)')
    plt.xlabel('time')
    plt.title('chart1')
    plt.savefig(path + 'chart1.png')

    x = list(range(0, len(df1 + 1)))
    plt.xticks([])
    plt.plot(x, df1['daily return %'], c='r')
    plt.plot(x, df2['daily return %'], c='b')
    plt.xlabel('time')
    plt.ylabel('daily returns %')
    plt.title('chart2')
    plt.savefig(path + 'chart2.png')




def linear_regression(x,y):
    xvar = float(sum(x) / len(x))
    yvar = sum(y) / len(y)
    b1 = 0
    b2 = 0
    for i in range(0, len(y)):
        b1 += (x[i] - xvar) * (y[i] - yvar)
        b2 += (x[i] - xvar) ** 2
    b = b1 / b2
    a = yvar - b * xvar
    print(a,b)
    a=round(a,4)
    b=round(b,4)
    return[a,b]

window=Tk()
window.geometry('500x500')
window.title('Stock Analysis')

label1=Label(window,text='Name of the Stock: ')
label2=Label(window,text='Where to save the file: ')
entry1=Entry(window)
entry2=Entry(window)
button=Button(window,text='OK',command=OK)

label1.place(x=20,y=80,width=200,height=20)
label2.place(x=20,y=110,width=200,height=20)
entry1.place(x=230,y=80,width=200,height=20)
entry2.place(x=230,y=110,width=200,height=20)
button.place(x=430,y=140)






window.mainloop()
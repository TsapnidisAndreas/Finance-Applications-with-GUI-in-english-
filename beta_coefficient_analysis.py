from tkinter import *
#Calculating the beta coeffcient of a stock using the annual returns of the MSCI world index over the last
#ten years. The annual returns of the stock are given manually by the user.
# In order to run the analysis we store the stock as an object and after the beta coefficient has been calculated it is
#stored in a dictionary so it can later be retrieved and used for future predictions.

class Stock:
    def __init__(self,name,a,b):
        self.name=name
        self.a=a
        self.b=b


def ns():
    disappear_all()
    entry1.place(x=520, y=110, width=150, height=20)
    label1.place(x=50, y=110, width=470, height=20)
    entry3.place(x=520, y=140, width=150, height=20)
    label3.place(x=110, y=140, width=150, height=20)
    submit_button1.place(x=700,y=110,width=50,height=20)

def es():
    disappear_all()
    entry2.place(x=400, y=110, width=150, height=20)
    label2.place(x=110, y=110, width=150, height=20)
    entry5.place(x=400, y=140, width=150, height=20)
    label5.place(x=60, y=140, width=300, height=20)
    submit_button3.place(x=700,y=110,width=50,height=20)

def disappear(a):
    a.place(x=0, y=0, width=0, height=0)

def disappear_all():
    disappear(label1)
    disappear(label2)
    disappear(label3)
    disappear(label4)
    disappear(label5)
    disappear(label6)
    disappear(entry1)
    disappear(entry2)
    disappear(entry3)
    disappear(entry5)
    disappear(submit_button1)
    disappear(submit_button2)
    disappear(submit_button3)
    disappear(OK_button1)

def submit1():
    disappear_all()
    global name
    name=entry3.get()
    global year
    year=int(entry1.get())
    if year>=2013:
        global labels
        global entries
        labels=[]
        entries=[]
        j=0
        j2=150
        for i in range (2022,year-1,-1):
            labels.append(Label(window,text='Annual Return for '+str(i)+':(%)'))
            entries.append(Entry(window,font=("arial",10)))
            labels[j].place(x=110,y=j2,width=150,height=20)
            entries[j].place(x=290, y=j2, width=150, height=20)
            j+=1
            j2+=30
        submit_button2.place(x=700,y=j2-30,width=50,height=20)
    else:
        label4.config(text="Not enough data. Try a year after 2012")
        label4.place(x=200, y=110, width=400, height=20)


def submit2():
    disappear_all()
    y=[]
    for i in range (0,2022-year+1):
        y.append(float(entries[i].get()))
        disappear(labels[i])
        disappear(entries[i])
    a,b=linear_regression(x,y)
    global name
    global stocks
    stocks[name]=Stock(name,a,b)
    global number_of_stocks
    number_of_stocks+=1
    label4.config(text="The beta coefficient of the stock is: "+str(stocks[name].b))
    label4.place(x=200, y=110, width=400, height=20)
    OK_button1.place(x=700, y=110, width=50, height=20)

def submit3():
    disappear_all()
    looking_name = entry2.get()
    MSCI_return=float(entry5.get())
    stock = stocks[looking_name]
    stock_return =stock.a+stock.b * MSCI_return
    stock_return=round(stock_return,2)
    label6.config(text="The projected return of the stock is: "+str(stock_return)+"%")
    label6.place(x=200, y=110, width=400, height=20)

def OK1():
    disappear_all()

def linear_regression(x,y):
    x = x[0:len(y)]
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
    print(x)
    print(y)
    print(a,b)
    return[a,b]

window = Tk()
window.geometry('800x800')
window.title('b coefficient analysis')

menubar=Menu(window)
window.config(menu=menubar)
menubar.add_command(label='Enter a new stock for analysis',command=ns)
menubar.add_command(label='Future projection of an existing stock',command=es)

entry1=Entry(window,font=("arial",10))
label1=Label(window,text="To calculate the beta coeffcient I should take account the returns since year: " )

entry2=Entry(window,font=("arial",10))
label2=Label(window,text="Name of the stock: " )

entry3=Entry(window,font=("arial",10))
label3=Label(window,text="Name of the stock: " )

label4=Label(window,text=" ")

entry5=Entry(window,font=("arial",10))
label5=Label(window,text="The projected return of MSCI is(%): ")

label6=Label(window,text=" ")

submit_button1=Button(text='OK',command=submit1)

submit_button2=Button(text='OK',command=submit2)

submit_button3=Button(text='OK',command=submit3)

OK_button1=Button(text='OK',command=OK1)

global x
x=[-17.37,22.35,16.5,28.4,-8.15,23,8.15,0.32,5.5,27.37]

global number_of_stocks
number_of_stocks = 0

global stocks
stocks={}

window.mainloop()
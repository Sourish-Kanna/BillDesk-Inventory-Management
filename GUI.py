#GUI Source Code
import modules.Install as Ins

Ins.install()
try:
    from modules.SQL_IDGenrate import supp_gen, prod_gen, cust_gen
except:
    raise SystemExit
from modules.SQL_Update import Update_All, Update_other
from modules.SQL_Entry import Create
from time import strftime as stime
import mysql.connector as mysql
from tkinter import messagebox
from datetime import datetime
from modules.PDF import Pdf
from tkinter import ttk
from tkinter import *

import modules.SQL_Pass as Pas
pas,us=Pas.Pass()

supplst = ['Select Supplier']
prodlst = ['Select Product']
unitlst = ('Select Unit', 'Kgs', 'Nos')
product = []
supplier = []
prodname = {}
gstlst = ('Select GST Rate', '00.00 %', '05.00 %', '12.00 %', '18.00 %', '28.00 %')


def sql_csv_imp():
    cc = messagebox.askquestion("Bulk Data Entry", "Do you want to add Data from file?")
    if cc == 'yes':
        window1 = Tk()
        window1.title('Bulk Data Entry')
        window1.config(bg='yellow')
        window1.focus_force()
        window1.iconbitmap(r'modules/1.ico')
        import modules.SQL_CSV as SQL0

        def imp():
            SQL0.Read_csv(us, pas)
            alist()
            window1.destroy()

        def cancel():
            SQL0.Delfile()
            window1.destroy()

        SQL0.New_csv()
        f = f"\nFile Created. Now Enter Data and click on Import Data when done."
        lab = Label(window1, text=f, bg='yellow', font=("arial", 14))
        lab.pack(padx=20)
        f = f"Only Supplier name is required for multiple products of same supplier."
        lab1 = Label(window1, text=f, bg='yellow', font=("arial", 14))
        lab1.pack(pady=10, padx=20)
        button0 = Button(window1, text="Import Data", bg="brown", fg="white",
                         font=('arial', 14), command=imp)
        button0.pack(padx=10)
        button1 = Button(window1, text="Cancel Import", bg="brown", fg="white",
                         font=('arial', 14), command=cancel)
        button1.pack(pady=10, padx=10)


def sql_csv_exp():
    cc = messagebox.askquestion("Export Database", "Do you want to export database?")
    if cc == 'yes':
        import modules.SQL_CSV as SQL0
        SQL0.Export_csv(us, pas)

def Helpwind():
    from modules.Help import Help
    Help()

def alist():
    global supplst, prodlst, prodname, product
    demodb = mysql.connect(host="localhost", user=us, passwd=pas, database="projectold")
    cursor = demodb.cursor()
    cursor.execute(f"SELECT SuppID,SuppName FROM supplier where Hide='N'")
    supplier = list(cursor.fetchall())
    supplst = ['Select Supplier']
    for i in supplier:
        ABC = f'{i[0]} - {i[1]}'
        supplst.append(ABC)

    cursor.execute(f"SELECT ProdID,Name FROM product where Hide='N'")
    product = list(cursor.fetchall())
    prodname = {}
    prodlst = ['Select Product']
    for i in product:
        ABC = f'{i[0]} - {i[1]}'
        prodname[i[0]] = i[1]
        prodlst.append(ABC)

    demodb.close()


def sql_data_create():
    from modules.SQL_Datacreate import SQL
    SQL(us, pas)
    sql_csv_imp()
    alist()


def exit_prog():
    ask_exit = messagebox.askquestion("Exit", "Do You Want To Exit Application ?")
    if ask_exit == 'yes':
        window.destroy()
    else:
        pass


def Suppdetail():
    right.place(x=220, y=55)
    SuppID = supp_gen(us, pas)
    right1 = Frame(right, bd=2, relief=SOLID, padx=50, pady=50)
    right1.pack()

    def Close():
        right1.destroy()
        Main()
        right.place(x=5000, y=80)

    def Back():
        right1.destroy()
        Main_Add()
        right.place(x=5000, y=80)

    def Save(tup):
        Create(1, tup, us, pas)
        supplst.append("{0} - {1}".format(tup[0], tup[1]))
        supplier.append((tup[0], tup[1]))
        Close()

    def Show(tup0):
        SuppName, SuppAdd, SuppPhone, SuppEmail = tup0
        SuppName = SuppName.title()
        SuppAdd = SuppAdd.title()
        Name.set(SuppName)
        Add.set(SuppAdd)
        eName.config(state='disabled')
        eAdd.config(state='disabled')
        ePhone.config(state='disabled')
        eEmail.config(state='disabled')
        button1.destroy()
        button2.destroy()
        tup = (SuppID, SuppName, SuppAdd, SuppPhone, SuppEmail)

        def OK():
            Save(tup)

        def callback(event):
            OK()

        right1.focus_set()
        right1.bind('<Return>', callback)

        button0 = Button(right1, text="All Ok! Lets save it", bg="brown", fg="white",
                         font=('arial', 14), command=OK)
        button0.grid(row=5, column=0, columnspan=2, pady=10)
        button = Button(right1, text="Cancel", bg="brown", fg="white",
                        font=('arial', 14), command=Close)
        button.grid(row=5, column=1, pady=10, sticky=E)

    def Check():
        phone, email = Phone.get(), Email.get()
        aad = eAdd.get(1.0, END).strip()
        Add.set(aad)
        a = 0
        if email == '':
            pass
        elif '@' not in email or '.' not in email:
            Email.set("")
            eEmail.focus()
            a = 1
        if not phone.isdigit():
            Phone.set("")
            ePhone.focus()
            a = 1
        if a == 1:
            messagebox.showerror("Wrong Format", "Wrong Format\nCheck Again")
        elif a == 0:
            Show(tuple([Name.get(), Add.get(), Phone.get(), Email.get()]))

    ID = StringVar()
    Name = StringVar()
    Add = StringVar()
    Phone = StringVar()
    Email = StringVar()

    ID.set(SuppID)

    lID = Label(right1, text="Supplier ID", font=("arial", 14))
    lID.grid(row=0, column=0, sticky=W)

    eID = Entry(right1, textvar=ID, state='disabled', font=("arial", 14))
    eID.grid(row=0, column=1, sticky=W, padx=10, pady=10)

    lName = Label(right1, text="Supplier Name", font=("arial", 14))
    lName.grid(row=1, column=0, sticky=W)

    eName = Entry(right1, textvar=Name, font=("arial", 14))
    eName.grid(row=1, column=1, sticky=W, padx=10, pady=10)
    eName.focus()

    lAdd = Label(right1, text="Supplier Address", font=("arial", 14))
    lAdd.grid(row=2, column=0, sticky=W)

    eAdd = Text(right1, width=20, height=3, font=("arial", 14))
    eAdd.grid(row=2, column=1, sticky=W, padx=10, pady=10)

    lPhone = Label(right1, text="Supplier Phone No.", font=("arial", 14))
    lPhone.grid(row=3, column=0, sticky=W)

    ePhone = Entry(right1, textvar=Phone, font=("arial", 14))
    ePhone.grid(row=3, column=1, sticky=W, padx=10, pady=10)

    lEmail = Label(right1, text="Supplier Email", font=("arial", 14))
    lEmail.grid(row=4, column=0, sticky=W)

    eEmail = Entry(right1, textvar=Email, font=("arial", 14))
    eEmail.grid(row=4, column=1, sticky=W, padx=10, pady=10)

    def callback(event):
        eAdd.focus()

    eName.bind('<Return>', callback)

    def callback(event):
        ePhone.focus()

    eAdd.bind('<Return>', callback)

    def callback(event):
        eEmail.focus()

    ePhone.bind('<Return>', callback)

    def callback(event):
        Check()

    eEmail.bind('<Return>', callback)

    button1 = Button(right1, text="Check", width=7, bg="brown", fg="white",
                     font=('arial', 14), command=Check)
    button1.grid(row=5, column=0, pady=10, columnspan=2, padx=10)
    button3 = Button(right1, text="Back", width=5, bg="brown", fg="white",
                     font=('arial', 14), command=Back)
    button3.grid(row=5, column=0, pady=10, padx=10, sticky=W)
    button2 = Button(right1, text="Exit", width=5, bg="brown", fg="white",
                     font=('arial', 14), command=Close)
    button2.grid(row=5, column=1, pady=10, padx=10, sticky=E)


def Suppdetail_Edit(SuppID):
    right.place(x=220, y=55)
    right1 = Frame(right, bd=2, relief=SOLID, padx=50, pady=50)
    right1.pack()

    def Close():
        right1.destroy()
        Main()
        right.place(x=5000, y=80)

    def Back():
        right1.destroy()
        Main_Mod()
        right.place(x=5000, y=80)

    def Save(tup):
        Update_All(1, tup, us, pas)
        Close()

    def Show(tup0):
        SuppName, SuppAdd, SuppPhone, SuppEmail = tup0
        SuppName = SuppName.title()
        SuppAdd = SuppAdd.title()
        Name.set(SuppName)
        Add.set(SuppAdd)
        eName.config(state='disabled')
        eAdd.config(state='disabled')
        ePhone.config(state='disabled')
        eEmail.config(state='disabled')
        button1.destroy()
        button2.destroy()
        tup = (SuppID, SuppName, SuppAdd, SuppPhone, SuppEmail)

        def OK():
            Save(tup)

        def callback(event):
            OK()

        right1.focus_set()
        right1.bind('<Return>', callback)

        button0 = Button(right1, text="All Ok! Lets save it", bg="brown", fg="white",
                         font=('arial', 14), command=OK)
        button0.grid(row=5, column=0, columnspan=2, pady=10)
        button = Button(right1, text="Cancel", bg="brown", fg="white",
                        font=('arial', 14), command=Close)
        button.grid(row=5, column=1, pady=10, sticky=E)

    def Check():
        phone, email = Phone.get(), Email.get()
        a = 0
        aad = eAdd.get(1.0, END).strip()
        Add.set(aad)
        if email == '':
            pass
        elif '@' not in email or '.' not in email:
            Email.set("")
            eEmail.focus()
            a = 1
        if not phone.isdigit():
            Phone.set("")
            ePhone.focus()
            a = 1
        if a == 1:
            messagebox.showerror("Wrong Format", "Wrong Format\nCheck Again")
        elif a == 0:
            Show(tuple([Name.get(), Add.get(), Phone.get(), Email.get()]))

    ID = StringVar()
    Name = StringVar()
    Add = StringVar()
    Phone = StringVar()
    Email = StringVar()

    demodb = mysql.connect(host="localhost", user=us, passwd=pas, database="projectold")
    cursor = demodb.cursor()
    cursor.execute(f"SELECT * FROM supplier WHERE SuppID='{SuppID}';")
    i = cursor.fetchone()
    ID.set(i[0])
    Name.set(i[1])
    Add.set(i[2])
    Phone.set(i[3])
    Email.set(i[4])
    demodb.close()

    lID = Label(right1, text="Supplier ID", font=("arial", 14))
    lID.grid(row=0, column=0, sticky=W)

    eID = Entry(right1, textvar=ID, state='disabled', font=("arial", 14))
    eID.grid(row=0, column=1, sticky=W, padx=10, pady=10)

    lName = Label(right1, text="Supplier Name", font=("arial", 14))
    lName.grid(row=1, column=0, sticky=W)

    eName = Entry(right1, textvar=Name, font=("arial", 14))
    eName.grid(row=1, column=1, sticky=W, padx=10, pady=10)
    eName.focus()

    lAdd = Label(right1, text="Supplier Address", font=("arial", 14))
    lAdd.grid(row=2, column=0, sticky=W)

    eAdd = Text(right1, width=20, height=3, font=("arial", 14))
    eAdd.grid(row=2, column=1, sticky=W, padx=10, pady=10)
    eAdd.insert(1.0, Add.get())

    lPhone = Label(right1, text="Supplier Phone No.", font=("arial", 14))
    lPhone.grid(row=3, column=0, sticky=W)

    ePhone = Entry(right1, textvar=Phone, font=("arial", 14))
    ePhone.grid(row=3, column=1, sticky=W, padx=10, pady=10)

    lEmail = Label(right1, text="Supplier Email", font=("arial", 14))
    lEmail.grid(row=4, column=0, sticky=W)

    eEmail = Entry(right1, textvar=Email, font=("arial", 14))
    eEmail.grid(row=4, column=1, sticky=W, padx=10, pady=10)

    def callback(event):
        eAdd.focus()

    eName.bind('<Return>', callback)

    def callback(event):
        ePhone.focus()

    eAdd.bind('<Return>', callback)

    def callback(event):
        eEmail.focus()

    ePhone.bind('<Return>', callback)

    def callback(event):
        Check()

    eEmail.bind('<Return>', callback)

    button1 = Button(right1, text="Check", width=7, bg="brown", fg="white",
                     font=('arial', 14), command=Check)
    button1.grid(row=5, column=0, pady=10, columnspan=2, padx=10)
    button3 = Button(right1, text="Back", width=5, bg="brown", fg="white",
                     font=('arial', 14), command=Back)
    button3.grid(row=5, column=0, pady=10, padx=10, sticky=W)
    button2 = Button(right1, text="Exit", width=5, bg="brown", fg="white",
                     font=('arial', 14), command=Close)
    button2.grid(row=5, column=1, pady=10, padx=10, sticky=E)


def Products():
    right.place(x=220, y=35)
    right1 = Frame(right, bd=2, relief=SOLID, padx=50, pady=20)
    right1.pack()

    def Close():
        right1.destroy()
        Main()
        right.place(x=5000, y=80)

    def Back():
        right1.destroy()
        Main_Add()
        right.place(x=5000, y=80)

    def Save(tup1):
        Create(2, tup1, us, pas)
        alist()
        Close()

    def Show(tup0):
        SuppID, ProdID, ProdName, ProdCost, ProdRate, ProdGST, ProdStock, ProdUnit = tup0
        ProdName = ProdName.title()
        ProdUnit = ProdUnit.title()

        Name.set(ProdName)
        Cost.set(ProdCost)
        Rate.set(ProdRate)
        GST.set(ProdGST)
        Unit.set(ProdUnit)
        Stock.set(ProdStock)

        eName.config(state='disabled')
        eCost.config(state='disabled')
        eRate.config(state='disabled')
        eGST.config(state='disabled')
        eUnit.config(state='disabled')
        eStock.config(state='disabled')
        eSID.config(state='disabled')

        button2.destroy()
        button1.destroy()
        tup1 = (SuppID, ProdID, ProdName, ProdCost, ProdRate, ProdGST, ProdUnit, ProdStock)

        def OK():
            Save(tup1)

        def callback(event):
            OK()

        right1.focus_set()
        right1.bind('<Return>', callback)

        button0 = Button(right1, text="All Ok! Lets save it", bg="brown", fg="white",
                         font=('arial', 14), command=OK)
        button0.grid(row=8, column=0, columnspan=2, pady=10)
        button = Button(right1, text="Cancel", bg="brown", fg="white",
                        font=('arial', 14), command=Close)
        button.grid(row=8, column=1, pady=10, sticky=E)
    def Check():
        stock, rate, cost = Stock.get(), Rate.get(), Cost.get()
        a = 0
        SID.set(eSID.get())
        GST.set(eGST.get())
        Unit.set(eUnit.get())
        SuppID = SID.get()[0:3]
        if SuppID == 'Sel':
            a = 1
            eSID.focus()
        gst = GST.get()[0:5]
        if gst == 'Selec':
            a = 1
            eGST.focus()
        if Unit.get() == 'Select Unit':
            a = 1
            eUnit.focus()
        ProdID = prod_gen(SuppID, us, pas)
        ID.set(ProdID)
        if not stock.isdigit():
            Stock.set("")
            eStock.focus()
            a = 1
        try:
            if float(rate):
                pass
        except ValueError:
            Rate.set("")
            eRate.focus()
            a = 1
        try:
            if float(cost):
                pass
        except ValueError:
            Cost.set("")
            eCost.focus()
            a = 1

        if a == 1:
            messagebox.showerror("Wrong Format", "Wrong Format\nCheck Again")
        if a == 0:
            Show(tuple([SuppID, ProdID, Name.get(), Cost.get(), Rate.get(), gst, Stock.get(), Unit.get()]))

    ID = StringVar()
    Name = StringVar()
    Cost = StringVar()
    Rate = StringVar()
    GST = StringVar()
    Unit = StringVar()
    Stock = StringVar()
    SID = StringVar()

    lSID = Label(right1, text="Supplier", font=("arial", 14))
    lSID.grid(row=0, column=0, sticky=W)

    eSID = ttk.Combobox(right1, value=supplst)
    eSID.config(width=18)
    eSID.config(font=("arial", 14))
    eSID.current(0)
    eSID.grid(row=0, column=1, padx=10, pady=10)
    eSID.config(state='readonly')
    eSID.focus()

    lID = Label(right1, text="Product ID", font=("arial", 14))
    lID.grid(row=1, column=0, sticky=W)

    eID = Entry(right1, textvar=ID, state='disabled', font=("arial", 14))
    eID.grid(row=1, column=1, sticky=W, padx=10, pady=10)

    lName = Label(right1, text="Product Name", font=("arial", 14))
    lName.grid(row=2, column=0, sticky=W)

    eName = Entry(right1, textvar=Name, font=("arial", 14))
    eName.grid(row=2, column=1, sticky=W, padx=10, pady=10)

    lCost = Label(right1, text="Product Cost (CP)", font=("arial", 14))
    lCost.grid(row=3, column=0, sticky=W)

    eCost = Entry(right1, textvar=Cost, font=("arial", 14))
    eCost.grid(row=3, column=1, sticky=W, padx=10, pady=10)

    lRate = Label(right1, text="Product Rate (SP)", font=("arial", 14))
    lRate.grid(row=4, column=0, sticky=W)

    eRate = Entry(right1, textvar=Rate, font=("arial", 14))
    eRate.grid(row=4, column=1, sticky=W, padx=10, pady=10)

    lStock = Label(right1, text="Product Stock", font=("arial", 14))
    lStock.grid(row=5, column=0, sticky=W)

    eStock = Entry(right1, textvar=Stock, font=("arial", 14))
    eStock.grid(row=5, column=1, sticky=W, padx=10, pady=10)

    lGST = Label(right1, text="Product GST(%)", font=("arial", 14))
    lGST.grid(row=6, column=0, sticky=W)

    eGST = ttk.Combobox(right1, value=gstlst)
    eGST.current(0)
    eGST.config(width=18)
    eGST.config(font=("arial", 14))
    eGST.grid(row=6, column=1, padx=10, pady=10)
    eGST.config(state='readonly')

    lUnit = Label(right1, text="Product Unit", font=("arial", 14))
    lUnit.grid(row=7, column=0, sticky=W)

    eUnit = ttk.Combobox(right1, value=unitlst)
    eUnit.config(width=18)
    eUnit.current(0)
    eUnit.config(font=("arial", 14))
    eUnit.grid(row=7, column=1, padx=10, pady=10)
    eUnit.config(state='readonly')

    def callback(event):
        eName.focus()

    eSID.bind('<Return>', callback)

    def callback(event):
        eCost.focus()

    eName.bind('<Return>', callback)

    def callback(event):
        eRate.focus()

    eCost.bind('<Return>', callback)

    def callback(event):
        eStock.focus()

    eRate.bind('<Return>', callback)

    def callback(event):
        eGST.focus()

    eStock.bind('<Return>', callback)

    def callback(event):
        eUnit.focus()

    eGST.bind('<Return>', callback)

    def callback(event):
        Check()

    eUnit.bind('<Return>', callback)

    button1 = Button(right1, text="Check", width=7, bg="brown", fg="white",
                     font=('arial', 14), command=Check)
    button1.grid(row=8, column=0, pady=10, columnspan=2, padx=10)
    button3 = Button(right1, text="Back", width=5, bg="brown", fg="white",
                     font=('arial', 14), command=Back)
    button3.grid(row=8, column=0, pady=10, padx=10, sticky=W)
    button2 = Button(right1, text="Exit", width=5, bg="brown", fg="white",
                     font=('arial', 14), command=Close)
    button2.grid(row=8, column=1, pady=10, padx=10, sticky=E)


def Products_Edit(ProdID):
    right.place(x=220, y=35)
    right1 = Frame(right, bd=2, relief=SOLID, padx=50, pady=20)
    right1.pack()

    def Close():
        right1.destroy()
        Main()
        right.place(x=5000, y=80)

    def Back():
        right1.destroy()
        Main_Mod()
        right.place(x=5000, y=80)

    def Save(tup1):
        Update_All(2, tup1, us, pas)
        Close()

    def Show(tup0):
        SuppID, ProdID, ProdName, ProdCost, ProdRate, ProdGST, ProdStock, ProdUnit = tup0
        ProdName = ProdName.title()
        ProdUnit = ProdUnit.title()

        Name.set(ProdName)
        Cost.set(ProdCost)
        Rate.set(ProdRate)
        GST.set(ProdGST)
        Unit.set(ProdUnit)
        Stock.set(ProdStock)

        eName.config(state='disabled')
        eCost.config(state='disabled')
        eRate.config(state='disabled')
        eGST.config(state='disabled')
        eUnit.config(state='disabled')
        eStock.config(state='disabled')
        eSID.config(state='disabled')

        button2.destroy()
        button1.destroy()
        tup1 = (ProdID, ProdName, ProdCost, ProdRate, ProdGST, ProdUnit, ProdStock)

        def OK():
            Save(tup1)

        def callback(event):
            OK()

        right1.focus_set()
        right1.bind('<Return>', callback)

        button0 = Button(right1, text="All Ok! Lets save it", bg="brown", fg="white",
                         font=('arial', 14), command=OK)
        button0.grid(row=8, column=0, columnspan=2, pady=10)
        button = Button(right1, text="Cancel", bg="brown", fg="white",
                        font=('arial', 14), command=Close)
        button.grid(row=8, column=1, pady=10, sticky=E)

    def Check():
        stock, rate, cost = Stock.get(), Rate.get(), Cost.get()
        a = 0
        GST.set(eGST.get())
        Unit.set(eUnit.get())
        SuppID = SID.get()[0:3]
        if SuppID == 'Sel':
            a = 1
            eSID.focus()
        gst = GST.get()[0:5]
        if gst == 'Selec':
            a = 1
            eGST.focus()
        if Unit.get() == 'Select Unit':
            a = 1
            eUnit.focus()
        if not stock.isdigit():
            Stock.set("")
            eStock.focus()
            a = 1
        try:
            if float(rate):
                pass
        except ValueError:
            Rate.set("")
            eRate.focus()
            a = 1
        try:
            if float(cost):
                pass
        except ValueError:
            Cost.set("")
            eCost.focus()
            a = 1

        if a == 1:
            messagebox.showerror("Wrong Format", "Wrong Format\nCheck Again")
        if a == 0:
            Show(tuple([SuppID, ProdID, Name.get(), Cost.get(), Rate.get(), gst, Stock.get(), Unit.get()]))

    ID = StringVar()
    Name = StringVar()
    Cost = StringVar()
    Rate = StringVar()
    GST = StringVar()
    Unit = StringVar()
    Stock = StringVar()
    SID = StringVar()

    demodb = mysql.connect(host="localhost", user=us, passwd=pas, database="projectold")
    cursor = demodb.cursor()
    sql = f"SELECT * FROM product where product.ProdID='{ProdID}';"
    cursor.execute(sql)
    i = cursor.fetchone()
    SID.set(i[0])
    ID.set(i[1])
    Name.set(i[2])
    Cost.set(i[3])
    Rate.set(i[4])
    GST.set(i[5])
    Unit.set(i[6])
    Stock.set(i[7])
    demodb.close()

    lSID = Label(right1, text="Supplier", font=("arial", 14))
    lSID.grid(row=0, column=0, sticky=W)

    eSID = Entry(right1, textvar=SID, state='disabled', font=("arial", 14))
    eSID.grid(row=0, column=1, sticky=W, padx=10, pady=10)

    lID = Label(right1, text="Product ID", font=("arial", 14))
    lID.grid(row=1, column=0, sticky=W)

    eID = Entry(right1, textvar=ID, state='disabled', font=("arial", 14))
    eID.grid(row=1, column=1, sticky=W, padx=10, pady=10)

    lName = Label(right1, text="Product Name", font=("arial", 14))
    lName.grid(row=2, column=0, sticky=W)

    eName = Entry(right1, textvar=Name, font=("arial", 14))
    eName.grid(row=2, column=1, sticky=W, padx=10, pady=10)
    eName.focus()

    lCost = Label(right1, text="Product Cost (CP)", font=("arial", 14))
    lCost.grid(row=3, column=0, sticky=W)

    eCost = Entry(right1, textvar=Cost, font=("arial", 14))
    eCost.grid(row=3, column=1, sticky=W, padx=10, pady=10)

    lRate = Label(right1, text="Product Rate (SP)", font=("arial", 14))
    lRate.grid(row=4, column=0, sticky=W)

    eRate = Entry(right1, textvar=Rate, font=("arial", 14))
    eRate.grid(row=4, column=1, sticky=W, padx=10, pady=10)

    lStock = Label(right1, text="Product Stock", font=("arial", 14))
    lStock.grid(row=5, column=0, sticky=W)

    eStock = Entry(right1, textvar=Stock, font=("arial", 14))
    eStock.grid(row=5, column=1, sticky=W, padx=10, pady=10)

    lGST = Label(right1, text="Product GST(%)", font=("arial", 14))
    lGST.grid(row=6, column=0, sticky=W)

    eGST = ttk.Combobox(right1, value=gstlst)
    for ind, itm in enumerate(gstlst):
        aa = str(GST.get())
        if aa == itm[0:5]:
            eGST.current(ind)
    eGST.config(width=18)
    eGST.config(font=("arial", 14))
    eGST.grid(row=6, column=1, padx=10, pady=10)
    eGST.config(state='readonly')

    lUnit = Label(right1, text="Product Unit", font=("arial", 14))
    lUnit.grid(row=7, column=0, sticky=W)

    eUnit = ttk.Combobox(right1, value=unitlst)
    eUnit.config(width=18)
    for ind, itm in enumerate(unitlst):
        aa = Unit.get()
        if aa == itm[0:4]:
            eUnit.current(ind)
    eUnit.config(font=("arial", 14))
    eUnit.grid(row=7, column=1, padx=10, pady=10)
    eUnit.config(state='readonly')

    def callback(event):
        eCost.focus()

    eName.bind('<Return>', callback)

    def callback(event):
        eRate.focus()

    eCost.bind('<Return>', callback)

    def callback(event):
        eStock.focus()

    eRate.bind('<Return>', callback)

    def callback(event):
        eGST.focus()

    eStock.bind('<Return>', callback)

    def callback(event):
        eUnit.focus()

    eGST.bind('<Return>', callback)

    def callback(event):
        Check()

    eUnit.bind('<Return>', callback)

    button1 = Button(right1, text="Check", width=7, bg="brown", fg="white",
                     font=('arial', 14), command=Check)
    button1.grid(row=8, column=0, pady=10, columnspan=2, padx=10)
    button3 = Button(right1, text="Back", width=5, bg="brown", fg="white",
                     font=('arial', 14), command=Back)
    button3.grid(row=8, column=0, pady=10, padx=10, sticky=W)
    button2 = Button(right1, text="Exit", width=5, bg="brown", fg="white",
                     font=('arial', 14), command=Close)
    button2.grid(row=8, column=1, pady=10, padx=10, sticky=E)


def Bill():
    right.place(x=75, y=65)
    right1 = Frame(right, bd=2, relief=SOLID, padx=20, pady=20)
    right1.pack()
    down = Frame(right1, bd=1, relief=SOLID)
    down.grid(row=1, column=0, sticky=W)
    side = Frame(right1)
    side.grid(row=0, column=1, rowspan=2, sticky=N)
    up = Frame(right1)
    up.grid(row=0, column=0, sticky=W)
    demodb = mysql.connect(host="localhost", user=us, passwd=pas, database="projectold")
    cursor = demodb.cursor()
    time = datetime.now()
    Date = str(time.strftime("%y""%m""%d"))
    cursor.execute(f"SELECT COUNT(BillID) FROM bill WHERE BillID LIKE '%{Date}%';")
    D = cursor.fetchone()[0] + 1
    demodb.close()
    a = [1, 0, 0]

    def Close():
        right1.destroy()
        Main()
        right.place(x=5000, y=80)

    def clock():
        stri = f"Time:      {stime('%I:%M:%S %p')}"
        label.config(text=stri)
        label.after(1000, clock)

    def ProdN(event):
        value = event.widget.get()
        if value == '' or value == 'Select Product':
            data = lst
        else:
            data = []
            for item in lst:
                if value.lower() in item.lower():
                    data.append(item)
        ePName.config(value=data)

    def Add():
        if len(lst) == 0:
            ePName.config(state="disabled")
            return
        Name = ePName.get()
        if ePName.get() == 'Select Product':
            messagebox.showerror("Select Product", "Please Select Product")
            return
        try:
            Qty = int(PQty.get())
        except ValueError:
            messagebox.showerror("No Qty", "Please Enter Product Qty")
            ePqty.focus()
            return
        for id, name in prodname.items():
            if name == Name:
                PID = id
        demodb = mysql.connect(host="localhost", user=us, passwd=pas, database="projectold")
        cursor = demodb.cursor()
        cursor.execute(f"SELECT SP, GST, Unit, Stock FROM product where ProdID='{PID}'")
        aa = cursor.fetchone()
        demodb.close()
        Pa = aa[0] * Qty
        Pgst = (Pa * float(aa[1])) / 100
        Prodtot = round(Pa + Pgst, 2)
        BBtot= Btot.get() + Prodtot
        Btot.set(BBtot)
        eBtot.config(text=f"₹{Btot.get()}")
        tup = (a[0], Name, Qty, aa[0], Prodtot, aa[1], aa[2])
        lst1.append([PID, Qty, Prodtot, a[0]])
        lst2.append(aa[3])
        a[0] += 1
        tv.insert('', 'end', values=tup)
        tv.yview_moveto(1)
        lst.remove(Name)
        ePName.config(value=lst)
        PQty.set('')
        ePName.focus()
        ePName.current(0)

    def Modify():
        if tv.focus() == '':
            return
        selected = tv.focus()
        if a[1] == selected:
            tup = a[2]
            abc = float(tup[4])
            tup[2] = PQty.get()
            lst1[(a[2][0]) - 1][1] = int(tup[2])
            Pa = float(tup[3]) * float(tup[2])
            Pgst = (Pa * float(tup[5])) / 100
            Prodtot = round(Pa + Pgst, 2)
            tup[4] = Prodtot
            BBtot = Btot.get() - abc + Prodtot
            Btot.set(BBtot)
            eBtot.config(text=f"₹{Btot.get()}")
            a[1], a[2] = 0, 1
            PQty.set('')
            tv.item(selected, text="", values=tup)
            button1.config(text='Edit')
            ePqty.bind('<Return>', callback1)
            return

        a[1] = selected
        a[2] = tv.item(selected)['values']
        ab = tv.item(selected)['values']
        PQty.set(ab[2])
        ePqty.focus()
        button1.config(text='Save')

        def callback(event):
            Modify()

        ePqty.bind('<Return>', callback)

    def Remve():
        if tv.focus() == '':
            return
        x = tv.focus()
        aa = tv.item(x)['values']
        ba = int(aa[0]) - 1
        lst.insert(1, aa[1])
        lst1.pop(ba)
        lst2.pop(ba)
        a[0] -= 1
        BBtot = Btot.get() - float(aa[4])
        Btot.set(BBtot)
        eBtot.config(text=f"₹{Btot.get()}")
        ePName.config(value=lst)
        tv.delete(x)

    def Clear():
        global lst
        for item in tv.get_children():
            tv.delete(item)
        lst = ['Select Product']
        for i in prodname.values():
            lst.append(i)
        ePName.config(value=lst)
        PQty.set('')
        Bdic.set('')
        CName.set('')
        Btot.set(0.0)
        eBtot.config(text=f"₹{Btot.get()}")


    def Check():
        if a[0] == 1:
            return
        CustName = CName.get()
        if CustName == '':
            CustName = 'Customer'
        CustID = cust_gen(CustName, us, pas)
        tme = datetime.now()
        BillNos = f'{tme.strftime("%y""%m""%d")}{CustID}-{D}'
        if Bdic.get() == '':
            disc = 0.0
        elif float(Bdic.get()) > 100:
            messagebox.showerror("Negetive Ruprees", "Please Enter discount percentage \nbetween 0 to 100")
            Bdic.set('')
            return
        else:
            disc = float(Bdic.get())
        BillAmt = Btot.get()
        for i in range(0, a[0] - 1):
            lst1[i].insert(0, BillNos)
            stk = lst2[i] - lst1[i][2]
            tup = (lst1[i][1], stk)
            Update_other(1, tup, us, pas)

        BillDisc = round(BillAmt * disc / 100, 2)
        BillNet = BillAmt - BillDisc
        BillDate = f'{tme.strftime("%Y")}-{tme.strftime("%m")}-{tme.strftime("%d")} {tme.strftime("%H:%M:%S")}'

        tup = (BillNos, CustID, CustName, BillDate, a[0] - 1, BillAmt, disc, BillNet)
        Create(3, tup, us, pas)
        for tup1 in lst1:
            Create(4, tup1, us, pas)

        QA = messagebox.askquestion("Print Pdf", f"Bill has been genrated.\nDo you want to print bill?")
        if QA == 'yes':
            PDF(BillNos)
        Clear()

    lst = ['Select Product']
    lst1 = []
    lst2 = []
    for i in prodname.values():
        lst.append(i)
    data = list(lst)

    scroll = Scrollbar(down)
    scroll.pack(side=RIGHT, fill=Y)
    tv = ttk.Treeview(down, columns=('col0', 'col1', 'col2', 'col3', 'col4', 'col5', 'col6'), show='headings',
                      height=10, yscrollcommand=scroll.set, style="mystyle.Treeview")
    tv.pack()
    scroll.config(command=tv.yview)

    tv.heading('col0', text='Sr No.')
    tv.heading('col1', text='Product Name')
    tv.heading('col2', text='Qty')
    tv.heading('col3', text='Rate')
    tv.heading('col4', text='Price')
    tv.heading('col5', text='GST')
    tv.heading('col6', text='Unit')

    tv.column('col0', anchor=CENTER, width=50)
    tv.column('col1', anchor=CENTER, width=150)
    tv.column('col2', anchor=CENTER, width=55)
    tv.column('col3', anchor=CENTER, width=100)
    tv.column('col4', anchor=CENTER, width=100)
    tv.column('col5', anchor=CENTER, width=60)
    tv.column('col6', anchor=CENTER, width=60)

    CName = StringVar()
    PQty = StringVar()
    Bdic = StringVar()
    Btot = DoubleVar()

    label = Label(up, font=("arial", 14))
    label.grid(row=0, column=2, sticky=W, columnspan=2)
    clock()

    lBtot = Label(up, text="Bill Total:", font=("arial", 14))
    lBtot.grid(row=1, column=0, sticky=W)

    eBtot = Label(up, text=f"₹{Btot.get()}", font=("arial", 14))
    eBtot.grid(row=1, column=1, sticky=W, padx=10, pady=10)

    lCName = Label(up, text="Customer Name:", font=("arial", 14))
    lCName.grid(row=0, column=0, sticky=W)

    eCName = Entry(up, textvar=CName, width=18, font=("arial", 14))
    eCName.grid(row=0, column=1, sticky=W, padx=10, pady=10)
    eCName.focus()

    lBdis = Label(up, text="Bill Discount(%):", font=("arial", 14))
    lBdis.grid(row=1, column=2, sticky=W)

    eBdis = Entry(up, textvar=Bdic, width=4, font=("arial", 14))
    eBdis.grid(row=1, column=3, sticky=W, padx=10, pady=10)

    lPName = Label(up, text="Product Name:", font=("arial", 14))
    lPName.grid(row=2, column=0, sticky=W)

    ePName = ttk.Combobox(up, value=data)
    ePName.current(0)
    ePName.configure(width=18, font=("arial", 14))
    ePName.grid(row=2, column=1)
    ePName.bind('<KeyRelease>', ProdN)

    lPqty = Label(up, text="Product Qty.:", font=("arial", 14))
    lPqty.grid(row=2, column=2, sticky=W)

    ePqty = Entry(up, textvar=PQty, width=4, font=("arial", 14))
    ePqty.grid(row=2, column=3, sticky=W, padx=10, pady=10)

    def callback(event):
        ePName.focus()

    eCName.bind('<Return>', callback)

    def callback(event):
        ePqty.focus()

    ePName.bind('<Return>', callback)

    def callback1(event):
        ePName.focus()
        Add()

    ePqty.bind('<Return>', callback1)

    button0 = Button(side, text="Add", width=12, bg="brown", fg="white", font=('arial', 14), command=Add)
    button0.grid(row=0, column=0, sticky=W, pady=10, padx=10)

    button1 = Button(side, text="Edit", width=12, bg="brown", fg="white", font=('arial', 14), command=Modify)
    button1.grid(row=1, column=0, sticky=W, pady=10, padx=10)

    button2 = Button(side, text="Delete", width=12, bg="brown", fg="white", font=('arial', 14), command=Remve)
    button2.grid(row=2, column=0, sticky=W, pady=10, padx=10)

    button3 = Button(side, text="Bill", width=12, bg="brown", fg="white", font=('arial', 14), command=Check)
    button3.grid(row=3, column=0, sticky=W, pady=10, padx=10)

    button3 = Button(side, text="Clear", width=12, bg="brown", fg="white", font=('arial', 14), command=Clear)
    button3.grid(row=4, column=0, sticky=W, pady=10, padx=10)

    button5 = Button(side, text="Cancel", width=12, bg="brown", fg="white", font=('arial', 14), command=Close)
    button5.grid(row=5, column=0, sticky=E, pady=10, padx=10)


def PDF(Bill):
    Pdf(Bill, us, pas)


def View(Type):
    right1 = Frame(right, bd=2, relief=SOLID, padx=50, pady=50)
    right1.pack()
    demodb = mysql.connect(host="localhost", user=us, passwd=pas, database="projectold")
    cursor = demodb.cursor()
    cursor.execute(f"SELECT BillID, Name, Date, Qty, Total FROM bill order by Date")
    bills = list(cursor.fetchall())
    cursor.execute(f"SELECT * FROM supplier")
    supp = list(cursor.fetchall())
    cursor.execute(f"SELECT ProdID, Name, Stock, SP, Hide FROM product")
    prod = list(cursor.fetchall())
    demodb.close()

    if Type == 1:
        right.place(x=145, y=75)
        lst2 = supp
        right2 = LabelFrame(right1, text='Suppliers', bd=1, relief=SOLID)
        right2.grid(row=1, column=0)
        scroll = Scrollbar(right2)
        scroll.pack(side=RIGHT, fill=Y)
        tv = ttk.Treeview(right2, columns=('col0', 'col1', 'col2', 'col3', 'col4', 'col5'),
                          show='headings', height=8, yscrollcommand=scroll.set,
                          selectmode="none", style="mystyle.Treeview")
        tv.pack()
        scroll.config(command=tv.yview)

        tv.heading('col0', text='Id')
        tv.heading('col1', text='Name')
        tv.heading('col2', text='Address')
        tv.heading('col3', text='Phone No.')
        tv.heading('col4', text='Email')
        tv.heading('col5', text='Status')

        tv.column('col0', anchor=CENTER, width=50)
        tv.column('col1', anchor=CENTER, width=100)
        tv.column('col2', anchor=CENTER, width=100)
        tv.column('col3', anchor=CENTER, width=100)
        tv.column('col4', anchor=CENTER, width=100)
        tv.column('col5', anchor=CENTER, width=100)

        for i in lst2:
            i = list(i)
            if i[5] == 'Y':
                i[5] = 'Discontinued'
            elif i[5] == 'N':
                i[5] = 'Active'
            tv.insert('', 'end', values=i)

        def close():
            right1.destroy()
            Main()
            right.place(x=5000, y=80)

        def back():
            right1.destroy()
            Main_View()
            right.place(x=5000, y=80)

        b1 = Button(right1, text='Back', font=('arial', 14), width=12, bg="brown", fg="white", command=back)
        b1.grid(row=3, column=0, sticky=W)
        l1 = Label(right1, text="Suppliers", font=("arial-bold", 25))
        l1.grid(row=0, column=0)
        b2 = Button(right1, text="Close", font=('arial', 14), width=12, bg="brown", fg="white", command=close)
        b2.grid(row=3, column=0, sticky=E)

    elif Type == 2:
        right.place(x=155, y=75)
        lst2 = prod
        right2 = LabelFrame(right1, text='Products', bd=1, relief=SOLID)
        right2.grid(row=1, column=0)
        scroll = Scrollbar(right2)
        scroll.pack(side=RIGHT, fill=Y)
        tv = ttk.Treeview(right2, columns=('col0', 'col1', 'col2', 'col3', 'col4'), show='headings'
                          , height=8, yscrollcommand=scroll.set, style="mystyle.Treeview")
        tv.pack()
        scroll.config(command=tv.yview)

        tv.heading('col0', text='Product ID')
        tv.heading('col1', text='Product Name')
        tv.heading('col2', text='Stock')
        tv.heading('col3', text='SP')
        tv.heading('col4', text='Status')

        tv.column('col0', anchor=CENTER, width=125)
        tv.column('col1', anchor=CENTER, width=175)
        tv.column('col2', anchor=CENTER, width=50)
        tv.column('col3', anchor=CENTER, width=50)
        tv.column('col4', anchor=CENTER, width=100)

        for i in lst2:
            i = list(i)
            if i[4] == 'Y':
                i[4] = 'Discontinued'
            elif i[4] == 'N':
                i[4] = 'Active'
            tv.insert('', 'end', values=i)

        def close():
            right1.destroy()
            Main()
            right.place(x=5000, y=80)

        def back():
            right1.destroy()
            right.place(x=5000, y=80)
            Main_View()

        def back1():
            right1.destroy()
            View(2)

        def detail(tup):
            right.place(x=175, y=80)
            tv.destroy()
            scroll.destroy()
            b3.destroy()
            right2.destroy()
            l1.config(text="Product Details")
            b1.config(command=back1)

            demodb = mysql.connect(host="localhost", user=us, passwd=pas, database="projectold")
            cursor = demodb.cursor()
            cursor.execute(f"SELECT * FROM product where ProdID = '{tup}'")
            bill2 = list(cursor.fetchone())
            demodb.close()

            right3 = Frame(right1)
            right3.grid(row=1, column=0, pady=10)

            a = f'Supplier ID: {bill2[0]}'
            b = f'Product ID: {bill2[1]}'
            c = f'Name: {bill2[2]}'
            d = f'Cost Price(CP): ₹{bill2[3]}'
            e = f'Selling Price(SP): ₹{bill2[4]}'
            f = f'GST: {bill2[5]} %'
            g = f'Unit: {bill2[6]}'
            h = f'Stock: {bill2[7]}'
            if bill2[8] == 'Y':
                bill2[8] = 'Discontinued'
            elif bill2[8] == 'N':
                bill2[8] = 'Active'
            i = f'Status: {bill2[8]}'
            Label(right3, text=a, font=("arial", 14)).grid(row=0, column=0, sticky=W, padx=10)
            Label(right3, text=b, font=("arial", 14)).grid(row=0, column=1, sticky=W, padx=10)
            Label(right3, text=c, font=("arial", 14)).grid(row=1, column=0, sticky=W, padx=10, pady=5)
            Label(right3, text=f, font=("arial", 14)).grid(row=1, column=1, sticky=W, padx=10)
            Label(right3, text=d, font=("arial", 14)).grid(row=2, column=0, sticky=W, padx=10)
            Label(right3, text=e, font=("arial", 14)).grid(row=2, column=1, sticky=W, padx=10)
            Label(right3, text=g, font=("arial", 14)).grid(row=3, column=0, sticky=W, padx=10, pady=5)
            Label(right3, text=i, font=("arial", 14)).grid(row=3, column=1, sticky=W, padx=10)
            Label(right3, text=h, font=("arial", 14)).grid(row=4, column=0, sticky=W, padx=10)

        def ab():
            item = tv.item(tv.focus())
            try:
                item['values'][0]
            except:
                return
            tup = item['values'][0]
            detail(tup)

        def click(event):
            ab()

        tv.bind('<Double 1>', click)
        b1 = Button(right1, text='Back', font=('arial', 14), width=10, bg="brown", fg="white", command=back)
        b1.grid(row=3, column=0, sticky=W)
        l1 = Label(right1, text="Products", font=("arial-bold", 25))
        l1.grid(row=0, column=0)
        b2 = Button(right1, text="Close", font=('arial', 14), width=10, bg="brown", fg="white", command=close)
        b2.grid(row=3, column=0, sticky=E)
        b3 = Button(right1, text="Next", font=('arial', 14), width=10, bg="brown", fg="white", command=ab)
        b3.grid(row=3, column=0)

    elif Type == 3:
        right.place(x=160, y=75)
        lst2 = bills
        right2 = LabelFrame(right1, text='Bills', bd=1, relief=SOLID)
        right2.grid(row=1, column=0)
        scroll = Scrollbar(right2)
        scroll.pack(side=RIGHT, fill=Y)
        tv = ttk.Treeview(right2, columns=('col0', 'col1', 'col2', 'col3', 'col4'), show='headings'
                          , height=8, yscrollcommand=scroll.set, style="mystyle.Treeview")
        tv.pack()
        scroll.config(command=tv.yview)

        tv.heading('col0', text='Bill No.')
        tv.heading('col1', text='Cust. Name')
        tv.heading('col2', text='Bill Date')
        tv.heading('col3', text='No. Items')
        tv.heading('col4', text='Bill Total')

        tv.column('col0', anchor=CENTER, width=100)
        tv.column('col1', anchor=CENTER, width=100)
        tv.column('col2', anchor=CENTER, width=100)
        tv.column('col3', anchor=CENTER, width=100)
        tv.column('col4', anchor=CENTER, width=100)

        for i in lst2:
            i = list(i)
            zz = str(i[2]).split()[0]
            i[2] = zz.split('-')[2] + '/' + zz.split('-')[1] + '/' + zz.split('-')[0]
            tv.insert('', 'end', values=i)

        def close():
            right1.destroy()
            right.place(x=5000, y=80)
            Main()

        def back():
            right1.destroy()
            right.place(x=200, y=50)
            Main_View()

        def back1():
            right1.destroy()
            View(3)

        def detail(tup, tup1):
            right.place(x=100, y=25)
            tv.destroy()
            scroll.destroy()
            b3.destroy()
            l1.config(text="Bill Details")
            right2.config(text='Bill Items')
            b1.config(command=back1)

            demodb = mysql.connect(host="localhost", user=us, passwd=pas, database="projectold")
            cursor = demodb.cursor()
            cursor.execute(f"SELECT * FROM billdetail where BillID = '{tup}'")
            det = cursor.fetchall()
            cursor.execute(f"SELECT * FROM bill where BillID = '{tup}'")
            bill2 = cursor.fetchone()
            demodb.close()

            roll = Scrollbar(right2)
            roll.pack(side=RIGHT, fill=Y)
            ttv = ttk.Treeview(right2, columns=('col0', 'col1', 'col2', 'col3', 'col4'), show='headings',
                               height=8, yscrollcommand=roll.set, style="mystyle.Treeview")
            ttv.pack()
            roll.config(command=ttv.yview)

            ttv.heading('col0', text='Sr No.')
            ttv.heading('col1', text='Product ID')
            ttv.heading('col2', text='Product Name')
            ttv.heading('col3', text='Qty')
            ttv.heading('col4', text='Total')

            ttv.column('col0', anchor=CENTER, width=100)
            ttv.column('col1', anchor=CENTER, width=100)
            ttv.column('col2', anchor=CENTER, width=100)
            ttv.column('col3', anchor=CENTER, width=100)
            ttv.column('col4', anchor=CENTER, width=100)

            for i in det:
                i = list(i)
                a = i.pop()
                i.insert(0, a)
                i[1] = i[2]
                if i[2] in prodname:
                    i[2] = prodname[i[2]]
                ttv.insert('', 'end', values=i)

            right3 = Frame(right1)
            right3.grid(row=2, column=0, pady=10)

            a = f'Bill No.: {bill2[0]}'
            b = f'Customer ID: {bill2[1]}'
            c = f'Customer Name: {bill2[2]}'
            d = f'Date: {tup1}'
            e = f'Discount: {abs(round(bill2[7] - bill2[5], 2))}({bill2[6]}%)'
            f = f'Total: ₹{bill2[7]}'
            Label(right3, text=a, font=("arial", 14)).grid(row=0, column=0, sticky=W)
            Label(right3, text=b, font=("arial", 14)).grid(row=0, column=1, padx=20, pady=5, sticky=W)
            Label(right3, text=d, font=("arial", 14)).grid(row=0, column=2, sticky=W)
            Label(right3, text=c, font=("arial", 14)).grid(row=1, column=0, sticky=W)
            Label(right3, text=e, font=("arial", 14)).grid(row=1, column=1, padx=20, pady=5, sticky=W)
            Label(right3, text=f, font=("arial", 14)).grid(row=1, column=2, sticky=W)

            def aa1():
                PDF(bill2[0])

            b4 = Button(right1, text='Make Bill', font=('arial', 14), width=12, bg="brown", fg="white", command=aa1)
            b4.grid(row=3, column=0)

        def ab():
            item = tv.item(tv.focus())
            try:
                item['values'][0]
            except:
                return
            tup = item['values'][0]
            tup1 = item['values'][2]
            detail(tup, tup1)

        def click(event):
            ab()

        tv.bind('<Double 1>', click)
        b1 = Button(right1, text='Back', font=('arial', 14), width=12, bg="brown", fg="white", command=back)
        b1.grid(row=3, column=0, sticky=W)
        l1 = Label(right1, text="Bills", font=("arial-bold", 25))
        l1.grid(row=0, column=0)
        b2 = Button(right1, text="Close", font=('arial', 14), width=12, bg="brown", fg="white", command=close)
        b2.grid(row=3, column=0, sticky=E)
        b3 = Button(right1, text="Next", font=('arial', 14), width=12, bg="brown", fg="white", command=ab)
        b3.grid(row=3, column=0)


def Main_Add():
    left2 = Frame(window, bd=2, relief=SOLID, padx=50, pady=50)
    left2.place(x=350, y=80)

    def Close():
        left2.destroy()

    def Close1():
        left2.destroy()
        Main()
        right.place(x=5000, y=80)

    def Supp():
        Close()
        Suppdetail()

    def Prod():
        Close()
        Products()

    b1 = Button(left2, text="Supplier", width=12, bg="brown", fg="white", font=('arial', 14), command=Supp)
    b1.grid(row=1, column=0, padx=10, pady=10)

    b2 = Button(left2, text="Product", width=12, bg="brown", fg="white", font=('arial', 14), command=Prod)
    b2.grid(row=2, column=0, padx=10, pady=10)

    b3 = Label(left2, text="New", font=("arial-bold", 25))
    b3.grid(row=0, column=0, padx=10, pady=10)

    b4 = Label(left2, text=" ", font=("arial", 14))
    b4.grid(row=4, column=0, padx=10, pady=11)

    b5 = Button(left2, text="Exit", width=12, bg="brown", fg="white", font=('arial', 14), command=Close1)
    b5.grid(row=5, column=0, padx=10, pady=10)


def Main_Mod():
    left2 = Frame(window, bd=2, relief=SOLID, padx=50, pady=50)
    left2.place(x=350, y=50)

    def Close():
        left2.destroy()

    def Close1():
        left2.destroy()
        Main()
        right.place(x=5000, y=80)

    def back():
        left2.destroy()
        Main_Mod()

    def Supp():
        left2.place(x=350, y=80)
        b2.destroy()
        b1.destroy()
        b3.destroy()
        b4.destroy()
        Label(left2, text="Supplier", font=("arial bold", 20)).grid(row=0, column=0)
        SID = StringVar()

        def Check():
            if eSID.get() == 'Select Supplier':
                messagebox.showerror("Wrong Format", "Select Supplier")
                return
            else:
                SID.set(eSID.get())
                SuppID = SID.get()[0:3]
                Close()
                Suppdetail_Edit(SuppID)

        eSID = ttk.Combobox(left2, value=supplst)
        eSID.config(width=12)
        eSID.config(font=("arial", 14))
        eSID.current(0)
        eSID.grid(row=2, column=0, pady=20)
        eSID.config(state='readonly')
        eSID.focus()

        b6 = Button(left2, text="Proceed", width=12, bg="brown", fg="white", font=('arial', 14), command=Check)
        b6.grid(row=3, column=0, padx=10, pady=10)

        b7 = Button(left2, text="Back", width=12, bg="brown", fg="white", font=('arial', 14), command=back)
        b7.grid(row=4, column=0, padx=10, pady=10)

        def callback(event):
            Check()

        eSID.bind('<Return>', callback)

    def Prod():
        left2.place(x=350, y=80)
        b1.destroy()
        b2.destroy()
        b3.destroy()
        b4.destroy()
        Label(left2, text="Product", font=("arial bold", 20)).grid(row=0, column=0)
        SID = StringVar()

        def Check():
            if eSID.get() == 'Select Product':
                messagebox.showerror("Wrong Format", "Select Product")
                return
            else:
                SID.set(eSID.get())
                ProdID = SID.get()[0:6]
                Close()
                Products_Edit(ProdID)

        eSID = ttk.Combobox(left2, value=prodlst)
        eSID.config(width=12)
        eSID.config(font=("arial", 14))
        eSID.current(0)
        eSID.grid(row=2, column=0, pady=20)
        eSID.config(state='readonly')
        eSID.focus()

        b6 = Button(left2, text="Proceed", width=12, bg="brown", fg="white", font=('arial', 14), command=Check)
        b6.grid(row=3, column=0, padx=10, pady=10)

        b7 = Button(left2, text="Back", width=12, bg="brown", fg="white", font=('arial', 14), command=back)
        b7.grid(row=4, column=0, padx=10, pady=10)

        def callback(event):
            Check()

        eSID.bind('<Return>', callback)

    def Delsupp():
        right.place(x=145, y=80)
        Close()
        right1 = Frame(right, bd=2, relief=SOLID, padx=50, pady=50)
        right1.pack()
        demodb = mysql.connect(host="localhost", user=us, passwd=pas, database="projectold")
        cursor = demodb.cursor()
        cursor.execute(f"SELECT * FROM supplier")
        lst2 = list(cursor.fetchall())
        demodb.close()
        right2 = LabelFrame(right1, text='Suppliers', bd=1, relief=SOLID)
        right2.grid(row=1, column=0)
        scroll = Scrollbar(right2)
        scroll.pack(side=RIGHT, fill=Y)
        tv = ttk.Treeview(right2, columns=('col0', 'col1', 'col2', 'col3', 'col4', 'col5'),
                          show='headings', height=8, yscrollcommand=scroll.set, style="mystyle.Treeview")
        tv.pack()
        scroll.config(command=tv.yview)

        tv.heading('col0', text='Id')
        tv.heading('col1', text='Name')
        tv.heading('col2', text='Address')
        tv.heading('col3', text='Phone No.')
        tv.heading('col4', text='Email')
        tv.heading('col5', text='Status')

        tv.column('col0', anchor=CENTER, width=50)
        tv.column('col1', anchor=CENTER, width=100)
        tv.column('col2', anchor=CENTER, width=100)
        tv.column('col3', anchor=CENTER, width=100)
        tv.column('col4', anchor=CENTER, width=100)
        tv.column('col5', anchor=CENTER, width=100)

        for i in lst2:
            i = list(i)
            if i[5] == 'Y':
                i[5] = 'Discontinued'
            elif i[5] == 'N':
                i[5] = 'Active'
            tv.insert('', 'end', values=i)

        def close():
            right1.destroy()
            Main()
            right.place(x=5000, y=80)

        def ab():
            item = tv.item(tv.focus())['values']
            try:
                item[0]
            except:
                return 0
            if item[5] == 'Discontinued':
                item[5] = 0
            elif item[5] == 'Active':
                item[5] = 1
            tup = (item[0], item[5])
            Update_other(2, tup, us, pas)
            alist()
            if item[5] == 1:
                item[5] = 'Discontinued'
            elif item[5] == 0:
                item[5] = 'Active'
            selected = tv.focus()
            tv.item(selected, text="", values=item)

        def click(event):
            ab()

        tv.bind('<Double 1>', click)

        def back():
            left2.destroy()
            right1.destroy()
            Main_Mod()

        b1 = Button(right1, text='Back', font=('arial', 14), width=12, bg="brown", fg="white", command=back)
        b1.grid(row=3, column=0, sticky=W)
        l1 = Label(right1, text="Change Supplier Status", font=("arial-bold", 25))
        l1.grid(row=0, column=0)
        b2 = Button(right1, text="Close", font=('arial', 14), width=12, bg="brown", fg="white", command=close)
        b2.grid(row=3, column=0, sticky=E)
        b3 = Button(right1, text="Change Status", font=('arial', 14), width=12, bg="brown", fg="white", command=ab)
        b3.grid(row=3, column=0)

    def Delprod():
        right.place(x=200, y=80)
        Close()
        right1 = Frame(right, bd=2, relief=SOLID, padx=50, pady=50)
        right1.pack()
        demodb = mysql.connect(host="localhost", user=us, passwd=pas, database="projectold")
        cursor = demodb.cursor()
        cursor.execute(f"SELECT ProdID, Name, Stock, SP, Hide FROM product")
        lst2 = list(cursor.fetchall())
        demodb.close()
        right2 = LabelFrame(right1, text='Suppliers', bd=1, relief=SOLID)
        right2.grid(row=1, column=0)
        scroll = Scrollbar(right2)
        scroll.pack(side=RIGHT, fill=Y)
        tv = ttk.Treeview(right2, columns=('col0', 'col1', 'col2', 'col3', 'col4'),
                          show='headings', height=8, yscrollcommand=scroll.set, style="mystyle.Treeview")
        tv.pack()
        scroll.config(command=tv.yview)

        tv.heading('col0', text='Id')
        tv.heading('col1', text='Name')
        tv.heading('col2', text='Stock')
        tv.heading('col3', text='SP')
        tv.heading('col4', text='Status')

        tv.column('col0', anchor=CENTER, width=125)
        tv.column('col1', anchor=CENTER, width=175)
        tv.column('col2', anchor=CENTER, width=50)
        tv.column('col3', anchor=CENTER, width=100)
        tv.column('col4', anchor=CENTER, width=100)

        for i in lst2:
            i = list(i)
            if i[4] == 'Y':
                i[4] = 'Discontinued'
            elif i[4] == 'N':
                i[4] = 'Active'
            tv.insert('', 'end', values=i)

        def close():
            right1.destroy()
            Main()
            right.place(x=5000, y=80)

        def ab():
            item = tv.item(tv.focus())['values']
            try:
                item[0]
            except:
                return 0
            if item[4] == 'Discontinued':
                item[4] = 0
            elif item[4] == 'Active':
                item[4] = 1
            tup = (item[0], item[4])
            Update_other(3, tup, us, pas)
            alist()
            if item[4] == 1:
                item[4] = 'Discontinued'
            elif item[4] == 0:
                item[4] = 'Active'
            selected = tv.focus()
            tv.item(selected, text="", values=item)

        def click(event):
            ab()

        tv.bind('<Double 1>', click)

        def back():
            left2.destroy()
            right1.destroy()
            Main_Mod()

        b1 = Button(right1, text='Back', font=('arial', 14), width=12, bg="brown", fg="white", command=back)
        b1.grid(row=3, column=0, sticky=W)
        l1 = Label(right1, text="Change Product Status", font=("arial-bold", 25))
        l1.grid(row=0, column=0)
        b2 = Button(right1, text="Close", font=('arial', 14), width=12, bg="brown", fg="white", command=close)
        b2.grid(row=3, column=0, sticky=E)
        b3 = Button(right1, text="Change Status", font=('arial', 14), width=12, bg="brown", fg="white", command=ab)
        b3.grid(row=3, column=0)

    b1 = Button(left2, text="Supplier", width=12, bg="brown", fg="white", font=('arial', 14), command=Supp)
    b1.grid(row=1, column=0, padx=10, pady=10)

    b2 = Button(left2, text="Product", width=12, bg="brown", fg="white", font=('arial', 14), command=Prod)
    b2.grid(row=2, column=0, padx=10, pady=10)

    b3 = Button(left2, text="Supplier Status", width=12, bg="brown", fg="white",
                font=('arial', 14), command=Delsupp)
    b3.grid(row=3, column=0, padx=10, pady=10)

    b4 = Button(left2, text="Product Status", width=12, bg="brown", fg="white",
                font=('arial', 14), command=Delprod)
    b4.grid(row=4, column=0, padx=10, pady=10)

    b6 = Label(left2, text="Modify", font=("arial-bold", 25))
    b6.grid(row=0, column=0)

    b5 = Button(left2, text="Exit", width=12, bg="brown", fg="white", font=('arial', 14), command=Close1)
    b5.grid(row=5, column=0, padx=10, pady=10)


def Main_Bill():
    Bill()


def Main_View():
    left2 = Frame(window, bd=2, relief=SOLID, padx=50, pady=50)
    left2.place(x=350, y=80)

    def Close():
        left2.destroy()
        right.place(x=5000, y=80)
        Main()

    def cc():
        left2.destroy()
        View(1)

    def cc1():
        left2.destroy()
        View(2)

    def cc2():
        left2.destroy()
        View(3)

    b1 = Button(left2, text="Supplier", width=12, bg="brown", fg="white",
                font=('arial', 14), command=cc)
    b1.grid(row=1, column=0, padx=10, pady=10)

    b2 = Button(left2, text="Product", width=12, bg="brown", fg="white",
                font=('arial', 14), command=cc1)
    b2.grid(row=2, column=0, padx=10, pady=10)

    b3 = Button(left2, text="Bills", width=12, bg="brown", fg="white",
                font=('arial', 14), command=cc2)
    b3.grid(row=3, column=0, padx=10, pady=10)

    b5 = Button(left2, text="Exit", width=12, bg="brown", fg="white",
                font=('arial', 14), command=Close)
    b5.grid(row=4, column=0, padx=10, pady=10)

    b3 = Label(left2, text="View", font=("arial-bold", 25))
    b3.grid(row=0, column=0)


def Main():
    left0 = Frame(left, bd=2, relief=SOLID, padx=50, pady=50)
    left0.pack()
    left.place(x=350, y=100)
    l = Label(window, text="A. Somasundara Nadar & Co.", bg='Yellow', font=("arial-bold", 25))
    l.place(x=300, y=25)

    def aa():
        left0.destroy()
        Main_Add()
        l.destroy()

    def bb():
        left0.destroy()
        Main_Mod()
        l.destroy()

    def cc():
        left0.destroy()
        Main_Bill()
        l.destroy()

    def dd():
        left0.destroy()
        Main_View()
        l.destroy()

    b0 = Button(left0, text="Add", width=12, bg="brown", fg="white",
                font=('arial', 14), command=aa)
    b0.grid(row=0, column=0, padx=10, pady=10)
    b1 = Button(left0, text="Modify", width=12, bg="brown", fg="white",
                font=('arial', 14), command=bb)
    b1.grid(row=1, column=0, padx=10, pady=10)
    b3 = Button(left0, text="View", width=12, bg="brown", fg="white",
                font=('arial', 14), command=dd)
    b3.grid(row=2, column=0, padx=10, pady=5)
    b2 = Button(left0, text="Billing", width=12, bg="brown", fg="white",
                font=('arial', 14), command=cc)
    b2.grid(row=3, column=0, padx=10, pady=10)
    b4 = Button(left0, text="Exit", width=12, bg="brown", fg="white",
                font=('arial', 14), command=exit_prog)
    b4.grid(row=4, column=0, padx=10, pady=5)


window = Tk()
window.title('Bill System')
window.geometry("960x540")
window.iconbitmap(r'modules/1.ico')
window.focus_force()
window.resizable(False, False)
window.config(bg='yellow')

menu = Menu(window)
window.config(menu=menu)
sm0 = Menu(menu, tearoff=0)
sm0.add_command(label="Repair", command=Ins.install_Old)
sm0.add_command(label="Bulk Entry", command=sql_csv_imp)
sm0.add_command(label="Export Database", command=sql_csv_exp)
sm0.add_separator()
sm0.add_command(label="Help", command=Helpwind)
sm0.add_command(label="Exit", command=exit_prog)
menu.add_cascade(label="Options", menu=sm0)

left = Frame(window, bg='yellow')
left.place(x=50, y=80)
right = Frame(window, bg='yellow')
right.place(x=5000, y=0)
window.protocol("WM_DELETE_WINDOW", exit_prog)
style = ttk.Style()
style.configure("mystyle.Treeview.Heading", font=("arial", 10, 'bold'))
style.configure("mystyle.Treeview", font=("arial", 10))
Main()

try:
    if pas == '':
        window.destroy()
        raise SystemExit
    else:
        demodb = mysql.connect(host="localhost", user=us, passwd=pas, database="projectold")
        cursor = demodb.cursor()
        cursor.execute('SELECT * FROM supplier;')
        demodb.close()
except mysql.errors.ProgrammingError:
    sql_data_create()

alist()

window.mainloop()
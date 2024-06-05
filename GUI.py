# GUI Source Code

""" Import Section """
import modules.Install as Ins
Ins.install()
try:
    from modules.SQL_IDGenrate import supp_gen, prod_gen, cust_gen
except:
    raise SystemExit
from modules.SQL_Update import Update_row, Update_column
from modules.SQL_Entry import Create
from modules.SQL_Check import Check_Database
from time import strftime as stime
import mysql.connector as mysql
from tkinter import messagebox
import modules.SQL_Pass as Pas
from datetime import datetime
from modules.PDF import Pdf
from tkinter import ttk
from tkinter import *


""" Constants """
# pas, us = 'Ramsour1_2003', 'root'
pas, us = Pas.Pass()
bgcol:str = "#add8e6"
text_format:tuple = ("arial", 14)
unitlst:tuple = ('Select Unit', 'Kgs', 'Nos')
button_format:dict = {"bg":"brown", "fg":"white", "font":text_format}
DB:dict[str,str] = {"user": us, "passwd": pas, "database": "project", "host": "localhost"}
gstlst:tuple = ('Select GST Rate', '00.00 %', '05.00 %', '12.00 %', '18.00 %', '28.00 %')

""" Working Lists/Dicts """
supplst: list[str] = [] # To select supplier in product Add
prodlst: list[str] = [] # To show product in Bill
custlst: list[str] = [] # To show customer in Bill
prodname:dict = {} # {PID:Name} To Display in modify screen
suppname:dict = {} # {SID:Name} To Display in modify screen
prodqty:dict = {}  # {PID:Qty}  To Check Avaible Stock


""" Other Functions """
def Search(): # Search Window
    return None

def Helpwind(): # Help Window
    import modules.Help
    modules.Help.Help()

def sql_data_create(): # Create database
    from modules.SQL_Datacreate import SQL
    SQL(us, pas)
    sql_csv()
    Update_lst(4)

def exit_prog(): # Exit Program
    ask_exit = messagebox.askquestion("Exit", "Do You Want To Exit Application ?")
    if ask_exit == 'yes':
        window.destroy()
    else:
        pass

def printf(filename): # Print Bills
    import os
    os.startfile(filename, 'print')

def PDF(Bill): # Genrate Bill
    Pdf(Bill, us, pas)

def sql_csv(): # Genrate CSV File
    cc = messagebox.askquestion("Bulk Data Entry", "Do you want to add Data from file?")
    if cc == 'yes':
        window1 = Tk()
        window1.title('Bulk Data Entry')
        window1.config(bg=bgcol)
        window1.focus_force()
        window1.iconbitmap(r'modules/1.ico')
        import modules.SQL_CSV as SQL0

        def imp():
            SQL0.Read_csv(us, pas)
            Update_lst(4)
            window1.destroy()

        def cancel():
            SQL0.Delfile()
            window1.destroy()

        SQL0.New_csv()
        
        from os import startfile as strfile
        strfile("Details.csv")

        f = f"\nFile Created. Now Enter Data and click on Import Data when done."
        lab = Label(window1, text=f, bg=bgcol, font=text_format)
        lab.pack(padx=20)
        f = f"Only Supplier name is required for multiple products of same supplier."
        lab1 = Label(window1, text=f, bg=bgcol, font=text_format)
        lab1.pack(pady=10, padx=20)
        button0 = Button(window1, text="Import Data", **button_format, command=imp)
        button0.pack(padx=10)
        button1 = Button(window1, text="Cancel Import", **button_format, command=cancel)
        button1.pack(pady=10, padx=10)

def Update_lst(what): # Genrate Alpha List
    demodb = mysql.connect(**DB)
    cursor = demodb.cursor()
    
    global supplst, prodlst, prodname, suppname, prodqty, custlst
    prodname = {}
    prodqty = {}
    prodlst = ['Select Product']
    supplst = ['Select Supplier']
    custlst = ['Select/Type Name']
    
    if what==1: # supplier
        cursor.execute(f"SELECT SuppID,SuppName FROM supplier where Hide='N'")
        supplier = list(cursor.fetchall())
        for i in supplier:
            ABC = f'{i[0]} - {i[1]}'
            suppname[i[0]] = i[1]
            supplst.append(ABC)
    elif what==2: # product
        cursor.execute(f"SELECT ProdID,Name FROM product where Hide='N'")
        product = list(cursor.fetchall())
        for i in product:
            prodname[i[0]] = i[1]
    elif what==3: # bill
        cursor.execute(f"select Name from product where Stock>0")
        bill = list(cursor.fetchall())
        for i in bill:
            prodlst.append(i[0])
    elif what==5: # Product Qty
        cursor.execute(f"select ProdID, Stock from product where Stock>0")
        Qty = list(cursor.fetchall())
        for i in Qty:
            prodqty[i[0]] = i[1]
    elif what==6: # Customer Name
        cursor.execute(f"select Name from cust")
        cust = list(cursor.fetchall())
        for i in cust:
            custlst.append(i[0])
    elif what==4: # All
        cursor.execute(f"SELECT SuppID,SuppName FROM supplier where Hide='N'")
        supplier = list(cursor.fetchall())
        for i in supplier:
            ABC = f'{i[0]} - {i[1]}'
            suppname[i[0]] = i[1]
            supplst.append(ABC)
        cursor.execute(f"SELECT ProdID,Name FROM product where Hide='N'")
        product = list(cursor.fetchall())
        for i in product:
            prodname[i[0]] = i[1]
        cursor.execute(f"select Name from product where Stock>0")
        bill = list(cursor.fetchall())
        for i in bill:
            prodlst.append(i[0])
        cursor.execute(f"select ProdID, Stock from product where Stock>0")
        Qty = list(cursor.fetchall())
        for i in Qty:
            prodqty[i[0]] = i[1]
        cursor.execute(f"select Name from cust")
        cust = list(cursor.fetchall())
        for i in cust:
            custlst.append(i[0])
        
    demodb.close()

def Main(): # Home Screen
    option = {1: Main_Add, 2: Main_Mod, 3: Bill, 4: Main_View}

    right.grid(column=0,row=1,padx=0,pady=0)
    right0 = Frame(right, bd=2, relief=SOLID, padx=50, pady=50)
    right0.pack(pady=20)
    lab = Label(window, text="A. Somasundara Nadar & Co.", bg=bgcol, font=("arial-bold", 25))
    lab.grid(column=0,row=0,ipadx=275,ipady=20)
    
    def Comon(v):
        right0.destroy()
        dictt = option.get(v)
        dictt()
        lab.destroy()

    b0 = Button(right0, text="Add", width=12, **button_format, command=lambda *args: Comon(1))
    b0.grid(row=0, column=0, padx=10, pady=10)
    b1 = Button(right0, text="Modify", width=12, **button_format, command=lambda *args: Comon(2))
    b1.grid(row=1, column=0, padx=10, pady=10)
    b3 = Button(right0, text="View", width=12, **button_format, command=lambda *args: Comon(4))
    b3.grid(row=2, column=0, padx=10, pady=5)
    b2 = Button(right0, text="Bill", width=12, **button_format, command=lambda *args: Comon(3))
    b2.grid(row=3, column=0, padx=10, pady=10)
    b4 = Button(right0, text="Exit", **button_format, width=12, command=exit_prog)
    b4.grid(row=4, column=0, padx=10, pady=5)

def Bill(): # Billing mode
    right.place(x=75, y=35)
    right1 = Frame(right, bd=2, relief=SOLID, padx=20, pady=20)
    right1.pack()
    down = Frame(right1, bd=1, relief=SOLID)
    down.grid(row=1, column=1, sticky=W, pady=5)
    side = Frame(right1)
    side.grid(row=0, column=0, rowspan=2)
    up = Frame(right1)
    up.grid(row=0, column=1, sticky=W)

    sel = None
    sel_tup = None
    Bal = DoubleVar()  # Bill Ballance
    Qty = StringVar()  # Product Qty
    Typ = StringVar()  # Bill Payment Type
    Adv = StringVar()  # Bill Pay in Advance
    Total = DoubleVar()  # Bill After Dicount
    Dis_ru = StringVar()  # Discount ₹
    data = list(prodlst)  # Product Name Working
    b_items = [] # Bill items in dict form -> {ProdID:(ProdName,Qty,Gst,Unit,Rate,Price)}
    Dis_per = StringVar()  # Discount %
    Pname = list(prodlst) # Product Name main
    Typ.set('Full')

    """ Other Interface """
    def Clear(): # Clear Interface
        right1.destroy()
        Bill()

    def Close(): # Close Interface
        right1.destroy()
        Main()

    def clock(): # Clock Function
        stri = f"Time:\t{stime('%I:%M:%S %p')}"
        label.config(text=stri)
        label.after(1000, clock)

    def Custdrop(): # Custname DropBox
        eCName.event_generate ('<Down>', when='head')

    def Proddrop(): # Prodname DropBox
        ePName.event_generate ('<Down>', when='head')
    
    """ CallBack Function """
    def Next_Prod(event):
        ePName.focus()

    def Next_Qty(event):
        eQty.focus()
        
    def Next_Prod1(event):
        ePName.focus()
        Add()

    def Next_dis(event):
        eBdis_r.focus()

    def Adv_pay(event):
        val = float(Adv.get())
        btotal = Total.get()

        if not val:
            val='0.0'

        if Total.get()<float(val):
            messagebox.showerror("Negetive Ruprees", "Please Enter advance less than total !!!!")
            Adv.set('')
            return

        if Total.get()!=0.0:
            btotal = round(btotal-float(val),2)
        
        Bal.set(btotal)
        eBtot.configure(text=f"₹{Bal.get()}")
        Check()

    def Next_Modify(event):
        Modify()

    def Or_Dis_p(event):
        Dis_ru.set('')
        eBdis_p.focus()

    def Or_Dis_r(event):
        Dis_per.set('')
        eBdis_r.focus()
    
    def Dis_perc(event):
        val = Dis_per.get()

        if not val:
            val='0.0'

        if float(val)>100.0:
            messagebox.showerror("Negetive Ruprees", "Please Enter discount(%) between 0 to 100 !!!!")
            Dis_per.set('')
            return
        
        if Total.get()!=0.0:
            Discount(1,val)
        Credit()
        eType1.focus()

    def Dis_rup(event):
        val = Dis_ru.get()

        if not val:
            val='0.0'

        if Total.get()<float(val):
            messagebox.showerror("Negetive Ruprees", "Please Enter discount(₹) less than total !!!!")
            Dis_ru.set('')
            return

        if Total.get()!=0.0:
            Discount(2,val)
        
        Credit()
        eType1.focus()

    """ Calculate """
    def ProdN(event): # Prodname search
        value = ePName.get()
        nonlocal Pname
        if value == '' or value == 'Select Product':
            data = Pname
        else:
            data = []
            for item in Pname:
                if value.lower() in item.lower():
                    data.append(item)
        ePName.config(values=data)
        ePName.after(750,Proddrop)
        
    def CustN(event): # Custname search
        value:str = eCName.get()
        if value == '':
            eCName.config(values=custlst)
        else:
            CName = []
            for item in custlst:
                if value.lower() in item.lower():
                    CName.append(item)
            CName.insert(0,value)
            eCName.config(values=CName)

    def Discount(typ:int,val:str|float): # Calculate discount
        val = float(val)
        btotal = Total.get()
        if typ==1: #calc %
            dis_ru = str(round((val/100)*btotal,2))
            btotal=round(btotal-float(dis_ru),2)
            Dis_ru.set(dis_ru)

        else: #calc ₹
            dis_per = str(round((val*100)/btotal,2))
            btotal=round(btotal-val,2)
            Dis_per.set(dis_per)
        
        Total.set(btotal)
        eBnet.configure(text=f"₹{Total.get()}")

    def Credit(): # Credit
        if Typ.get() == "Full" :
            eType1.config(bg='light gray')
            eType2.config(bg='SystemButtonFace')
            Adv.set("")
            ePay.config(state="disabled")
        else:
            eType1.config(bg='SystemButtonFace')
            eType2.config(bg='light gray')
            ePay.config(state="normal")
            ePay.focus()

    """ Side Panel """
    def Add(): # Add Element
        # Preprocessing Part
        if ePName.get() == 'Select Product':
            messagebox.showerror("Select Product", "Please Select Product")
            return
        try:
            int(eQty.get())
        except ValueError:
            messagebox.showerror("No Qty", "Please Enter Product Qty")
            eQty.focus()
            return
        pid:str = ""
        name:str = ePName.get()
        for ppid, pname in prodname.items():
            if pname == name:
                pid = ppid  # Product ID
        qty:int = int(eQty.get())
        stk = Check_Database(1,(pid,qty),us,pas)
        if not stk[0]:
            messagebox.showerror("Insuffient Stock", f"You dont have enough stock of {name}.\n Stock Availble = {stk[1]}")
            eQty.focus()
            Qty.set('')
            return
        stk = stk[1]
        
        # Processing Part
        demodb = mysql.connect(**DB)
        cursor = demodb.cursor()
        cursor.execute(f"SELECT GST, Unit, SP FROM product where ProdID='{pid}'")
        det = cursor.fetchone()
        demodb.close()
        price = round((det[2]*qty)+((det[2]*qty)*(float(det[0]))/100),2)
        tup = (name,qty,det[0],det[1],det[2],price)
        
        # Postprocessing Part
        b_items.append({pid:tup})
        tv.insert('', 'end', values=tup)  # For Display Table
        tv.yview_moveto(1)
        Total.set(Total.get()+price)
        eBnet.configure(text=f"₹{Total.get()}")
        Qty.set("")
        Pname.remove(name)
        ePName.config(values=Pname)
        ePName.current(0)
    
    def Delete(): # Remove Element
        if tv.focus() == '':
            return

        x = tv.focus()
        aa = tv.item(x)['values']  # (Name,qty,gst,unit,rate,price)
        name, qty, gst, unit, sp, price = aa
        sp = float(sp)
        price = float(price)
        pid = ''

        for ppid, pname in prodname.items():
            if pname == name:
                pid = ppid
                break
        b_items.remove({pid: (name, qty, gst, unit, sp, price)})
        
        Total.set(Total.get() - float(price))
        eBnet.configure(text=f"₹{Total.get()}")

        Pname.append(name)
        ePName.config(values=Pname)
        ePName.current(0)
        tv.delete(x)

    def Modify(): # Edit Qty
        if tv.focus() == '':
            return

        nonlocal sel,sel_tup
        select = tv.focus()

        if sel!=select: # Modified
            sel = select
            sel_tup = tv.item(select)['values']  # (Name,qty,gst,unit,rate,price)
            Qty.set(sel_tup[1])
            button1.config(text='Save Edit')
            eQty.focus()
            eQty.bind('<Return>', Next_Modify)
            return
        
        sp = float(sel_tup[4])
        gst = float(sel_tup[2])
        new = int(Qty.get())
        old_price = float(sel_tup[5])
        pid = ""

        for ppid, pname in prodname.items():
            if pname == sel_tup[0]:
                pid = ppid
                break

        stk = Check_Database(1, (pid, new), us, pas)
        if not stk[0]:
            messagebox.showerror("Insufficient Stock", f"Not enough stock of {new}.\nAvailable stock = {stk[1]}")
            return
        
        sel_tup[5] = float(sel_tup[5])
        sel_tup[4] = float(sel_tup[4])
        index = b_items.index({pid:tuple(sel_tup)})
        sel_tup[1] = new
        new_price = round((sp * new) + ((sp * new) * (gst) / 100), 2)
        sel_tup[5] = new_price

        b_items[index] = {pid:tuple(sel_tup)}
        tv.item(sel, text="", values=sel_tup)
        Total.set((Total.get()-old_price)+new_price)
        eBnet.configure(text=f"₹{Total.get()}")
        button1.config(text='Edit Qty')
        eQty.bind('<Return>', Next_Prod1)
        ePName.focus()
        return

    def Check(): # Check Before Billing
        cc = messagebox.askquestion("Procced to Bill","Procced to Bill?")
        if cc == 'no':
            return

        # # Preprocessing part
        CustName = eCName.get()
        if CustName == '' or CustName == 'Select/Type Name':
            messagebox.showerror("Unknown Customer", "Please Enter Customer Name")
            eCName.focus()
            return
        
        if CustName not in custlst:
            cid = cust_gen(CustName, us, pas)
            count = 0
        else:
            cid,count = Check_Database(2,(CustName,stime('%Y-%m-%d')),us,pas)
            count += 1
        
        BillDate = f'{stime("%Y-%m-%d %H:%M:%S")}'
        balance = Bal.get()
        total = Total.get()
        b_to_pay = total-balance-float(Adv.get())
        Type = 'Cash' if Typ.get()=="Full" else 'Credit'

        # Processing part
        if count == 0:
            Create(5,(cid,CustName,1,balance,total),us,pas)
            count=1
            BillNos = f'{stime('%y%m%d')}{cid}-{count}'
        else:
            Update_column(4,(cid,balance,total),us,pas)
            BillNos = f'{stime('%y%m%d')}{cid}-{count}'

        Create(3,(BillNos,cid,Type,BillDate,len(b_items),b_to_pay,Dis_per.get(),total,balance),us,pas)

        count=1
        for i in b_items: # i = {ProdID:(ProdName,Qty,Gst,Unit,Rate,Price)}
            pid,tup = list(i.items())[0]
            Update_column(1,(pid,tup[1]),us,pas)
            Create(4,(BillNos,pid,tup[1],tup[5],count),us,pas)
            count+=1
        
        PDF(BillNos)

        # Postprocessing part
        QA = messagebox.askquestion("Print Pdf", f"Bill has been genrated.\nDo you want to print bill?")
        if QA == 'yes':
            filename = str(f'Bills\\Invoice {a[3]}.pdf')
            printf(filename)
        Clear()

    lCName = Label(up, text="Customer Name:", font=text_format)
    lCName.grid(row=0, column=0, sticky=W)
    eCName = ttk.Combobox(up, values=custlst)
    eCName.grid(row=0, column=1, pady=5, padx=10)
    eCName.configure(width=16, font=text_format)
    eCName.current(0)
    eCName.bind('<KeyRelease>', CustN)
    eCName.bind('<Return>', Next_Prod)
    eCName.after(750,Custdrop)
    eCName.focus()

    label = Label(up, font=text_format)  # For Clock
    label.grid(row=0, column=2, sticky=W, columnspan=2)
    clock()

    lPName = Label(up, text="Product Name:", font=text_format)
    lPName.grid(row=1, column=0, sticky=W)
    ePName = ttk.Combobox(up, values=data)
    ePName.current(0)
    ePName.configure(width=16, font=text_format)
    ePName.grid(row=1, column=1, pady=5, padx=10)
    ePName.bind('<KeyRelease>', ProdN)
    ePName.bind('<Return>', Next_Qty)
    ePName.bind('<Shift_L>', Next_dis)
    ePName.bind('<Shift_R>', Next_dis)

    lQty = Label(up, text="Quantity:", font=text_format)
    lQty.grid(row=1, column=2, sticky=W)
    eQty = Entry(up, textvariable=Qty, width=7, font=text_format)
    eQty.grid(row=1, column=3, sticky=W, padx=10, pady=5)
    eQty.bind('<Return>', Next_Prod1)
    eQty.bind('<Shift_L>', Next_dis)
    eQty.bind('<Shift_R>', Next_dis)

    lBdis_r = Label(up, text="Discount(₹):", font=text_format)
    lBdis_r.grid(row=2, column=0, sticky=W)
    eBdis_r = Entry(up, textvariable=Dis_ru, width=7, font=text_format)
    eBdis_r.grid(row=2, column=1, sticky=W, padx=10, pady=5)
    eBdis_r.bind('<Return>', Dis_rup)
    eBdis_r.bind('<Shift_L>', Or_Dis_p)
    eBdis_r.bind('<Shift_R>', Or_Dis_p)

    lBdis_p = Label(up, text="Discount(%):", font=text_format)
    lBdis_p.grid(row=2, column=2, sticky=W)
    eBdis_p = Entry(up, textvariable=Dis_per, width=7, font=text_format)
    eBdis_p.grid(row=2, column=3, sticky=W, padx=10, pady=5)
    eBdis_p.bind('<Return>', Dis_perc)
    eBdis_p.bind('<Shift_L>', Or_Dis_r)
    eBdis_p.bind('<Shift_R>', Or_Dis_r)

    lType = Label(up, text="Payment Type:", font=text_format)
    lType.grid(row=3, column=0, sticky=W)
    eType1 = Radiobutton(up, text="Full", variable=Typ, value="Full", font=text_format, command=Credit)
    eType1.grid(row=3, column=1, sticky=W, pady=5)
    eType2 = Radiobutton(up, text="Part", variable=Typ, value="Part", font=text_format, command=Credit)
    eType2.grid(row=3, column=1, sticky=E, padx=10)

    lPay = Label(up, text="Advance:", font=text_format)
    lPay.grid(row=3, column=2, sticky=W)
    ePay = Entry(up, textvariable=Adv, width=7, font=text_format)
    ePay.grid(row=3, column=3, sticky=W, padx=10, pady=5)
    ePay.config(state="disabled")
    ePay.bind('<Return>', Adv_pay)

    lBnet = Label(up, text="Bill Total:", font=text_format)
    lBnet.grid(row=4, column=0, sticky=W)
    eBnet = Label(up, text=f"₹{Total.get()}", font=text_format)
    eBnet.grid(row=4, column=1, sticky=W, padx=10, pady=5)

    lBtot = Label(up, text="Balance:", font=text_format)
    lBtot.grid(row=4, column=2, sticky=W)
    eBtot = Label(up, text=f"₹{Bal.get()}", font=text_format)
    eBtot.grid(row=4, column=3, sticky=W, padx=10, pady=5)


    scroll = Scrollbar(down)
    scroll.pack(side=RIGHT, fill=Y)
    tv = ttk.Treeview(down, columns=('col0', 'col1', 'col2', 'col3', 'col4', 'col5'), 
                      show='headings', height=10, yscrollcommand=scroll.set, style="mystyle.Treeview")
    tv.pack()
    scroll.config(command=tv.yview)

    tv.heading('col0', text='Product Name')
    tv.heading('col1', text='Qty')
    tv.heading('col2', text='GST')
    tv.heading('col3', text='Unit')
    tv.heading('col4', text='Rate')
    tv.heading('col5', text='Price')

    tv.column('col0', anchor=CENTER, width=175)
    tv.column('col1', anchor=CENTER, width=60)
    tv.column('col2', anchor=CENTER, width=60)
    tv.column('col3', anchor=CENTER, width=60)
    tv.column('col4', anchor=CENTER, width=100)
    tv.column('col5', anchor=CENTER, width=100)


    button0 = Button(side, text="Add", **button_format, width=12, command=Add)
    button0.grid(row=0, column=0, sticky=W, pady=10, padx=10)

    button1 = Button(side, text="Edit Qty", **button_format, width=12 ,command=Modify)
    button1.grid(row=1, column=0, sticky=W, pady=10, padx=10)

    button2 = Button(side, text="Delete", **button_format, width=12, command=Delete)
    button2.grid(row=2, column=0, sticky=W, pady=10, padx=10)

    button3 = Button(side, text="Check Out", **button_format, width=12, command=Check)
    button3.grid(row=3, column=0, sticky=W, pady=10, padx=10)

    button3 = Button(side, text="Clear", **button_format, width=12, command=Clear)
    button3.grid(row=4, column=0, sticky=W, pady=10, padx=10)

    button5 = Button(side, text="Home", **button_format, width=12, command=Close)
    button5.grid(row=5, column=0, sticky=E, pady=10, padx=10)


""" Add Function """
def Main_Add(): # Select what to Add
    option = {1: Suppliers_Add, 2: Products_Add, 3: Main}
    
    right.grid(row=0,column=0,padx=350,pady=80)
    right2 = Frame(right, bd=2, relief=SOLID, padx=50, pady=50)
    right2.pack()
    l0 = Label(right2, text="New", font=("arial-bold", 25))
    l0.grid(row=0, column=0, padx=10, pady=10)

    def Comon(v):
        right2.destroy()
        dictt = option.get(v)
        dictt()


    b1 = Button(right2, text="Supplier", width=12, **button_format, command=lambda *args: Comon(1))
    b1.grid(row=1, column=0, padx=10, pady=10)
    b2 = Button(right2, text="Product", width=12, **button_format, command=lambda *args: Comon(2))
    b2.grid(row=2, column=0, padx=10, pady=10)
    b4 = Button(right2, text="Home", width=12, **button_format, command=lambda *args: Comon(3))
    b4.grid(row=4, column=0, padx=10, pady=10)
    l3 = Label(right2, text=" ", font=text_format)
    l3.grid(row=3, column=0, padx=10, pady=11)

def Suppliers_Add(): # Add supplier
    right.grid(row=0,column=0,padx=220,pady=55)
    SuppID = supp_gen(us, pas)
    right1 = Frame(right, bd=2, relief=SOLID, padx=50, pady=50)
    right1.pack()

    def Close():
        right1.destroy()
        Main()

    def Back():
        right1.destroy()
        Main_Add()

    def Save(tup):
        Create(1, tup, us, pas)
        supplst.append(f"{tup[0]} - {tup[1]}")
        right1.destroy()
        Suppliers_Add()

    def Show(tup0):
        SuppName, SuppAdd, SuppPhone, SuppEmail = tup0
        SuppName = SuppName.title()
        SuppAdd = SuppAdd.title()
        Name.set(SuppName)
        Adr.set(SuppAdd)
        eName.config(state='disabled')
        eAdd.config(state='disabled')
        ePhone.config(state='disabled')
        eEmail.config(state='disabled')
        tup = (SuppID, SuppName, SuppAdd, SuppPhone, SuppEmail)

        def OK():
            Save(tup)

        def callback(event):
            OK()

        right1.focus_set()
        right1.bind('<Return>', callback)

        button1.configure(text="All Ok! Lets save it", command=OK, width=15)

    def Check():
        phone, email = Phone.get(), Email.get()
        adr = eAdd.get(1.0, END).strip()
        Adr.set(adr)
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
            Show(tuple([Name.get(), Adr.get(), Phone.get(), Email.get()]))

    ID = StringVar()
    Name = StringVar()
    Adr = StringVar()
    Phone = StringVar()
    Email = StringVar()

    ID.set(SuppID)

    lID = Label(right1, text="Supplier ID", font=text_format)
    lID.grid(row=0, column=0, sticky=W)
    eID = Entry(right1, textvariable=ID, state='disabled', font=text_format)
    eID.grid(row=0, column=1, sticky=W, padx=10, pady=10)

    lName = Label(right1, text="Supplier Name", font=text_format)
    lName.grid(row=1, column=0, sticky=W)
    eName = Entry(right1, textvariable=Name, font=text_format)
    eName.grid(row=1, column=1, sticky=W, padx=10, pady=10)
    eName.focus()

    lAdd = Label(right1, text="Supplier Address", font=text_format)
    lAdd.grid(row=2, column=0, sticky=W)
    eAdd = Text(right1, width=20, height=3, font=text_format)
    eAdd.grid(row=2, column=1, sticky=W, padx=10, pady=10)

    lPhone = Label(right1, text="Supplier Phone No.", font=text_format)
    lPhone.grid(row=3, column=0, sticky=W)
    ePhone = Entry(right1, textvariable=Phone, font=text_format)
    ePhone.grid(row=3, column=1, sticky=W, padx=10, pady=10)

    lEmail = Label(right1, text="Supplier Email", font=text_format)
    lEmail.grid(row=4, column=0, sticky=W)
    eEmail = Entry(right1, textvariable=Email, font=text_format)
    eEmail.grid(row=4, column=1, sticky=W, padx=10, pady=10)

    def callback0(event):
        eAdd.focus()
    eName.bind('<Return>', callback0)

    def callback1(event):
        ePhone.focus()
    eAdd.bind('<Return>', callback1)

    def callback2(event):
        eEmail.focus()
    ePhone.bind('<Return>', callback2)

    def callback3(event):
        Check()
    eEmail.bind('<Return>', callback3)

    button1 = Button(right1, text="Check", width=7, **button_format, command=Check)
    button1.grid(row=5, column=0, pady=10, columnspan=2, padx=10)
    button3 = Button(right1, text="Back", width=5, **button_format, command=Back)
    button3.grid(row=5, column=0, pady=10, padx=10, sticky=W)
    button2 = Button(right1, text="Home", width=5, **button_format, command=Close)
    button2.grid(row=5, column=1, pady=10, padx=10, sticky=E)

def Products_Add(): # Add product
    right.grid(row=0,column=0,padx=220,pady=25)
    right1 = Frame(right, bd=2, relief=SOLID, padx=50, pady=20)
    right1.pack()

    global prodlst, prodname

    def Close():
        right1.destroy()
        Main()

    def Back():
        right1.destroy()
        Main_Add()

    def Save(tup1):
        Create(2, tup1, us, pas)
        prodname.update({tup1[1]:tup1[2]})
        prodlst.append(tup1[2])
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

        tup1 = (SuppID, ProdID, ProdName, ProdCost, ProdRate, ProdGST, ProdUnit, ProdStock)

        def OK():
            Save(tup1)

        def callback(event):
            OK()

        right1.focus_set()
        right1.bind('<Return>', callback)

        button1.configure(text="All Ok! Lets save it", command=OK)
        button2.configure(text="Cancel", command=Back)

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
        ProdID:str = prod_gen(SuppID, us, pas)
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

    lSID = Label(right1, text="Supplier", font=text_format)
    lSID.grid(row=0, column=0, sticky=W)
    eSID = ttk.Combobox(right1, values=supplst)
    eSID.config(width=18)
    eSID.config(font=text_format)
    eSID.current(0)
    eSID.grid(row=0, column=1, padx=10, pady=10)
    eSID.config(state='readonly')
    eSID.focus()

    lID = Label(right1, text="Product ID", font=text_format)
    lID.grid(row=1, column=0, sticky=W)
    eID = Entry(right1, textvariable=ID, state='disabled', font=text_format)
    eID.grid(row=1, column=1, sticky=W, padx=10, pady=10)

    lName = Label(right1, text="Product Name", font=text_format)
    lName.grid(row=2, column=0, sticky=W)
    eName = Entry(right1, textvariable=Name, font=text_format)
    eName.grid(row=2, column=1, sticky=W, padx=10, pady=10)

    lCost = Label(right1, text="Product Cost (CP)", font=text_format)
    lCost.grid(row=3, column=0, sticky=W)
    eCost = Entry(right1, textvariable=Cost, font=text_format)
    eCost.grid(row=3, column=1, sticky=W, padx=10, pady=10)

    lRate = Label(right1, text="Product Rate (SP)", font=text_format)
    lRate.grid(row=4, column=0, sticky=W)
    eRate = Entry(right1, textvariable=Rate, font=text_format)
    eRate.grid(row=4, column=1, sticky=W, padx=10, pady=10)

    lStock = Label(right1, text="Product Stock", font=text_format)
    lStock.grid(row=5, column=0, sticky=W)
    eStock = Entry(right1, textvariable=Stock, font=text_format)
    eStock.grid(row=5, column=1, sticky=W, padx=10, pady=10)

    lGST = Label(right1, text="Product GST(%)", font=text_format)
    lGST.grid(row=6, column=0, sticky=W)
    eGST = ttk.Combobox(right1, values=gstlst)
    eGST.current(0)
    eGST.config(width=18)
    eGST.config(font=text_format)
    eGST.grid(row=6, column=1, padx=10, pady=10)
    eGST.config(state='readonly')

    lUnit = Label(right1, text="Product Unit", font=text_format)
    lUnit.grid(row=7, column=0, sticky=W)
    eUnit = ttk.Combobox(right1, values=unitlst)
    eUnit.config(width=18)
    eUnit.current(0)
    eUnit.config(font=text_format)
    eUnit.grid(row=7, column=1, padx=10, pady=10)
    eUnit.config(state='readonly')

    def callback0(event):
        eName.focus()
    eSID.bind('<Return>', callback0)

    def callback1(event):
        eCost.focus()
    eName.bind('<Return>', callback1)

    def callback2(event):
        eRate.focus()
    eCost.bind('<Return>', callback2)

    def callback3(event):
        eStock.focus()
    eRate.bind('<Return>', callback3)

    def callback4(event):
        eGST.focus()
    eStock.bind('<Return>', callback4)

    def callback5(event):
        eUnit.focus()
    eGST.bind('<Return>', callback5)

    def callback6(event):
        Check()
    eUnit.bind('<Return>', callback6)

    button1 = Button(right1, text="Check", width=7, **button_format, command=Check)
    button1.grid(row=8, column=0, pady=10, columnspan=2, padx=10)
    button3 = Button(right1, text="Back", width=5, **button_format, command=Back)
    button3.grid(row=8, column=0, pady=10, padx=10, sticky=W)
    button2 = Button(right1, text="Home", width=5, **button_format, command=Close)
    button2.grid(row=8, column=1, pady=10, padx=10, sticky=E)


""" Modify Functions """
def Main_Mod(): # Select what to modify 
    option = {1: SuppSelct, 2: ProdSelect, 3: Delsupp, 4: Delprod, 5: Main}
    
    right.grid(column=0,row=0,padx=350,pady=55)
    right2 = Frame(right, bd=2, relief=SOLID, padx=50, pady=50)
    right2.pack()


    def Comon(v):
        right2.destroy()
        dictt = option.get(v)
        dictt()

    l0 = Label(right2, text="Modify", font=("arial-bold", 25))
    l0.grid(row=0, column=0)

    b1 = Button(right2, text="Supplier", width=12, **button_format, command=lambda *args: Comon(1))
    b1.grid(row=1, column=0, padx=10, pady=10)

    b2 = Button(right2, text="Product", width=12, **button_format, command=lambda *args: Comon(2))
    b2.grid(row=2, column=0, padx=10, pady=10)

    b3 = Button(right2, text="Supplier Status", width=12, **button_format, command=lambda *args: Comon(3))
    b3.grid(row=3, column=0, padx=10, pady=10)

    b4 = Button(right2, text="Product Status", width=12, **button_format, command=lambda *args: Comon(4))
    b4.grid(row=4, column=0, padx=10, pady=10)

    b5 = Button(right2, text="Home", width=12, **button_format, command=lambda *args: Comon(5))
    b5.grid(row=5, column=0, padx=10, pady=10)

def SuppSelct(): # Select for modify Supplier
    right.grid(row=0,column=0,padx=275,pady=80)
    right3 = Frame(right, bd=2, relief=SOLID, padx=50, pady=50)
    right3.pack()
    l0 = Label(right3, text="Supplier", font=("arial bold", 20))
    l0.grid(row=0, column=0, columnspan=2)

    def back(v):
        right3.destroy()
        if v == 1:
            Main_Mod()
        elif v == 2:
            Main()

    def Check(event):
        item = tv.item(tv.focus())['values']
        try:
            item[0]
        except:
            messagebox.showerror("Wrong Format", "Select Supplier")
            return

        right3.destroy()
        Suppliers_Edit(item[0])

    right4 = Frame(right3, bd=1, relief=SOLID)
    right4.grid(row=2, column=0, pady=20, columnspan=2)
    scroll = Scrollbar(right4)
    scroll.pack(side=RIGHT, fill=Y)
    tv = ttk.Treeview(right4, columns=('col0', 'col1'),
                      show='headings', height=4, yscrollcommand=scroll.set, style="mystyle.Treeview")
    tv.pack()
    scroll.config(command=tv.yview)

    tv.heading('col0', text='Id')
    tv.heading('col1', text='Name')

    tv.column('col0', anchor=CENTER, width=100)
    tv.column('col1', anchor=CENTER, width=200)

    for ID, Name in suppname.items():
        i = [ID, Name]
        tv.insert('', 'end', values=i)

    tv.bind('<Double 1>', Check)

    b4 = Button(right3, text="Back", width=12, **button_format, command=lambda *args: back(1))
    b4.grid(row=3, column=0, pady=10)

    b5 = Button(right3, text="Home", width=12, **button_format, command=lambda *args: back(2))
    b5.grid(row=3, column=1, pady=10)

def ProdSelect(): # Select for modify Product
    right.grid(row=0,column=0,padx=275,pady=80)
    right3 = Frame(right, bd=2, relief=SOLID, padx=50, pady=50)
    right3.pack()
    l0 = Label(right3, text="Product", font=("arial bold", 20))
    l0.grid(row=0, column=0, columnspan=2)

    def back(v):
        right3.destroy()
        if v == 1:
            Main_Mod()
        elif v == 2:
            Main()

    def Check(event):
        item = tv.item(tv.focus())['values']
        try:
            item[0]
        except:
            messagebox.showerror("Wrong Format", "Select Product")
            return

        right3.destroy()
        Products_Edit(item[0])

    right4 = Frame(right3, bd=1, relief=SOLID)
    right4.grid(row=2, column=0, pady=20, columnspan=2)
    scroll = Scrollbar(right4)
    scroll.pack(side=RIGHT, fill=Y)
    tv = ttk.Treeview(right4, columns=('col0', 'col1'),
                      show='headings', height=4, yscrollcommand=scroll.set, style="mystyle.Treeview")
    tv.pack()
    scroll.config(command=tv.yview)

    tv.heading('col0', text='Id')
    tv.heading('col1', text='Name')

    tv.column('col0', anchor=CENTER, width=100)
    tv.column('col1', anchor=CENTER, width=200)

    for ID, Name in prodname.items():
        i = [ID, Name]
        tv.insert('', 'end', values=i)

    tv.bind('<Double 1>', Check)

    b4 = Button(right3, text="Back", width=12, **button_format, command=lambda *args: back(1))
    b4.grid(row=3, column=0, pady=10)

    b5 = Button(right3, text="Home", width=12, **button_format, command=lambda *args: back(2))
    b5.grid(row=3, column=1, pady=10)

def Delsupp(): # Delete Supplier
    right.grid(row=0,column=0,padx=145,pady=80)
    right3 = Frame(right, bd=2, relief=SOLID, padx=50, pady=50)
    right3.pack()
    demodb = mysql.connect(**DB)
    cursor = demodb.cursor()
    cursor.execute(f"SELECT * FROM supplier")
    lst2 = list(cursor.fetchall())
    demodb.close()
    right2 = Frame(right3, bd=1, relief=SOLID)
    right2.grid(row=1, column=0, pady=20)
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

    def ab():
        item:list = tv.item(tv.focus())['values']
        try:
            item[0]
        except:
            messagebox.showerror("Wrong Format", "Select Supplier")
            return 0
        if item[5] == 'Discontinued':
            item[5] = 0
        elif item[5] == 'Active':
            item[5] = 1
        tup = (item[0], item[5])
        Update_column(2, tup, us, pas)
        Update_lst(1)
        if item[5] == 1:
            item[5] = 'Discontinued'
        elif item[5] == 0:
            item[5] = 'Active'
        selected = tv.focus()
        tv.item(selected, text="", values=item)

    def click(event):
        ab()
    tv.bind('<Double 1>', click)

    def close():
        right3.destroy()
        Main()

    def back():
        right2.destroy()
        right3.destroy()
        Main_Mod()

    b1 = Button(right3, text='Back', width=12, **button_format, command=back)
    b1.grid(row=3, column=0, sticky=W)
    l1 = Label(right3, text="Change Supplier Status", font=("arial-bold", 25))
    l1.grid(row=0, column=0)
    b2 = Button(right3, text="Home", width=12, **button_format, command=close)
    b2.grid(row=3, column=0, sticky=E)
    b3 = Button(right3, text="Change Status", width=12, **button_format, command=ab)
    b3.grid(row=3, column=0)

def Delprod(): # Delete Product
    right.grid(row=0,column=0,padx=200,pady=80)
    right3 = Frame(right, bd=2, relief=SOLID, padx=50, pady=50)
    right3.pack()
    demodb = mysql.connect(**DB)
    cursor = demodb.cursor()
    cursor.execute(f"SELECT ProdID, Name, Stock, SP, Hide FROM product")
    lst2 = list(cursor.fetchall())
    demodb.close()
    right2 = Frame(right3, bd=1, relief=SOLID)
    right2.grid(row=1, pady=20, column=0)
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
        right3.destroy()
        Main()

    def ab():
        item = tv.item(tv.focus())['values']
        try:
            item[0]
        except:
            messagebox.showerror("Wrong Format", "Select Product")
            return 0
        if item[4] == 'Discontinued':
            item[4] = 0
        elif item[4] == 'Active':
            item[4] = 1
        tup = (item[0], item[4])
        Update_column(3, tup, us, pas)
        Update_lst(2)
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
        right2.destroy()
        right3.destroy()
        Main_Mod()

    b1 = Button(right3, text='Back', width=12, **button_format, command=back)
    b1.grid(row=3, column=0, sticky=W)
    l1 = Label(right3, text="Change Product Status", font=("arial-bold", 25))
    l1.grid(row=0, column=0)
    b2 = Button(right3, text="Home", width=12, **button_format, command=close)
    b2.grid(row=3, column=0, sticky=E)
    b3 = Button(right3, text="Change Status", width=12, **button_format, command=ab)
    b3.grid(row=3, column=0)

def Suppliers_Edit(SuppID): # Modify Supplier
    right.grid(row=0,column=0,padx=220,pady=55)
    right1 = Frame(right, bd=2, relief=SOLID, padx=50, pady=50)
    right1.pack()

    def Close():
        right1.destroy()
        Main()

    def Back():
        right1.destroy()
        SuppSelct()

    def Save(tup):
        Update_row(1, tup, us, pas)
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

        button0 = Button(right1, text="All Ok! Lets save it", **button_format, command=OK)
        button0.grid(row=5, column=0, columnspan=2, pady=10)
        button = Button(right1, text="Cancel", **button_format, command=Close)
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

    def callback1(event):
        eAdd.focus()

    def callback2(event):
        ePhone.focus()

    def callback3(event):
        eEmail.focus()

    def callback4(event):
        Check()

    ID = StringVar()
    Name = StringVar()
    Add = StringVar()
    Phone = StringVar()
    Email = StringVar()

    demodb = mysql.connect(**DB)
    cursor = demodb.cursor()
    cursor.execute(f"SELECT * FROM supplier WHERE SuppID='{SuppID}';")
    i:tuple = cursor.fetchone()
    ID.set(i[0])
    Name.set(i[1])
    Add.set(i[2])
    Phone.set(i[3])
    Email.set(i[4])
    demodb.close()

    lID = Label(right1, text="Supplier ID", font=text_format)
    lID.grid(row=0, column=0, sticky=W)

    eID = Entry(right1, textvariable=ID, state='disabled', font=text_format)
    eID.grid(row=0, column=1, sticky=W, padx=10, pady=10)

    lName = Label(right1, text="Supplier Name", font=text_format)
    lName.grid(row=1, column=0, sticky=W)

    eName = Entry(right1, textvariable=Name, font=text_format)
    eName.grid(row=1, column=1, sticky=W, padx=10, pady=10)
    eName.focus()
    eName.bind('<Return>', callback1)

    lAdd = Label(right1, text="Supplier Address", font=text_format)
    lAdd.grid(row=2, column=0, sticky=W)

    eAdd = Text(right1, width=20, height=3, font=text_format)
    eAdd.grid(row=2, column=1, sticky=W, padx=10, pady=10)
    eAdd.insert(1.0, Add.get())
    eAdd.bind('<Return>', callback2)

    lPhone = Label(right1, text="Supplier Phone No.", font=text_format)
    lPhone.grid(row=3, column=0, sticky=W)

    ePhone = Entry(right1, textvariable=Phone, font=text_format)
    ePhone.grid(row=3, column=1, sticky=W, padx=10, pady=10)
    ePhone.bind('<Return>', callback3)

    lEmail = Label(right1, text="Supplier Email", font=text_format)
    lEmail.grid(row=4, column=0, sticky=W)

    eEmail = Entry(right1, textvariable=Email, font=text_format)
    eEmail.grid(row=4, column=1, sticky=W, padx=10, pady=10)
    eEmail.bind('<Return>', callback4)

    button1 = Button(right1, text="Check", width=7, **button_format, command=Check)
    button1.grid(row=5, column=0, pady=10, columnspan=2, padx=10)
    button3 = Button(right1, text="Back", width=5, **button_format, command=Back)
    button3.grid(row=5, column=0, pady=10, padx=10, sticky=W)
    button2 = Button(right1, text="Home", width=5, **button_format, command=Close)
    button2.grid(row=5, column=1, pady=10, padx=10, sticky=E)

def Products_Edit(ProdID): # Modify Product
    right.grid(row=0,column=0,padx=220,pady=35)
    right1 = Frame(right, bd=2, relief=SOLID, padx=50, pady=20)
    right1.pack()

    def Close():
        right1.destroy()
        Main()

    def Back():
        right1.destroy()
        ProdSelect()

    def Save(tup1):
        Update_row(2, tup1, us, pas)
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

        button0 = Button(right1, text="All Ok! Lets save it", **button_format, command=OK)
        button0.grid(row=8, column=0, columnspan=2, pady=10)
        button = Button(right1, text="Cancel", **button_format, command=Close)
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

    def callback1(event):
        eCost.focus()

    def callback2(event):
        eRate.focus()

    def callback3(event):
        eStock.focus()

    def callback4(event):
        eGST.focus()

    def callback5(event):
        eUnit.focus()

    def callback6(event):
        Check()

    ID = StringVar()
    Name = StringVar()
    Cost = StringVar()
    Rate = StringVar()
    GST = StringVar()
    Unit = StringVar()
    Stock = StringVar()
    SID = StringVar()

    demodb = mysql.connect(**DB)
    cursor = demodb.cursor()
    sql = f"SELECT * FROM product where product.ProdID='{ProdID}';"
    cursor.execute(sql)
    i:tuple = cursor.fetchone()
    SID.set(i[0])
    ID.set(i[1])
    Name.set(i[2])
    Cost.set(i[3])
    Rate.set(i[4])
    GST.set(i[5])
    Unit.set(i[6])
    Stock.set(i[7])
    demodb.close()

    lSID = Label(right1, text="Supplier", font=text_format)
    lSID.grid(row=0, column=0, sticky=W)

    eSID = Entry(right1, textvariable=SID, state='disabled', font=text_format)
    eSID.grid(row=0, column=1, sticky=W, padx=10, pady=10)

    lID = Label(right1, text="Product ID", font=text_format)
    lID.grid(row=1, column=0, sticky=W)

    eID = Entry(right1, textvariable=ID, state='disabled', font=text_format)
    eID.grid(row=1, column=1, sticky=W, padx=10, pady=10)

    lName = Label(right1, text="Product Name", font=text_format)
    lName.grid(row=2, column=0, sticky=W)

    eName = Entry(right1, textvariable=Name, font=text_format)
    eName.grid(row=2, column=1, sticky=W, padx=10, pady=10)
    eName.bind('<Return>', callback1)
    eName.focus()

    lCost = Label(right1, text="Product Cost (CP)", font=text_format)
    lCost.grid(row=3, column=0, sticky=W)

    eCost = Entry(right1, textvariable=Cost, font=text_format)
    eCost.grid(row=3, column=1, sticky=W, padx=10, pady=10)
    eCost.bind('<Return>', callback2)

    lRate = Label(right1, text="Product Rate (SP)", font=text_format)
    lRate.grid(row=4, column=0, sticky=W)

    eRate = Entry(right1, textvariable=Rate, font=text_format)
    eRate.grid(row=4, column=1, sticky=W, padx=10, pady=10)
    eRate.bind('<Return>', callback3)

    lStock = Label(right1, text="Product Stock", font=text_format)
    lStock.grid(row=5, column=0, sticky=W)

    eStock = Entry(right1, textvariable=Stock, font=text_format)
    eStock.grid(row=5, column=1, sticky=W, padx=10, pady=10)
    eStock.bind('<Return>', callback4)

    lGST = Label(right1, text="Product GST(%)", font=text_format)
    lGST.grid(row=6, column=0, sticky=W)

    eGST = ttk.Combobox(right1, values=gstlst)
    for ind, itm in enumerate(gstlst):
        aa = str(GST.get())
        if aa == itm[0:5]:
            eGST.current(ind)
    eGST.config(width=18)
    eGST.config(font=text_format)
    eGST.grid(row=6, column=1, padx=10, pady=10)
    eGST.config(state='readonly')
    eGST.bind('<Return>', callback5)

    lUnit = Label(right1, text="Product Unit", font=text_format)
    lUnit.grid(row=7, column=0, sticky=W)

    eUnit = ttk.Combobox(right1, values=unitlst)
    eUnit.config(width=18)
    for ind, itm in enumerate(unitlst):
        aa = Unit.get()
        if aa == itm[0:4]:
            eUnit.current(ind)
    eUnit.config(font=text_format)
    eUnit.grid(row=7, column=1, padx=10, pady=10)
    eUnit.config(state='readonly')
    eUnit.bind('<Return>', callback6)

    button1 = Button(right1, text="Check", width=7, **button_format, command=Check)
    button1.grid(row=8, column=0, pady=10, columnspan=2, padx=10)
    button3 = Button(right1, text="Back", width=5, **button_format, command=Back)
    button3.grid(row=8, column=0, pady=10, padx=10, sticky=W)
    button2 = Button(right1, text="Home", width=5, **button_format, command=Close)
    button2.grid(row=8, column=1, pady=10, padx=10, sticky=E)


""" View Functions """
def Main_View(): # Select what to View
    option = {1: View, 2: View, 3: View, 4: View, 5: Main}
    
    right.grid(column=0,row=0,padx=350,pady=35)
    right2 = Frame(right, bd=2, relief=SOLID, padx=50, pady=50)
    right2.pack(pady=20)

    def Comon(v):
        right2.destroy()
        dictt = option.get(v)
        if v == 5:
            dictt()
        else:
            dictt(v)

    l0 = Label(right2, text="View", font=("arial-bold", 25))
    l0.grid(row=0, column=0)

    b1 = Button(right2, text="Supplier", width=12, **button_format, command=lambda *args: Comon(1))
    b1.grid(row=1, column=0, padx=10, pady=10)

    b2 = Button(right2, text="Product", width=12, **button_format, command=lambda *args: Comon(2))
    b2.grid(row=2, column=0, padx=10, pady=10)

    b3 = Button(right2, text="Bills", width=12, **button_format, command=lambda *args: Comon(3))
    b3.grid(row=3, column=0, padx=10, pady=10)

    b4 = Button(right2, text="Customer", width=12, **button_format, command=lambda *args: Comon(4))
    b4.grid(row=4, column=0, padx=10, pady=10)

    b5 = Button(right2, text="Home", width=12, **button_format, command=lambda *args: Comon(5))
    b5.grid(row=5, column=0, padx=10, pady=10)

def View(Type): # Control what to View
    right1 = Frame(right, bd=2, relief=SOLID, padx=50, pady=20)
    right1.pack(pady=20)
    demodb = mysql.connect(**DB)
    cursor = demodb.cursor()

    if Type == 1:  # Supplier
        right.grid(row=0,column=0,padx=145,pady=55)
        cursor.execute(f"SELECT * FROM supplier")
        supp = list(cursor.fetchall())
        lst2 = supp
        l1 = Label(right1, text="Suppliers", font=("arial-bold", 25))
        l1.grid(row=0, column=0,pady=20)
        right2 = LabelFrame(right1,text="Supplier", bd=1, relief=SOLID)
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

        def back():
            right1.destroy()
            Main_View()

        b1 = Button(right1, text='Back', width=12, **button_format, command=back)
        b1.grid(row=3, column=0, sticky=W,pady=20)
        b2 = Button(right1, text="Home", width=12, **button_format, command=close)
        b2.grid(row=3, column=0, sticky=E)
        demodb.close()

    elif Type == 2:  # Products
        right.grid(row=0,column=0,padx=200,pady=45)
        cursor.execute(f"SELECT ProdID, Name, Stock, SP, Hide FROM product")
        prod = list(cursor.fetchall())
        lst2 = prod
        l1 = Label(right1, text="Products", font=("arial-bold", 25))
        l1.grid(row=0, column=0,pady=20)
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

        def back():
            right1.destroy()
            Main_View()

        def ab():
            item = tv.item(tv.focus())
            try:
                item['values'][0]
            except:
                return
            tup = item['values'][0]
            right1.destroy()
            Products_View(tup)

        def click(event):
            ab()

        tv.bind('<Double 1>', click)
        b1 = Button(right1, text='Back', width=10,**button_format, command=back)
        b1.grid(row=3, column=0, sticky=W,pady=20)
        b2 = Button(right1, text="Home", width=10,**button_format, command=close)
        b2.grid(row=3, column=0, sticky=E)
        b3 = Button(right1, text="Next", width=10,**button_format, command=ab)
        b3.grid(row=3, column=0)
        demodb.close()

    elif Type == 3:  # Bills
        right.grid(row=0,column=0,padx=65,pady=40)
        cursor.execute(f"SELECT bill.BillID, cust.Name, bill.Type, bill.Date, bill.Qty, bill.Balance, bill.Total FROM "
                   f"bill,cust where bill.CustID=cust.CustID order by Date;")
        bills = list(cursor.fetchall())
        lst2 = bills
        l1 = Label(right1, text="Bills", font=("arial-bold", 25))
        l1.grid(row=0, column=0,pady=20)
        right2 = LabelFrame(right1, text='Bills', bd=1, relief=SOLID)
        right2.grid(row=1, column=0)
        scroll = Scrollbar(right2)
        scroll.pack(side=RIGHT, fill=Y)
        tv = ttk.Treeview(right2, columns=('col0', 'col1', 'col2', 'col3', 'col4', 'col5', 'col6'), show='headings'
                          , height=8, yscrollcommand=scroll.set, style="mystyle.Treeview")
        tv.pack()
        scroll.config(command=tv.yview)

        tv.heading('col0', text='Bill No.')
        tv.heading('col1', text='Cust. Name')
        tv.heading('col2', text='Bill Type')
        tv.heading('col3', text='Bill Date')
        tv.heading('col4', text='No. Items')
        tv.heading('col5', text='Bill Balance')
        tv.heading('col6', text='Bill Total')

        tv.column('col0', anchor=CENTER, width=100)
        tv.column('col1', anchor=CENTER, width=100)
        tv.column('col2', anchor=CENTER, width=100)
        tv.column('col3', anchor=CENTER, width=100)
        tv.column('col4', anchor=CENTER, width=100)
        tv.column('col5', anchor=CENTER, width=100)
        tv.column('col6', anchor=CENTER, width=100)

        for i in lst2:
            i = list(i)
            zz = str(i[3]).split()[0]
            i[3] = zz.split('-')[2] + '/' + zz.split('-')[1] + '/' + zz.split('-')[0]
            tv.insert('', 'end', values=i)

        def close():
            right1.destroy()
            Main()

        def back():
            right1.destroy()
            Main_View()

        def ab():
            item = tv.item(tv.focus())
            try:
                item['values'][0]
            except:
                return
            tup = item['values'][0]
            tup1 = item['values'][3]
            right1.destroy()
            Bill_View(tup, tup1)

        def click(event):
            ab()

        tv.bind('<Double 1>', click)
        b1 = Button(right1, text='Back', width=12, **button_format, command=back)
        b1.grid(row=3, column=0, sticky=W)
        b2 = Button(right1, text="Home", width=12, **button_format, command=close)
        b2.grid(row=3, column=0, sticky=E,pady=20)
        b3 = Button(right1, text="Next", width=12, **button_format, command=ab)
        b3.grid(row=3, column=0)
        demodb.close()

    elif Type == 4:  # Customers
        right.grid(row=0,column=0,padx=200,pady=45)
        cursor.execute(f"SELECT CustID,Name,Qty,Balance,Total FROM cust;")
        cust = list(cursor.fetchall())
        lst2 = cust
        l1 = Label(right1, text="Customers", font=("arial-bold", 25))
        l1.grid(row=0, column=0,pady=20)
        right2 = LabelFrame(right1, text='Customers', bd=1, relief=SOLID)
        right2.grid(row=1, column=0)
        scroll = Scrollbar(right2)
        scroll.pack(side=RIGHT, fill=Y)
        tv = ttk.Treeview(right2, columns=('col0', 'col1', 'col2', 'col3', 'col4'), show='headings'
                          , height=8, yscrollcommand=scroll.set, style="mystyle.Treeview")
        tv.pack()
        scroll.config(command=tv.yview)

        tv.heading('col0', text='Customer ID')
        tv.heading('col1', text='Customer Name')
        tv.heading('col2', text='Qty')
        tv.heading('col3', text='Balance')
        tv.heading('col4', text='Total')

        tv.column('col0', anchor=CENTER, width=110)
        tv.column('col1', anchor=CENTER, width=155)
        tv.column('col2', anchor=CENTER, width=50)
        tv.column('col3', anchor=CENTER, width=100)
        tv.column('col4', anchor=CENTER, width=100)

        for i in lst2:
            i = list(i)
            tv.insert('', 'end', values=i)

        def close():
            right1.destroy()
            Main()

        def back():
            right1.destroy()
            Main_View()

        def ab():
            item = tv.item(tv.focus())
            try:
                item['values'][0]
            except:
                return
            tup = item['values'][0]
            right1.destroy()
            Cust_View(tup)

        def click(event):
            ab()

        tv.bind('<Double 1>', click)
        b1 = Button(right1, text='Back', width=10, **button_format, command=back)
        b1.grid(row=3, column=0, sticky=W,pady=20)
        b2 = Button(right1, text="Home", width=10, **button_format, command=close)
        b2.grid(row=3, column=0, sticky=E)
        b3 = Button(right1, text="Next", width=10, **button_format, command=ab)
        b3.grid(row=3, column=0)
        demodb.close()

def Products_View(ProdID): # View Products
    right.grid(row=0,column=0,padx=100,pady=85)
    right1 = Frame(right, bd=2, relief=SOLID, padx=50, pady=20)
    right1.pack()

    def Close():
        right1.destroy()
        Main()

    def Back():
        right1.destroy()
        View(2)

    ID = StringVar()
    Name = StringVar()
    Cost = StringVar()
    Rate = StringVar()
    GST = StringVar()
    Unit = StringVar()
    Stock = StringVar()
    SID = StringVar()
    State = StringVar()

    demodb = mysql.connect(**DB)
    cursor = demodb.cursor()
    sql = f"SELECT * FROM product where product.ProdID='{ProdID}';"
    cursor.execute(sql)
    i:tuple = cursor.fetchone()
    SID.set(i[0])
    ID.set(i[1])
    Name.set(i[2])
    Cost.set(i[3])
    Rate.set(i[4])
    GST.set(i[5])
    Unit.set(i[6])
    Stock.set(i[7])
    if i[8] == 'Y':
        State.set('Discontinued')
    elif i[8] == 'N':
        State.set('Active')
    demodb.close()

    lSID = Label(right1, text="Supplier", font=text_format)
    lSID.grid(row=0, column=0, sticky=W)
    eSID = Entry(right1, textvariable=SID, state='readonly', font=text_format)
    eSID.grid(row=0, column=1, sticky=W, padx=10, pady=10)

    lID = Label(right1, text="Product ID", font=text_format)
    lID.grid(row=0, column=2, sticky=W)
    eID = Entry(right1, textvariable=ID, state='readonly', font=text_format, width=8)
    eID.grid(row=0, column=3, sticky=W, padx=10, pady=10)

    lName = Label(right1, text="Product Name", font=text_format)
    lName.grid(row=1, column=0, sticky=W)
    eName = Entry(right1, textvariable=Name, state='readonly', font=text_format)
    eName.grid(row=1, column=1, sticky=W, padx=10, pady=10)

    lState = Label(right1, text='Status', font=text_format)
    lState.grid(row=1, column=2, sticky=W)
    eState = Entry(right1, textvariable=State, state='readonly', font=text_format, width=8)
    eState.grid(row=1, column=3, padx=10, pady=10)

    lCost = Label(right1, text="Product Cost (CP)", font=text_format)
    lCost.grid(row=2, column=0, sticky=W)
    eCost = Entry(right1, textvariable=Cost, state='readonly', font=text_format)
    eCost.grid(row=2, column=1, sticky=W, padx=10, pady=10)

    lRate = Label(right1, text="Product Rate (SP)", font=text_format)
    lRate.grid(row=2, column=2, sticky=W)
    eRate = Entry(right1, textvariable=Rate, state='readonly', font=text_format, width=8)
    eRate.grid(row=2, column=3, sticky=W, padx=10, pady=10)

    lStock = Label(right1, text="Product Stock", font=text_format)
    lStock.grid(row=3, column=0, sticky=W)
    eStock = Entry(right1, textvariable=Stock, state='readonly', font=text_format)
    eStock.grid(row=3, column=1, sticky=W, padx=10, pady=10)

    lUnit = Label(right1, text="Product Unit", font=text_format)
    lUnit.grid(row=3, column=2, sticky=W)
    eUnit = Entry(right1, textvariable=Unit, state='readonly', font=text_format, width=8)
    eUnit.grid(row=3, column=3, padx=10, pady=10)

    lGST = Label(right1, text="Product GST(%)", font=text_format)
    lGST.grid(row=4, column=0, sticky=W)
    eGST = Entry(right1, textvariable=GST, state='readonly', font=text_format)
    eGST.grid(row=4, column=1, padx=10, pady=10)

    button1 = Button(right1, text="Back", width=5, **button_format, command=Back)
    button1.grid(row=5, column=0, columnspan=2, pady=10, padx=10)
    button2 = Button(right1, text="Home", width=5, **button_format, command=Close)
    button2.grid(row=5, column=2, columnspan=2, pady=10, padx=10)

def Bill_View(BillID, Date): # View Bills
    # right.place(x=70, y=50)
    right.grid(row=0,column=0,padx=75,pady=45)
    right1 = Frame(right, bd=2, relief=SOLID, padx=20, pady=20)
    right1.pack()
    down = Frame(right1, bd=1, relief=SOLID)
    down.grid(row=1, column=1, sticky=W, pady=5)
    side = Frame(right1)
    side.grid(row=0, column=0, rowspan=2)
    up = Frame(right1)
    up.grid(row=0, column=1, sticky=W)
    demodb = mysql.connect(**DB)
    cursor = demodb.cursor()
    cursor.execute(f"SELECT billdetail.Serial, product.Name, billdetail.Qty, product.SP, billdetail.Total, "
                   f"product.GST, product.Unit FROM billdetail,product where billdetail.BillID = '{BillID}' AND "
                   f"billdetail.ProdID=product.ProdID ORDER BY Serial ASC;")
    Bitem = cursor.fetchall()
    cursor.execute(f"SELECT bill.BillID, bill.CustID, Cust.Name, bill.Type, bill.Amt, bill.Dis_per, bill.Total, "
                   f"bill.Balance FROM bill,Cust where BillID = '{BillID}' AND bill.CustID=Cust.CustID")
    billd:tuple = cursor.fetchone()
    demodb.close()
    CName = StringVar()
    Cid = StringVar()
    Bdisc = StringVar()
    Btot = StringVar()
    Bnet = StringVar()
    Bpay = StringVar()
    Type = StringVar()

    CName.set(billd[2])
    Cid.set(billd[1])
    Bdisc.set(f'{abs(round(billd[4] - billd[6], 2))} ({billd[5]}%)')
    Type.set(billd[3])
    Bnet.set(f"₹{billd[6]}")
    if Type.get() == 'Cash':
        Btot.set(f"₹{billd[6]}")
        Bpay.set(f'₹0.0')
    elif Type.get() == 'Credit':
        Btot.set(f"₹{abs(round(billd[6] - billd[7]))}")
        Bpay.set(f'₹{billd[7]}')

    def Close():
        right1.destroy()
        Main()

    def Back():
        right1.destroy()
        View(3)

    def Pri():
        PDF(BillID)
        filename = str(f'Bills\\Invoice {BillID}.pdf')
        printf(filename)

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

    for i in Bitem:
        tv.insert('', 'end', values=i)

    lCName = Label(up, text="Customer Name:", font=text_format)
    lCName.grid(row=0, column=0, sticky=W)
    eCName = Entry(up, textvariable=CName, width=18, font=text_format, state='readonly')
    eCName.grid(row=0, column=1, sticky=W, padx=10, pady=5)

    lDate = Label(up, text=f"Billing Date:", font=text_format)
    lDate.grid(row=1, column=2, sticky=W)
    eDate = Label(up, text=f"{Date}", font=text_format)
    eDate.grid(row=1, column=3, sticky=W, padx=10, pady=5)

    lType = Label(up, text="Payment Type:", font=text_format)
    lType.grid(row=1, column=0, sticky=W)
    eType = Label(up, text=Type.get(), font=text_format)
    eType.grid(row=1, column=1, sticky=W, padx=10, pady=5)

    lPay = Label(up, text="Balance Amt.:", font=text_format)
    lPay.grid(row=3, column=2, sticky=W)
    ePay = Label(up, text=Bpay.get(), font=text_format)
    ePay.grid(row=3, column=3, sticky=W, padx=10, pady=5)

    lBtot = Label(up, text="Amt. Paid:", font=text_format)
    lBtot.grid(row=2, column=2, sticky=W)
    eBtot = Label(up, text=Btot.get(), font=text_format)
    eBtot.grid(row=2, column=3, sticky=W, padx=10, pady=5)

    lBdisc = Label(up, text="Discount Amt.(%):", font=text_format)
    lBdisc.grid(row=2, column=0, sticky=W)
    eBdisc = Label(up, text=Bdisc.get(), font=text_format)
    eBdisc.grid(row=2, column=1, sticky=W, padx=10, pady=5)

    lBnet = Label(up, text="Bill Total:", font=text_format)
    lBnet.grid(row=3, column=0, sticky=W)
    eBnet = Label(up, text=Bnet.get(), font=text_format)
    eBnet.grid(row=3, column=1, sticky=W, padx=10, pady=5)

    lBdis = Label(up, text="Cust. ID:", font=text_format)
    lBdis.grid(row=0, column=2, sticky=W)
    eBdis = Label(up, text=Cid.get(), font=text_format)
    eBdis.grid(row=0, column=3, sticky=W, padx=10, pady=5)

    button1 = Button(side, text="Home", **button_format, width=12, command=Close)
    button1.grid(row=5, column=0, sticky=E, pady=10, padx=10)

    button2 = Button(side, text="Back", **button_format, width=12, command=Back)
    button2.grid(row=4, column=0, sticky=E, pady=10, padx=10)

    button3 = Button(side, text='Print Bill', **button_format, width=12, command=Pri)
    button3.grid(row=3, column=0, sticky=E, pady=10, padx=10)

def Cust_View(CustID): # View Customers
    right.grid(row=0,column=0,padx=0,pady=0)

    right1 = Frame(right, bd=2, relief=SOLID, padx=20, pady=20)
    right1.pack()
    down = Frame(right1, bd=1, relief=SOLID)
    down.grid(row=1, column=1, sticky=W, pady=5)
    side = Frame(right1)
    side.grid(row=0, column=0, rowspan=2)
    up = Frame(right1)
    up.grid(row=0, column=1, sticky=W)
    
    demodb = mysql.connect(**DB)
    cursor = demodb.cursor()
    cursor.execute(f"SELECT Name, CustID, Qty, Total, ROUND((Total-Balance),2), Balance from cust where CustID = '{CustID}'")
    CustDet:tuple = cursor.fetchone()
    cursor.execute(f"SELECT BillID, Date, Type, bill.Qty, Dis_per, bill.Total,bill.Balance,ROUND((bill.Total-bill.Balance),2)"
                   f" AS Paid FROM bill,Cust where cust.CustID = '{CustID}' AND bill.CustID=Cust.CustID;")
    Bills:tuple = cursor.fetchall()
    demodb.close()
    
    CName = StringVar()
    Cid = StringVar()
    BQty = StringVar()
    Btot = StringVar()
    Bpaid = StringVar()
    Bal = StringVar()

    CName.set(CustDet[0])
    Cid.set(CustDet[1])
    BQty.set(CustDet[2])
    Btot.set(CustDet[3])
    Bpaid.set(CustDet[4])
    Bal.set(CustDet[5])

    lCName = Label(up, text="Name:", font=text_format)
    lCName.grid(row=0, column=0, sticky=W)
    eCName = Entry(up, textvariable=CName, width=18, font=text_format,state='readonly')
    eCName.grid(row=0, column=1, sticky=W, padx=10, pady=5)

    lBdis = Label(up, text="CustID:", font=text_format)
    lBdis.grid(row=0, column=2, sticky=W)
    eBdis = Label(up, text=Cid.get(), font=text_format)
    eBdis.grid(row=0, column=3, sticky=W, padx=10, pady=5)

    lType = Label(up, text="No. of Orders:", font=text_format)
    lType.grid(row=1, column=0, sticky=W)
    eType = Label(up, text=BQty.get(), font=text_format)
    eType.grid(row=1, column=1, sticky=W, padx=10, pady=5)

    lBtot = Label(up, text="Total:", font=text_format)
    lBtot.grid(row=1, column=2, sticky=W)
    eBtot = Label(up, text=Btot.get(), font=text_format)
    eBtot.grid(row=1, column=3, sticky=W, padx=10, pady=5)

    lBnet = Label(up, text="Paid:", font=text_format)
    lBnet.grid(row=3, column=0, sticky=W)
    eBnet = Label(up, text=Bpaid.get(), font=text_format)
    eBnet.grid(row=3, column=1, sticky=W, padx=10, pady=5)
    
    lPay = Label(up, text="Balance:", font=text_format)
    lPay.grid(row=3, column=2, sticky=W)
    ePay = Label(up, text=Bal.get(), font=text_format)
    ePay.grid(row=3, column=3, sticky=W, padx=10, pady=5)

    def Close():
        right1.destroy()
        Main()

    def Back():
        right1.destroy()
        View(4)

    scroll = Scrollbar(down)
    scroll.pack(side=RIGHT, fill=Y)
    tv = ttk.Treeview(down, columns=('col0', 'col1', 'col2', 'col3', 'col4', 'col5', 'col6', 'col7'), show='headings',
                      height=10, yscrollcommand=scroll.set, style="mystyle.Treeview")
    tv.pack()
    scroll.config(command=tv.yview)

    tv.heading('col0', text='Bill No.')
    tv.heading('col1', text='Date')
    tv.heading('col2', text='Type')
    tv.heading('col3', text='Qty')
    tv.heading('col4', text='Dis (%)')
    tv.heading('col5', text='Total')
    tv.heading('col6', text='Balance')
    tv.heading('col7', text='Paid')

    tv.column('col0', anchor=CENTER, width=90)
    tv.column('col1', anchor=CENTER, width=75)
    tv.column('col2', anchor=CENTER, width=55)
    tv.column('col3', anchor=CENTER, width=40)
    tv.column('col4', anchor=CENTER, width=55)
    tv.column('col5', anchor=CENTER, width=100)
    tv.column('col6', anchor=CENTER, width=100)
    tv.column('col7', anchor=CENTER, width=100)

    for i in Bills:
        tup = list(i)
        zz = str(i[1]).split()[0]
        tup[1] = zz.split('-')[2] + '/' + zz.split('-')[1] + '/' + zz.split('-')[0]
        tv.insert('', 'end', values=tup)

    button1 = Button(side, text="Home", **button_format, width=12, command=Close)
    button1.grid(row=5, column=0, sticky=E, pady=10, padx=10)

    button2 = Button(side, text="Back", **button_format, width=12, command=Back)
    button2.grid(row=4, column=0, sticky=E, pady=10, padx=10)


""" Program Start """
window = Tk()

""" Menu bar """
menu = Menu(window,background=bgcol)
menu.add_command(label="Bulk Entry", command=sql_csv)
menu.add_command(label="Repair", command=Ins.install_Old)
menu.add_command(label="Search", command=Search)
menu.add_separator()
menu.add_command(label="Help", command=Helpwind)
menu.add_command(label="Exit", command=exit_prog)

""" Window Attributies """
window.config(menu=menu)
window.iconbitmap(r'modules/1.ico')
window.config(bg=bgcol)
window.title('Bill System')
window.geometry("960x540")
window.resizable(False, False)
window.protocol("WM_DELETE_WINDOW", exit_prog)
window.focus_force()

""" Treeview Style """
style = ttk.Style()
style.configure("mystyle.Treeview.Heading", font=("arial", 10, 'bold'))
style.configure("mystyle.Treeview", font=("arial", 10))

try:
    if pas == '':
        window.destroy()
        raise SystemExit
    else:
        demodb = mysql.connect(**DB)
        cursor = demodb.cursor()
        cursor.execute('SELECT * FROM supplier;')
        demodb.close()
except mysql.errors.ProgrammingError:
    sql_data_create()

right = Frame(window, bg=bgcol)
right.grid(column=0,row=1)

Update_lst(4) # First intialize
Main()  # Start Home Screen

window.mainloop()

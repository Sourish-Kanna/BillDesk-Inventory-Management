# GUI Source Code

print("# Update & Change SQL_Check, SQL_Entry & SQL_Update after Bill Module")

""" Import Section """
from modules.SQL_Check import Check_Database
from time import strftime as stime
import mysql.connector as mysql
from tkinter import messagebox
from datetime import datetime
from modules.PDF import Pdf
from tkinter import ttk
from tkinter import *


""" Constants """
pas, us = 'Ramsour1_2003', 'root'
bgcol:str = "#add8e6"
text_format:tuple = ("arial", 14)
unitlst:tuple = ('Select Unit', 'Kgs', 'Nos')
button_format:dict = {"bg":"brown", "fg":"white", "font":text_format}
DB:dict = {"user": us, "passwd": pas, "database": "project", "host": "localhost"}
gstlst:tuple = ('Select GST Rate', '00.00 %', '05.00 %', '12.00 %', '18.00 %', '28.00 %')

""" Working Lists """
supplst: list[str] = [] # To select supplier in product Add
prodlst: list[str] = [] # To show product in Bill
custlst: list[str] = [] # To show customer in Bill
prodname:dict = {} # {PID:Name} To Display in modify screen
suppname:dict = {} # {SID:Name} To Display in modify screen
prodqty:dict = {}  # {PID:Qty}  To Check Avaible Stock


""" Other Functions """
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
        pass
        # right1.destroy()
        # Main()

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
        Add()
        ePName.focus()

    def Next_dis(event):
        eBdisc.focus()

    def Next_Bill(event):
        Check()

    def Next_Modify(event):
        Modify()

    def Or_dis(event):
        eBdis.focus()
    
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
        
        Check()

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

        Check()

    """ Calculate """
    def ProdN(event): # Prodname search
        value = ePName.get()
        nonlocal Pname
        if value == '' or value == 'Select Product':
            # Pname = sorted(Pname[1:])
            data = Pname
        else:
            data = []
            for item in Pname:
                if value.lower() in item.lower():
                    data.append(item)
            # data = sorted(data[1:])
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
        print(btotal)
        eBnet.configure(text=f"₹{Total.get()}")

    def Credit(): # Credit
        if Typ.get() == "Full" :
            Adv.set("")
            ePay.config(state="disabled")
        else:
            ePay.config(state="normal")

    """ Side Panel """
    def Add(): # Add
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
        
        # Ending Part
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

    def Modify():
        if tv.focus() == '':
            return

        nonlocal sel,sel_tup
        select = tv.focus()

        if sel==select: # Modified
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
            eQty.bind('<Return>', Next_Prod1)
            ePName.focus()
            return
        
        sel = select
        sel_tup = tv.item(select)['values']  # (Name,qty,gst,unit,rate,price)
        Qty.set(sel_tup[1])
        eQty.focus()
        eQty.bind('<Return>', Next_Modify)

    def Check(): # Show/Check Before Billing
        #sql_update_other 1 put stk directly from treeview
        pass

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

    lBdisc = Label(up, text="Discount(₹):", font=text_format)
    lBdisc.grid(row=2, column=0, sticky=W)
    eBdisc = Entry(up, textvariable=Dis_ru, width=7, font=text_format)
    eBdisc.grid(row=2, column=1, sticky=W, padx=10, pady=5)
    eBdisc.bind('<Return>', Dis_rup)
    eBdisc.bind('<Shift_L>', Or_dis)
    eBdisc.bind('<Shift_R>', Or_dis)

    lBdis = Label(up, text="Discount(%):", font=text_format)
    lBdis.grid(row=2, column=2, sticky=W)
    eBdis = Entry(up, textvariable=Dis_per, width=7, font=text_format)
    eBdis.grid(row=2, column=3, sticky=W, padx=10, pady=5)
    eBdis.bind('<Return>', Dis_perc)
    eBdis.bind('<Shift_L>', Next_dis)
    eBdis.bind('<Shift_R>', Next_dis)

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
    ePay.bind('<Return>', Next_Bill)

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

    button1 = Button(side, text="Edit", **button_format, width=12 ,command=Modify)
    button1.grid(row=1, column=0, sticky=W, pady=10, padx=10)

    button2 = Button(side, text="Delete", **button_format, width=12, command=Delete)
    button2.grid(row=2, column=0, sticky=W, pady=10, padx=10)

    button3 = Button(side, text="Check Out", **button_format, width=12, command=Check)
    button3.grid(row=3, column=0, sticky=W, pady=10, padx=10)

    button3 = Button(side, text="Clear", **button_format, width=12, command=Clear)
    button3.grid(row=4, column=0, sticky=W, pady=10, padx=10)

    button5 = Button(side, text="Home", **button_format, width=12, command=Close)
    button5.grid(row=5, column=0, sticky=E, pady=10, padx=10)


""" Program Start """
window = Tk()


""" Window Attributies """
window.iconbitmap(r'modules/1.ico')
window.config(bg=bgcol)
window.title('Bill System')
window.geometry("960x540")
window.resizable(False, False)

window.focus_force()

""" Treeview Style """
style = ttk.Style()
style.configure("mystyle.Treeview.Heading", font=("arial", 10, 'bold'))
style.configure("mystyle.Treeview", font=("arial", 10))


right = Frame(window, bg=bgcol)
right.grid(column=0,row=1)

Update_lst(4) # First intialize
Bill()  # Start Home Screen

window.mainloop()

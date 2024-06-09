# SQL_Entry Source Code
import mysql.connector
DBname:str = "project"

def Create(tab_name, tab_items, us, pas):
    """Create MySQL Rows

    Tuple Order :-
    
        1] supplier   --> (SuppID, SuppName, SuppAdd, SuppPhone, SuppEmail) \n
        2] product    --> (SuppID, ProdID, ProdName, ProdCost, ProdRate, ProdGST, ProdUnit, ProdStock ) \n
        3] bill       --> (BillNos, CustID, Type, BillDate, Billser, Paid, Dis_per, Dis_ru, BillNet,Balance) \n
        4] billdetail --> (BillNos, ProdID, ProdQty, Prodtot, Billser) \n
        5] cust       --> (CustID, CustName, Qty, Balance, Total)
    """

    if tab_name == 0: # All Print
        conn = mysql.connector.connect(host="localhost", user=us, passwd=pas, database=DBname)
        cursor = conn.cursor()
        abc = ("SELECT * FROM supplier;", "SELECT * FROM product;",
               "SELECT * FROM bill;", "SELECT * FROM billdetail;", "SELECT * FROM cust;")

        for i in abc:
            cursor.execute(i)
            print(cursor)
            lst = cursor.fetchall()
            ab = cursor.rowcount
            for a in range(0, ab):
                print(lst[a])
            print()

        conn.close()

    elif tab_name == 1:  # supplier
        SuppID, SuppName, SuppAdd, SuppPhone, SuppEmail = tab_items
        conn = mysql.connector.connect(host="localhost", user=us, passwd=pas, database=DBname)
        cursor = conn.cursor()
        sql = f"INSERT INTO supplier(SuppID,SuppName,Addr,Phone,Email) " \
              f"VALUES ('{SuppID}','{SuppName}','{SuppAdd}','{SuppPhone}','{SuppEmail}');"
        cursor.execute(sql)
        conn.commit()
        conn.close()

    elif tab_name == 2:  # product
        SuppID, ProdID, ProdName, ProdCost, ProdRate, ProdGST, ProdUnit, ProdStock = tab_items
        conn = mysql.connector.connect(host="localhost", user=us, passwd=pas, database=DBname)
        cursor = conn.cursor()
        sql = f"INSERT INTO product(SuppID,ProdID,Name,CP,SP,GST,Unit,Stock) " \
              f"VALUES ('{SuppID}','{ProdID}','{ProdName}',{ProdCost},{ProdRate},'{ProdGST}','{ProdUnit}',{ProdStock}); "
        cursor.execute(sql)
        conn.commit()
        conn.close()

    elif tab_name == 3:  # bill
        BillNos, CustID, Type, BillDate, Billser, Paid, Dis_per, Dis_ru, BillNet, Balance = tab_items
        conn = mysql.connector.connect(host="localhost", user=us, passwd=pas, database=DBname)
        cursor = conn.cursor()
        sql = f"INSERT INTO bill(BillID,CustID,Type,Date,Qty,Paid,Dis_per,Dis_ru,Total,Balance) " \
              f"VALUES ('{BillNos}','{CustID}','{Type}','{BillDate}',{Billser}, {Paid},{Dis_per},{Dis_ru},{BillNet}, {Balance});"
        cursor.execute(sql)
        conn.commit()
        conn.close()

    elif tab_name == 4:  # billdetail
        BillNos, ProdID, ProdQty, Prodtot, Billser = tab_items
        conn = mysql.connector.connect(host="localhost", user=us, passwd=pas, database=DBname)
        cursor = conn.cursor()
        sql = f"INSERT INTO billdetail(BillID,ProdID,Qty,Total,Serial) " \
              f"VALUES ('{BillNos}','{ProdID}','{ProdQty}','{Prodtot}','{Billser}');"
        cursor.execute(sql)
        conn.commit()
        conn.close()

    elif tab_name == 5:  # cust
        CustID, CustName, Qty, Balance, Total = tab_items
        conn = mysql.connector.connect(host="localhost", user=us, passwd=pas, database=DBname)
        cursor = conn.cursor()
        sql = f"select * from cust where CustID='{CustID}';"
        cursor.execute(sql)
        lst = cursor.fetchall()
        if lst==[]:
            sql = f"INSERT INTO cust(CustID,Name,Qty,Balance,Total) "\
                  f"VALUES ('{CustID}','{CustName}','{Qty}','{Balance}','{Total}');"
            cursor.execute(sql)
            conn.commit()
        else:
            Qty = lst[0][2]+Qty
            Balance = lst[0][3]+Balance
            Total = lst[0][4]+Total
            sql = f"UPDATE cust set Qty='{Qty}',Balance='{Balance}',Total='{Total}' where CustID ='{CustID}';"
            cursor.execute(sql)
            conn.commit()
        conn.close()


if __name__ == '__main__':
    # from SQL_TPass import Pass
    # pas, us = Pass()
    pas, us = 'Ramsour1_2003', 'root'
    if pas == None:
        from time import sleep
        sleep(2.5)
        raise SystemExit
    a = int(input('0-View\n1-Supplierdetails\n2-Product\n3-Bill\n4-Billdetails\n5-custdetail\nNo: '))
    if a == 0:
        Create(a, (), us, pas)
    else:
        b = eval(input("Tuple: "))
        Create(a, b, us, pas)
        a = 0
        Create(a, (), us, pas)

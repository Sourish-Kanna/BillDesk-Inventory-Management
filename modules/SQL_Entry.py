#SQL_Entry Source Code
import mysql.connector


def Create(tab_name, tab_items, us, pas):
    """Create MySQL Tables

    Tuple Order :-
    supplier   --> (SuppID, SuppName, SuppAdd, SuppPhone, SuppEmail)
    product    --> (SuppID, ProdID, ProdName)
    bill       --> (BillNos, CustID, CustName, BillDate, BillAmt, BillDisc, BillNet)
    billdetail --> (BillNos, ProdID, ProdQty, Prodtot, Billser)"""
    if tab_name == 0:
        conn = mysql.connector.connect(host="localhost",
                                       user=us,
                                       passwd=pas,
                                       database="projectold")
        cursor = conn.cursor()
        abc = ("SELECT * FROM supplier;", "SELECT * FROM product;",
               "SELECT * FROM bill;", "SELECT * FROM billdetail;")

        for i in abc:
            cursor.execute(i)
            print(cursor)
            lst=cursor.fetchall()
            ab=cursor.rowcount
            for a in range(0,ab):
                print(lst[a])
            print()

        conn.close()

    elif tab_name == 1:  # supplier
        SuppID, SuppName, SuppAdd, SuppPhone, SuppEmail = tab_items
        conn = mysql.connector.connect(host="localhost",
                                       user=us,
                                       passwd=pas,
                                       database="projectold")
        cursor = conn.cursor()
        sql = f"INSERT INTO supplier(SuppID,SuppName,Addr,Phone,Email) " \
              f"VALUES ('{SuppID}','{SuppName}','{SuppAdd}','{SuppPhone}','{SuppEmail}');"
        cursor.execute(sql)
        conn.commit()
        conn.close()

    elif tab_name == 2:  # product
        SuppID, ProdID, ProdName, ProdCost, ProdRate, ProdGST, ProdUnit, ProdStock = tab_items
        conn = mysql.connector.connect(host="localhost",
                                       user=us,
                                       passwd=pas,
                                       database="projectold")
        cursor = conn.cursor()
        sql = f"INSERT INTO product(SuppID,ProdID,Name,CP,SP,GST,Unit,Stock) VALUES ('{SuppID}','{ProdID}','{ProdName}"\
              f"',{ProdCost},{ProdRate},'{ProdGST}','{ProdUnit}',{ProdStock}); "
        cursor.execute(sql)
        conn.commit()
        conn.close()

    elif tab_name == 3:  # bill
        BillNos, CustID, CustName, BillDate, Billser, BillAmt, BillDisc, BillNet = tab_items
        conn = mysql.connector.connect(host="localhost",
                                       user=us,
                                       passwd=pas,
                                       database="projectold")
        cursor = conn.cursor()
        sql = f"INSERT INTO bill(BillID,CustID,Name,Date,Qty,Amt,Disc,Total) " \
              f"VALUES ('{BillNos}','{CustID}','{CustName}','{BillDate}',{Billser}, {BillAmt},{BillDisc},{BillNet});"
        cursor.execute(sql)
        conn.commit()
        conn.close()

    elif tab_name == 4:  # billdetail
        BillNos, ProdID, ProdQty, Prodtot, Billser = tab_items
        conn = mysql.connector.connect(host="localhost",
                                       user=us,
                                       passwd=pas,
                                       database="projectold")
        cursor = conn.cursor()
        sql = f"INSERT INTO billdetail(BillID,ProdID,Qty,Total,Serial) " \
              f"VALUES ('{BillNos}','{ProdID}','{ProdQty}','{Prodtot}','{Billser}');"
        cursor.execute(sql)
        conn.commit()
        conn.close()


if __name__ == '__main__':
    from SQL_TPass import Pass
    pas, us = Pass()
    if pas==None:
        print('Wrong Password')
        from time import sleep
        sleep(2.5)
        raise SystemExit
    a = int(input('0-View\n1-Supplierdetails\n2-Product\n3-Productdetails\n4-Billl\n5-Billdetails\nNo: '))
    if a == 0:
        Create(a, (), us, pas)
    else:
        b = eval(input("Tuple: "))
        Create(a, b, us, pas)
        a = 0
        Create(a, (), us, pas)
#SQL_Update Source Code
import mysql.connector

DBname:str = "project"
DBhost:str = "localhost"

def Update_row(tab_name, tab_items, us, pas):
    """Modify MySQL Row

    Update tables
    
    Tuple Order :-
        1] supplier   --> (SuppID, SuppName, SuppAdd, SuppPhone, SuppEmail) \n
        2] product    --> (ProdID,ProdName,ProdCost,ProdRate,ProdGST,ProdUnit,ProdStock) \n
    """

    if tab_name == 1:  # supplier
        SuppID, SuppName, SuppAdd, SuppPhone, SuppEmail = tab_items
        conn = mysql.connector.connect(host=DBhost, user=us, passwd=pas, database=DBname)
        cursor = conn.cursor()
        sql = f"UPDATE supplier SET SuppName = '{SuppName}', Addr= '{SuppAdd}'," \
              f" Phone= '{SuppPhone}', Email= '{SuppEmail}' WHERE SuppID='{SuppID}';"
        cursor.execute(sql)
        conn.commit()
        conn.close()

    elif tab_name == 2:  # product
        ProdID, ProdName, ProdCost, ProdRate, ProdGST, ProdUnit, ProdStock = tab_items
        conn = mysql.connector.connect(host=DBhost, user=us, passwd=pas, database=DBname)
        cursor = conn.cursor()
        sql = f"UPDATE product SET Name = '{ProdName}', CP='{ProdCost}', SP='{ProdRate}', " \
              f"GST='{ProdGST}', Stock='{ProdStock}', Unit='{ProdUnit}' WHERE ProdID='{ProdID}';"
        cursor.execute(sql)
        conn.commit()
        conn.close()


def Update_column(tab_name, tab_items, us, pas):
    """Modify MySQL Columns

    Update stocks, Hide Status

    Tuple Order :-
        1] Update stock after Billing --> ProdID,Stock \n
        2] Hide Supplier --> SuppID, Stat \n
        3] Hide Product --> ProdID, Stat \n
        4] Update Cust Total after Billing --> CustID,balance,total
    """

    if tab_name == 1:  # Update stock after Billing
        pid, stk = tab_items
        conn = mysql.connector.connect(host=DBhost, user=us, passwd=pas, database=DBname)
        cursor = conn.cursor()
        sql = f"SELECT Stock FROM Product WHERE ProdID='{pid}';"
        cursor.execute(sql)
        qty = cursor.fetchone()[0]
        stk = qty-stk
        sql = f"UPDATE Product set Stock={stk} where ProdID='{pid}';"
        cursor.execute(sql)
        conn.commit()
        conn.close()

    elif tab_name == 2:  # Hide Supplier
        SuppID, Stat = tab_items
        conn = mysql.connector.connect(host=DBhost, user=us, passwd=pas, database=DBname)
        cursor = conn.cursor()
        sql = f"SELECT Hide FROM Supplier WHERE SuppID='{SuppID}'"
        cursor.execute(sql)
        aa = cursor.fetchone()[0]
        conn.close()
        if aa == 'N' and Stat == 1:
            sql = f"UPDATE Supplier set Hide='Y' where SuppID='{SuppID}';"
            conn = mysql.connector.connect(host=DBhost, user=us, passwd=pas, database=DBname)
            cursor = conn.cursor()
            cursor.execute(sql)
            conn.commit()
            conn.close()
            return 1
        elif aa == 'Y' and Stat == 0:
            sql = f"UPDATE Supplier set Hide='N' where SuppID='{SuppID}';"
            conn = mysql.connector.connect(host=DBhost, user=us, passwd=pas, database=DBname)
            cursor = conn.cursor()
            cursor.execute(sql)
            conn.commit()
            conn.close()
            return 1
        else:
            return 0

    elif tab_name == 3:  # Hide Product
        ProdID, Stat = tab_items
        conn = mysql.connector.connect(host=DBhost, user=us, passwd=pas, database=DBname)
        cursor = conn.cursor()
        sql = f"SELECT Hide FROM Product WHERE ProdID='{ProdID}'"
        cursor.execute(sql)
        aa = cursor.fetchone()[0]
        conn.close()
        if aa == 'N' and Stat == 1:
            sql = f"UPDATE Product set Hide='Y' where ProdID='{ProdID}';"
            conn = mysql.connector.connect(host=DBhost, user=us, passwd=pas, database=DBname)
            cursor = conn.cursor()
            cursor.execute(sql)
            conn.commit()
            conn.close()
            return 1
        elif aa == 'Y' and Stat == 0:
            sql = f"UPDATE Product set Hide='N' where ProdID='{ProdID}';"
            conn = mysql.connector.connect(host=DBhost, user=us, passwd=pas, database=DBname)
            cursor = conn.cursor()
            cursor.execute(sql)
            conn.commit()
            conn.close()
            return 1
        else:
            return 0
    
    elif tab_name ==4:  # Update Cust Total after Billing
        cid, bal, tot = tab_items
        conn = mysql.connector.connect(host=DBhost, user=us, passwd=pas, database=DBname)
        cursor = conn.cursor()
        sql = f"SELECT Qty,balance, total FROM cust WHERE CustID='{cid}';"
        cursor.execute(sql)
        qty,old_bal,old_tot = cursor.fetchone()
        bal = old_bal+bal
        tot = old_tot+tot
        qty = qty+1
        sql = f"UPDATE cust set balance={bal} where CustID='{cid}';"
        cursor.execute(sql)
        sql = f"UPDATE cust set total={tot} where CustID='{cid}';"
        cursor.execute(sql)
        sql = f"UPDATE cust set Qty={qty} where CustID='{cid}';"
        cursor.execute(sql)
        conn.commit()
        conn.close()


if __name__ == '__main__':
    from SQL_TPass import Pass
    pas, us = Pass()
    if pas==None:
        from time import sleep
        sleep(2.5)
        raise SystemExit
    a = int(input('Update Entire Row\n0-Pass\n1-Supplier\n2-Product\nNo: '))
    if a!=0:
        b = eval(input("Tuple: "))
        Update_row(a, b, us, pas)
    print()
    a = int(input('Update Induvial column\n0-Pass\n1-Stock\n2-Sup Status\n3-Prod Status\n4-cust\nNo: '))
    if a!=0:
        b = eval(input("Tuple: "))
        print(Update_column(a, b, us, pas))


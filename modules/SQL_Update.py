#SQL_Update Source Code
import mysql.connector
DBname:str = "project"

def Update_All(tab_name, tab_items, us, pas):
    """Modify MySQL Row

    Update tables
    
    Tuple Order :-
    1] supplier   --> (SuppID, SuppName, SuppAdd, SuppPhone, SuppEmail)
    2] product    --> (ProdID,ProdName,ProdCost,ProdRate,ProdGST,ProdUnit,ProdStock)"""

    if tab_name == 1:  # supplier
        SuppID, SuppName, SuppAdd, SuppPhone, SuppEmail = tab_items
        conn = mysql.connector.connect(host="localhost", user=us, passwd=pas, database=DBname)
        cursor = conn.cursor()
        sql = f"UPDATE supplier SET SuppName = '{SuppName}', Addr= '{SuppAdd}'," \
              f" Phone= '{SuppPhone}', Email= '{SuppEmail}' WHERE SuppID='{SuppID}';"
        cursor.execute(sql)
        conn.commit()
        conn.close()

    elif tab_name == 2:  # product
        ProdID, ProdName, ProdCost, ProdRate, ProdGST, ProdUnit, ProdStock = tab_items
        conn = mysql.connector.connect(host="localhost", user=us, passwd=pas, database=DBname)
        cursor = conn.cursor()
        sql = f"UPDATE product SET Name = '{ProdName}', CP='{ProdCost}', SP='{ProdRate}', " \
              f"GST='{ProdGST}', Stock='{ProdStock}', Unit='{ProdUnit}' WHERE ProdID='{ProdID}';"
        cursor.execute(sql)
        conn.commit()
        conn.close()


def Update_other(tab_name, tab_items, us, pas):
    """Modify MySQL Columns

    Update stocks, Hide Status

    Tuple Order :-
    1] Update stock after Billing --> ProdID,ProdStock
    2] Hide Supplier --> SuppID, Stat
    3] Hide Product --> ProdID, Stat"""

    if tab_name == 1:  # Update stock after Billing
        pid, stk = tab_items
        conn = mysql.connector.connect(host="localhost", user=us, passwd=pas, database=DBname)
        cursor = conn.cursor()
        sql = f"UPDATE Product set Stock={stk} where ProdID='{pid}';"
        cursor.execute(sql)
        conn.commit()
        conn.close()

    elif tab_name == 2:  # Hide Supplier
        SuppID, Stat = tab_items
        conn = mysql.connector.connect(host="localhost", user=us, passwd=pas, database=DBname)
        cursor = conn.cursor()
        sql = f"SELECT Hide FROM Supplier WHERE SuppID='{SuppID}'"
        cursor.execute(sql)
        aa = cursor.fetchone()[0]
        conn.close()
        if aa == 'N' and Stat == 1:
            sql = f"UPDATE Supplier set Hide='Y' where SuppID='{SuppID}';"
            conn = mysql.connector.connect(host="localhost", user=us, passwd=pas, database=DBname)
            cursor = conn.cursor()
            cursor.execute(sql)
            conn.commit()
            conn.close()
            return 1
        elif aa == 'Y' and Stat == 0:
            sql = f"UPDATE Supplier set Hide='N' where SuppID='{SuppID}';"
            conn = mysql.connector.connect(host="localhost", user=us, passwd=pas, database=DBname)
            cursor = conn.cursor()
            cursor.execute(sql)
            conn.commit()
            conn.close()
            return 1
        else:
            return 0

    elif tab_name == 3:  # Hide Product
        ProdID, Stat = tab_items
        conn = mysql.connector.connect(host="localhost", user=us, passwd=pas, database=DBname)
        cursor = conn.cursor()
        sql = f"SELECT Hide FROM Product WHERE ProdID='{ProdID}'"
        cursor.execute(sql)
        aa = cursor.fetchone()[0]
        conn.close()
        if aa == 'N' and Stat == 1:
            sql = f"UPDATE Product set Hide='Y' where ProdID='{ProdID}';"
            conn = mysql.connector.connect(host="localhost", user=us, passwd=pas, database=DBname)
            cursor = conn.cursor()
            cursor.execute(sql)
            conn.commit()
            conn.close()
            return 1
        elif aa == 'Y' and Stat == 0:
            sql = f"UPDATE Product set Hide='N' where ProdID='{ProdID}';"
            conn = mysql.connector.connect(host="localhost", user=us, passwd=pas, database=DBname)
            cursor = conn.cursor()
            cursor.execute(sql)
            conn.commit()
            conn.close()
            return 1
        else:
            return 0


if __name__ == '__main__':
    from SQL_TPass import Pass
    #pas, us = Pass()
    pas, us = 'Ramsour1_2003', 'root'
    if pas==None:
        from time import sleep
        sleep(2.5)
        raise SystemExit
    a = int(input('Update Entire Row\n0-Pass\n1-Supplier\n2-Product\nNo: '))
    if a!=0:
        b = eval(input("Tuple: "))
        Update_All(a, b, us, pas)
    print()
    a = int(input('Update Induvial column\n0-Pass\n1-Stock\n2-Sup Status\n3-Prod Status\nNo: '))
    if a!=0:
        b = eval(input("Tuple: "))
        print(Update_other(a, b, us, pas))

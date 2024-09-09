#SQL_Update Source Code
import mysql.connector
DBname:str = "project"
DBhost:str = "localhost"

def Check_Database(tab_name:int, tab_items:tuple, us:str, pas:str):
    """Check MySQL Columns
    
    Check Various things in database

    Tuple Order :-
        1] Check stock before Billing --> ProdID,ProdStock \n
        2] Check Customer name --> CID,count
    """

    if tab_name == 1:  # Check stock before Billing
        pid, stk = tab_items
        conn = mysql.connector.connect(host=DBhost, user=us, passwd=pas, database=DBname)
        cursor = conn.cursor()
        sql = f"SELECT Stock FROM Product WHERE ProdID='{pid}';"
        cursor.execute(sql)
        qty = cursor.fetchone()[0]
        conn.close()
        if qty-stk>=0:
            return True,qty-stk
        else:
            return False,qty
        
    elif tab_name == 2: # Check Customer name
        cname,date = tab_items
        conn = mysql.connector.connect(host=DBhost, user=us, passwd=pas, database=DBname)
        cursor = conn.cursor()
        sql = f"SELECT cust.CustID, COUNT(bill.BillID) AS BillCount FROM cust LEFT JOIN bill ON cust.CustID = bill.CustID \
            AND bill.Date LIKE '%{date}%' WHERE cust.Name = '{cname}' GROUP BY cust.CustID UNION SELECT cust.CustID, 0 AS BillCount \
            FROM cust WHERE cust.Name = '{cname}' AND NOT EXISTS ( SELECT 1 FROM bill JOIN cust ON cust.CustID = bill.CustID \
            WHERE bill.Date LIKE '{date}' AND cust.Name = '{cname}' );"
        cursor.execute(sql)
        cid,count = cursor.fetchone()
        conn.close()
        return cid,count
 

if __name__ == '__main__':
    from SQL_TPass import Pass
    pas, us = Pass()
    if pas==None:
        from time import sleep
        sleep(2.5)
        raise SystemExit
    print(Check_Database(2,("Sourish","2024-06-05"),us,pas))
    
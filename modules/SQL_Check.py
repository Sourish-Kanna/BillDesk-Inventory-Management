#SQL_Update Source Code
import mysql.connector
DBname:str = "project"
DBhost:str = "localhost"

def Check_Database(tab_name:int, tab_items:tuple, us:str, pas:str):
    """Check MySQL Columns

    Check stocks

    Tuple Order :-
    1] Check stock before Billing --> ProdID,ProdStock"""

    if tab_name == 1:  # Update stock after Billing
        pid, stk = tab_items
        conn = mysql.connector.connect(host=DBhost, user=us, passwd=pas, database=DBname)
        cursor = conn.cursor()
        sql = f"SELECT Stock FROM Product WHERE ProdID='{pid}';"
        cursor.execute(sql)
        qty = cursor.fetchone()[0]
        conn.close()
        if qty-stk>0:
            return True,qty-stk
        else:
            return False,qty
 

if __name__ == '__main__':
    from SQL_TPass import Pass
    #pas, us = Pass()
    pas, us = 'Ramsour1_2003', 'root'
    if pas==None:
        from time import sleep
        sleep(2.5)
        raise SystemExit
    print(Check_Database(1,("S01P01",100),us,pas))
    
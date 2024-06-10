#SQL_Datacreate Source Code
import mysql.connector
DBname:str = "project"

def SQLTAB(us, pas):
    """Create SQL Table"""
    # Create tables
    conn = mysql.connector.connect(host="localhost", user=us, passwd=pas, database=DBname)
    cursor = conn.cursor()
    sql = 'CREATE TABLE supplier( SuppID CHAR(3) PRIMARY KEY NOT NULL, SuppName VARCHAR(250) NOT NULL DEFAULT ' \
          '\'Supplier\', Addr VARCHAR(250) DEFAULT \'No Address\', Phone VARCHAR(15) NOT NULL , Email VARCHAR(250) ' \
          'DEFAULT \'No Email\', Hide ENUM(\'Y\',\'N\') NOT NULL DEFAULT \'N\'); '
    cursor.execute(sql)
    sql = 'CREATE TABLE product( SuppID CHAR(3) NOT NULL, FOREIGN KEY (SuppID) REFERENCES supplier(SuppID), ' \
          'ProdID CHAR(6) PRIMARY KEY NOT NULL, Name VARCHAR(250) NOT NULL DEFAULT \'Product\', CP FLOAT NOT NULL, ' \
          'SP FLOAT NOT NULL, GST ENUM(\'00.00\', \'05.00\', \'12.00\', \'18.00\', \'28.00\') NOT NULL DEFAULT ' \
          '\'18.00\', Unit ENUM(\'Kgs\',\'Nos\') NOT NULL DEFAULT \'Kgs\' , Stock INT NOT NULL, Hide ENUM(\'Y\',' \
          '\'N\') NOT NULL DEFAULT \'N\'); '
    cursor.execute(sql)
    sql = 'CREATE TABLE cust(CustID CHAR(3) NOT NULL PRIMARY KEY, Name VARCHAR(50) NOT NULL DEFAULT ' \
          '\'Customer\', Qty INT NOT NULL, Balance FLOAT NOT NULL, Total FLOAT NOT NULL); '
    cursor.execute(sql)
    sql = 'CREATE TABLE bill(BillID CHAR (12) NOT NULL PRIMARY KEY, CustID CHAR(3) NOT NULL ' \
          'REFERENCES cust(CustID), Date DATETIME NOT NULL, Qty INT NOT NULL, Total FLOAT NOT NULL, '\
          'Type ENUM(\'Cash\', \'Credit\') NOT NULL, Balance FLOAT NOT NULL, Paid FLOAT NOT NULL, '\
          'Dis_per FLOAT NOT NULL, Dis_ru FLOAT NOT NULL);'
    cursor.execute(sql)
    sql = 'CREATE TABLE billdetail(BillID CHAR (12) NOT NULL, FOREIGN KEY (BillID) REFERENCES bill(BillID), ' \
          'ProdID CHAR(6) NOT NULL, FOREIGN KEY (ProdID) REFERENCES product(ProdID), Qty INT NOT NULL, Total Float ' \
          'NOT NULL, Serial INT NOT NULL DEFAULT \'1\'); '
    cursor.execute(sql)
    conn.commit()
    conn.close()


def SQL(us, pas):
    """Create SQL Database"""
    conn = mysql.connector.connect(host="localhost", user=us, passwd=pas)
    cursor = conn.cursor()
    cursor.execute("DROP database IF EXISTS project")
    sql = "CREATE database project;"
    cursor.execute(sql)
    conn.commit()
    conn.close()
    SQLTAB(us, pas)


def del_sql(us, pas):
    """Delete SQL Database"""
    conn = mysql.connector.connect(host="localhost", user=us, passwd=pas)
    cursor = conn.cursor()
    cursor.execute("DROP database IF EXISTS project")
    conn.commit()
    conn.close()


if __name__ == '__main__':
    from SQL_TPass import Pass
    pas, us = Pass()
    if pas==None:
        from time import sleep
        sleep(2.5)
        raise SystemExit
    if input('do you want to delete database enter 1 for yes ') == '1':
        del_sql(us,pas)
    else:
        SQL(us,pas)
        print("Done")
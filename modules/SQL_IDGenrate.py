#SQL_IDGenrate Source Code
from mysql.connector import connect


def supp_gen(us, pas):
    demodb = connect(host="localhost", user=us, passwd=pas, database="projectold")
    cursor = demodb.cursor()
    cursor.execute(f"SELECT SuppID FROM supplier;")
    for i in cursor:
        if not bool(i):
            SuppID = 'S00'
        else:
            SuppID = max(i)

    try:
        if SuppID[-1] == '9':
            pass
    except:
        SuppID = 'S00'

    if SuppID[-1] == '9':
        b = str(int(SuppID[-2]) + 1)
        SuppID = 'S' + b + "0"
    elif SuppID[-1] != '9':
        a = str(int(SuppID[-1]) + 1)
        b = str(int(SuppID[-2]))
        SuppID = 'S' + b + a
    demodb.close()
    return SuppID


def prod_gen(SuppID, us, pas):
    demodb = connect(host="localhost", user=us, passwd=pas, database="projectold")
    cursor = demodb.cursor()
    cursor.execute(f"SELECT ProdID FROM product WHERE SuppID = '{SuppID}'")
    for i in cursor:
        ProdID = i[-1]
    try:
        if ProdID[0] == 'S':
            pass
    except:
        ProdID = SuppID + 'P00'

    if ProdID[-1] == '9':
        b = str(int(ProdID[-2]) + 1)
        ProdID = ProdID[0:4] + b + "0"
    elif ProdID[-1] != '9':
        a = str(int(ProdID[-1]) + 1)
        b = str(int(ProdID[-2]))
        ProdID = ProdID[0:4] + b + a

    demodb.close()
    return ProdID


def cust_gen(CustName, us, pas):
    demodb = connect(host="localhost", user=us, passwd=pas, database="projectold")
    cursor = demodb.cursor()
    lst = dict()
    cursor.execute(f"SELECT CustID,Name FROM bill;")
    for i in cursor:
        lst[i[1]] = i[0]

    if CustName in lst:
        CustID = lst[CustName]
        Nomore = True

    elif not bool(lst):
        CustID = 'C00'
        Nomore = False

    else:
        CustID = max(lst.values())
        Nomore = False

    if not Nomore:
        if CustID[2] == '9':
            b = str(int(CustID[1]) + 1)
            CustID = 'C' + b + "0"
        elif CustID[2] != '9':
            a = str(int(CustID[2]) + 1)
            b = str(int(CustID[1]))
            CustID = "C" + b + a
    demodb.close()
    return CustID


if __name__ == '__main__':
    from SQL_TPass import Pass
    pas, us = Pass()
    if pas==None:
        print('Wrong Password')
        from time import sleep
        sleep(2.5)
        raise SystemExit
    print('Supplier ID =', supp_gen(us, pas))
    print('Product ID =', prod_gen('S01', us, pas))
    print('Customer ID =', cust_gen('Sooo', us, pas))
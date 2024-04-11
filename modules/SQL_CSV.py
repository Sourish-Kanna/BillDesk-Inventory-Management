# SQL_CSV Source Code
import csv
from mysql.connector import connect
DBname:str = "project"

def New_csv():
    with open("Details.csv", "w", newline='') as file:
        file = csv.writer(file)
        file.writerow(['SuppName', 'SuppAdd', 'SuppPhone', 'SuppEmail',
                       'ProdName', 'CP', 'SP', 'GST',
                       'Unit', 'Stock'])
        file.writerow(['Supplier name', 'Address of supplier', 'phone no', 'sample@test.com',
                       'product 1', 'Cost price', 'selling price', 'Gst in %',
                       'Kgs or Nos', 'in number'])
        file.writerow(['Supplier name', 'Thane', '75066', 'sample@test.com',
                       'product 2', '100', '150', '5.0',
                       'Kgs', '1000'])
        file.writerow(['Supplier name', '', '', '',
                       'product 3', '100', '150', '12.0 or 18.0 or 28.0',
                       'Nos', '1000'])


def Delfile():
    from os import remove
    remove("Details.csv")


def Read_csv(us, pas):
    if __name__ == '__main__':
        from SQL_Entry import Create
        from SQL_IDGenrate import supp_gen, prod_gen
    else:
        from modules.SQL_Entry import Create
        from modules.SQL_IDGenrate import supp_gen, prod_gen

    fh = open("Details.csv", "r", newline='')
    file = csv.reader(fh)

    lst = dict()
    lst1 = dict()

    demodb = connect(host="localhost", user=us, passwd=pas, database=DBname)
    cursor = demodb.cursor()
    cursor.execute(f"SELECT SuppID,SuppName FROM supplier;")
    for i in cursor:
        lst[i[1]] = i[0]

    cursor.execute(f"SELECT ProdID,Name FROM product;")
    for i in cursor:
        lst1[i[1]] = i[0]

    demodb.close()

    for i in file:
        if i[0] == 'SuppName':
            continue
        elif i[0] == 'Supplier name':
            continue
        i[0] = i[0].title()
        i[1] = i[1].title()
        i[4] = i[4].title()
        i[5] = float(i[5])
        i[6] = float(i[6])
        if len(i[7]) == 1:
            i[7] = '0' + str(float(i[7])) + '0'
        elif len(i[7]) == 2:
            i[7] = str(float(i[7])) + '0'
        i[8] = i[8].title()
        i[9] = int(i[9])

        if i[0] in lst:
            SuppID = lst[i[0]]
            ProdID = prod_gen(SuppID, us, pas)
            SupCh = False

        else:
            SuppID = supp_gen(us, pas)
            ProdID = prod_gen(SuppID, us, pas)
            SupCh = True

        lst[i[0]] = SuppID

        lst1[SuppID] = ProdID

        tup1 = (SuppID, ProdID, i[4], i[5], i[6], i[7], i[8], i[9])
        if not SupCh:
            pass
        elif SupCh:
            tup0 = (SuppID, i[0], i[1], i[2], i[3])
            Create(1, tup0, us, pas)

        Create(2, tup1, us, pas)

    fh.close()
    Delfile()


if __name__ == '__main__':
    ch = input('1]Create\n2]Read\nChoice:')
    if ch == '1':
        New_csv()
    elif ch == '2':
        from SQL_TPass import Pass
        pas, us = Pass()
        if pas == None:
            from time import sleep
            sleep(2.5)
            raise SystemExit
        Read_csv(us, pas)

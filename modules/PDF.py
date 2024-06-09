#PDF Source Code
# Importing part  ###Pending New Revision
from reportlab.platypus import Paragraph, Table, TableStyle, LongTable
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import A4, inch
from reportlab.lib.enums import TA_CENTER
from reportlab.pdfgen import canvas
from mysql.connector import connect
from reportlab.lib import colors
from num2words import num2words


def Pdf(BillID, us, pas):
    # Create a Pdf File
    BillID = BillID.upper()
    DBhost = "localhost"
    DBname = 'project'

    # Connect to the MySQL database
    with connect(host=DBhost, user=us, passwd=pas, database=DBname) as demodb:
        cursor = demodb.cursor()

        # Fetch bill details
        cursor.execute(f"SELECT Type, Date, Qty, Paid, Dis_per, Total, Balance, Dis_ru FROM bill WHERE BillID='{BillID}';")
        type, date, BQty, b_paid, Dis_per, Total, Bal, Dis_ru= cursor.fetchone()
        time: str = str(date)[11:]
        date: str = str(date)[:10]
        Decide:int = BQty

        # Fetch customer details
        cursor.execute(f"SELECT bill.CustID, Name FROM cust JOIN bill ON cust.CustID=bill.CustID WHERE bill.BillID='{BillID}';")
        CID, Name = cursor.fetchone()

        # Fetch bill item details
        cursor.execute(f"SELECT ProdID, Qty, Serial, Total FROM billdetail WHERE BillID='{BillID}' ORDER BY Serial;")
        bill_items:list = cursor.fetchall()

        # Fetch product details for each bill item
        product_details = {}
        for ProdID, _, _, _ in bill_items:
            if ProdID not in product_details:
                cursor.execute(f"SELECT Name, SP, Unit, GST FROM product WHERE ProdID='{ProdID}';")
                product_details[ProdID] = cursor.fetchone()

        # Calculate amounts for each product
        Pamt = [product_details[ProdID][1] * Qty for ProdID, Qty, _, _ in bill_items]

        # Close the database connection
        demodb.close()

    filename = str(f'../Bills/Invoice {BillID}.pdf') if __name__ == "__main__" else str(f'Bills/Invoice {BillID}.pdf')
    document = canvas.Canvas(f"{filename}", pagesize=A4)
    styles = getSampleStyleSheet()
    width, height = A4
    styleN = styles["BodyText"]
    styleN.alignment = TA_CENTER
    styleBH = styles["Normal"]
    styleBH.alignment = TA_CENTER

    # Variables
    Page_Decide = Decide if Decide <= 20 else 20

    title:str = f'A. Somasundara Nadar & Co.'
    cont:str = f'Ph. No 04634-240430'
    add:str = f'GSTIN : 27AACCA8432H1ZQ'
    bye:str = f'Thank You for shopping. See you Again!'

    net_tot = sum(bill_items[x][3] for x in range(int(BQty)))
    Name: list[str] = [f'Cust Name: {Name}', f'Bill No: {BillID}', f'Date/Time: {date} {time}']
    cust_pay: list[str] = [f'Cust ID: {CID}', f'Payment Type: {type}', f'Total Qty: {BQty}']
    b_total:str = f'{round(Total,2)}'
    amt_word = f'{num2words(b_total.rsplit('.')[0]).title()} Rupees {num2words(b_total.rsplit('.')[1]).title()} Paise'
    disc_amt: str = f'{Dis_ru}'
    
    if len(disc_amt.rsplit('.')[-1]) < 2:
        disc_amt = disc_amt + '0'
    if len(b_total.rsplit('.')[-1]) < 2:
        b_total = b_total + '0'
    if time.split(':')[0] > '12':
        a = int(time.split(':')[0]) - 12
        time = str(a) + ':' + time.split(':')[1] + ':' + time.split(':')[2] + ' PM'
    else:
        time = time + " AM"

    Tot_num: str = f'Grand Total: Rs {b_total}'
    Tot_text:str = f'({amt_word})'
    Amt_pay: str = f'Amt Bal: Rs {Bal}  Amt Paid: Rs {b_paid}'
    discount: str = f'Disc: Rs {disc_amt} ({Dis_per}%)'
    botom_text: str = f'{Tot_num}\n{Tot_text}\n{Amt_pay}    {discount}\n{cont}  {add}\n{bye}'

    # Place top part in pdf first page
    document.setFont("Helvetica-Bold", 36)
    document.drawCentredString(300, 775, title)

    text = document.beginText(40, 740)
    text.setFont("Helvetica", 16)
    for line in Name:
        text.textLine(line)
    document.drawText(text)

    text = document.beginText(350, 740)
    text.setFont("Helvetica", 16)
    for line in cust_pay:
        text.textLine(line)
    document.drawText(text)

    # Coordinate Part for table and bottom part
    if Decide <= 20:
        def table(max):
            x, y = 40, height - max - 150
            return x, y
    
        def Bot_tot():
            x, y = 40, height - req_hei - 170
            return x, int(y)
        
        def Bot_txt():
            x, y = 40, height - req_hei - 190
            return x, int(y)

        def Amt_row():
            x, y = 40, height - req_hei - 220
            return x, int(y)
        
        def Cont():
            x, y = 40, height - req_hei - 240
            return x, int(y)

        def Bye():
            x, y = 100, height - req_hei - 270
            return x, int(y)

    data = [[Paragraph('''<b>Sr No.</b>''', styleBH), Paragraph('''<b>Product</b>''', styleBH),
             Paragraph('''<b>Qty</b>''', styleBH), Paragraph('''<b>Units</b>''', styleBH),
             Paragraph('''<b>Rate</b>''', styleBH), Paragraph('''<b>Amount</b>''', styleBH),
             Paragraph('''<b>Tax</b>''', styleBH), Paragraph('''<b>Total</b>''', styleBH)]]
    
    for i in range(0, Page_Decide):
        p_ser = bill_items[i][2]
        p_pid = bill_items[i][0]
        p_name = product_details[p_pid][0]
        p_qty = bill_items[i][1]
        p_unit = product_details[p_pid][2]
        p_rate = product_details[p_pid][1]
        p_amt = Pamt[i]
        p_tax = product_details[p_pid][3]
        p_total = bill_items[i][3]
        c = [Paragraph(f'{p_ser}', styleN), Paragraph(f'{p_name}', styleN), Paragraph(f'{p_qty}', styleN),
             Paragraph(f'{p_unit}', styleN), Paragraph(f'{p_rate}', styleN), Paragraph(f'{p_amt}', styleN),
             Paragraph(f'{p_tax}', styleN), Paragraph(f'{p_total}', styleN)]
        data.append(c)

    if Decide <= 20:
        data.append(
            ['', '', '', '', '', '', Paragraph('''<b>Net Total</b>''', styleBH), Paragraph(f'{net_tot}', styleN)])

    t = Table(data, rowHeights=25, colWidths=[45, 210, 30, 40, 50, 50, 50, 50])
    t.setStyle(TableStyle([('ALIGN', (0, 0), (-1, -1), 'CENTER'), ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'), 
                           ('INNERGRID', (0, 0), (-1, -1), 1, colors.black), ('BOX', (0, 0), (-1, -1), 1, colors.black), ]))
    req_wid,req_hei = t.wrapOn(document, width, height)
    t.drawOn(document, *table(req_hei))

    if Decide <= 20:
        aa = [Bot_tot,Bot_txt,Amt_row,Cont,Bye]
        b = botom_text.split('\n')
        for i in range(0,len(b)):
            if aa[i] == Bot_tot or aa[i] == Bye:
                document.setFont("Helvetica-Bold", 17)
            else:
                document.setFont("Helvetica", 16)
            document.drawString(*aa[i](),b[i])

    document.save()

if __name__ == '__main__':
    from SQL_TPass import Pass
    pas, us = ("Ramsour1_2003","root") #Pass()
    if pas==None:
        print('Wrong Password')
        from time import sleep
        sleep(2.5)
        raise SystemExit
    # demodb = connect(host="localhost", user=us, passwd=pas, database="project")
    # cursor = demodb.cursor()
    # cursor.execute(f"SELECT BillID FROM bill")
    # for i in cursor:
    #     print(i[0])
    # demodb.close()
    # Pdf(input("BillId: "), us, pas)
    Pdf('240610C01-1', us, pas)
    Pdf('240610C01-7', us, pas)

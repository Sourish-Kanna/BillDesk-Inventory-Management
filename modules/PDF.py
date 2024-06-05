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
    demodb = connect(host=DBhost, user=us, passwd=pas, database=DBname)
    cursor = demodb.cursor()

    # Fetch bill details
    cursor.execute(f"SELECT Date, Total, Dis_per, Amt FROM bill WHERE BillID='{BillID}';")
    bill_details = cursor.fetchone()
    billtime, BillNet, BillDisc, BillAmt = str(bill_details[0]).split(), *bill_details[1:]

    # Fetch customer details
    cursor.execute(f"SELECT cust.CustID, Name FROM cust JOIN bill ON cust.CustID=bill.CustID WHERE bill.BillID='{BillID}';")
    CustID, CustName = cursor.fetchone()

    # Fetch bill item count
    cursor.execute(f"SELECT COUNT(BillID) FROM billdetail WHERE BillID='{BillID}';")
    BQty = D= cursor.fetchone()[0]

    # Fetch bill item details
    cursor.execute(f"SELECT ProdID, Qty, Serial, Total FROM billdetail WHERE BillID='{BillID}' ORDER BY Serial;")
    bill_items = cursor.fetchall()

    # Fetch product details for each bill item
    product_details = {}
    for ProdID, Qty, Serial, Total in bill_items:
        if ProdID not in product_details:
            cursor.execute(f"SELECT Unit, GST, SP, Name FROM product WHERE ProdID='{ProdID}';")
            product_details[ProdID] = cursor.fetchone()

    # Calculate amounts for each product
    Pamt = [product_details[ProdID][2] * Qty for ProdID, Qty, _, _ in bill_items]

    # Close the database connection
    demodb.close()

    # Prepare data for PDF creation
    PId, Pqty, Bs, Ptot = zip(*bill_items)
    Pu, Ptax, Pc, Pname = zip(*product_details.values())

    # Page Creation
    if __name__ == "__main__":
        filename = str(f'../Bills/Invoice {BillID}.pdf')
    else:
        filename = str(f'Bills/Invoice {BillID}.pdf')
    document = canvas.Canvas(f"{filename}", pagesize=A4)
    styles = getSampleStyleSheet()
    width, height = A4
    styleN = styles["BodyText"]
    styleN.alignment = TA_CENTER
    styleBH = styles["Normal"]
    styleBH.alignment = TA_CENTER

    if D <= 16:
        b = D
    else:
        b = 16

    def table():
        x, y = 0.0, height - (2.3 + (0.5 * (b + 2))) * inch
        return x, y

    # Variables
    title = f'A. Somasundara Nadar & Co.'
    cont = f'Ph. No 04634-240430'
    add = f'GSTIN : 27AACCA8432H1ZQ'
    bye = f'Thank You for shopping. See you Again!'
    btype = f'1'

    disc = BillDisc
    tot = BillAmt
    disc_amt = str(round((tot * BillDisc) / 100, 2))
    amt = str(BillNet)

    if len(disc_amt.rsplit('.')[-1]) < 2:
        disc_amt = disc_amt + '0'

    if len(amt.rsplit('.')[-1]) < 2:
        a = amt.rsplit('.')
        amt = a[0] + '.' + str(int(a[1]) * 10)
        del a

    date = billtime[0].split('-')[2] + '/' + billtime[0].split('-')[1] + '/' + billtime[0].split('-')[0]
    time = billtime[1]
    BilID = BillID
    cust_name = CustName

    if time.split(':')[0] > '12':
        a = int(time.split(':')[0]) - 12
        time = str(a) + ':' + time.split(':')[1] + ':' + time.split(':')[2] + ' PM'
    else:
        time = time + " AM"

    discount = f'Discount: Rs {disc_amt} ({disc}%)'
    cust_name = [f'Customer Name: {cust_name}', f'Bill No: {BilID}', f'Date: {date}']
    cust_pay = [f'Customer ID: {CustID}', f'User: root', f'Time: {time}']

    a = amt.rsplit('.')
    a1 = int(a[0])
    a2 = int(a[1])
    amt_wrd = str(num2words(a1).title()) + ' Rupees ' + str(num2words(a2).title()) + ' Paise'

    Gndtot_1 = f'Grand Total: Rs {amt}'
    Gndtot_2 = f'({amt_wrd})'
    Qty = f'Total Qty: {BQty}'
    amt_paid = f'Amount Paid: Rs {amt}'

    # Place top part in pdf first page
    document.setFont("Helvetica-Bold", 36)
    document.drawCentredString(300, 775, title)

    text = document.beginText(40, 725)
    text.setFont("Helvetica", 16)
    for line in cust_name:
        text.textLine(line)
    document.drawText(text)

    text = document.beginText(350, 725)
    text.setFont("Helvetica", 16)
    for line in cust_pay:
        text.textLine(line)
    document.drawText(text)

    # Coordinate Part for table and bottom part
    if D <= 12:
        def gndtot_1():
            x, y = 30, height - (3.00 + (0.5 * (b + 2))) * inch
            return x, y

        def gndtot_2():
            x, y = 225, height - (3.00 + (0.5 * (b + 2))) * inch
            return x, y

        def qty():
            x, y = 470, height - (3.45 + (0.5 * (b + 2))) * inch
            return x, y

        def Amt_paid():
            x, y = 35, height - (3.45 + (0.5 * (b + 2))) * inch
            return x, y

        def Discount():
            x, y = 230, height - (3.45 + (0.5 * (b + 2))) * inch
            return x, y

        def Cont():
            x, y = 40, height - (3.95 + (0.5 * (b + 2))) * inch
            return x, y

        def Add():
            x, y = 230, height - (3.95 + (0.5 * (b + 2))) * inch
            return x, y

        def Bye():
            x, y = 300, height - (4.45 + (0.5 * (b + 2))) * inch
            return x, y

    elif 12 < D <= 16:  # new page

        def gndtot_1():
            x, y = 40, height - 1.30 * inch
            return x, y

        def gndtot_2():
            x, y = 40, height - 1.60 * inch
            return x, y

        def qty():
            x, y = 450, height - 1.95 * inch
            return x, y

        def Amt_paid():
            x, y = 40, height - 1.95 * inch
            return x, y

        def Discount():
            x, y = 230, height - 1.95 * inch
            return x, y

        def Cont():
            x, y = 40, height - 2.45 * inch
            return x, y

        def Add():
            x, y = 230, height - 2.45 * inch
            return x, y

        def Bye():
            x, y = 300, height - 2.95 * inch
            return x, y

    elif D > 16:  # Coordinate Part for table and bottom part
        # For items more than 14
        def gndtot_1():
            x, y = 40, height - ((0.5 * (b + 2)) + 1.30) * inch
            return x, y

        def gndtot_2():
            x, y = 40, height - ((0.5 * (b + 2)) + 1.60) * inch
            return x, y

        def qty():
            x, y = 450, height - ((0.5 * (b + 2)) + 1.95) * inch
            return x, y

        def Amt_paid():
            x, y = 40, height - ((0.5 * (b + 2)) + 1.95) * inch
            return x, y

        def Discount():
            x, y = 230, height - ((0.5 * (b + 2)) + 1.95) * inch
            return x, y

        def Cont():
            x, y = 40, height - ((0.5 * (b + 2)) + 2.45) * inch
            return x, y

        def Add():
            x, y = 230, height - ((0.5 * (b + 2)) + 2.45) * inch
            return x, y

        def Bye():
            x, y = 300, height - ((0.5 * (b + 2)) + 2.95) * inch
            return x, y

    data = [[Paragraph('''<b>Sr No.</b>''', styleBH), Paragraph('''<b>Product</b>''', styleBH),
             Paragraph('''<b>Qty.</b>''', styleBH), Paragraph('''<b>Units</b>''', styleBH),
             Paragraph('''<b>Rate</b>''', styleBH), Paragraph('''<b>Amount</b>''', styleBH),
             Paragraph('''<b>Tax</b>''', styleBH), Paragraph('''<b>Total</b>''', styleBH)]]
    for i in range(0, b):
        c = [Paragraph(f'{Bs[i]}', styleN), Paragraph(f'{Pname[i]}', styleN), Paragraph(f'{Pqty[i]}', styleN),
             Paragraph(f'{Pu[i]}', styleN), Paragraph(f'{Pc[i]}', styleN), Paragraph(f'{Pamt[i]}', styleN),
             Paragraph(f'{Ptax[i]}', styleN), Paragraph(f'{Ptot[i]}', styleN)]
        data.append(c)

    if D <= 16:
        data.append(
            ['', '', '', '', '', '', Paragraph('''<b>Net Total</b>''', styleBH), Paragraph(f'{BillAmt}', styleN)])

    t = Table(data, rowHeights=0.5*inch)
    t.setStyle(
        TableStyle([('INNERGRID', (0, 0), (-1, -1), 1, colors.black), ('BOX', (0, 0), (-1, -1), 1, colors.black), ]))
    t.wrapOn(document, width, height)
    t.drawOn(document, *table())

    if D <= 12:  # For single page document lower part
        text = document.beginText(*gndtot_1())
        text.setFont("Helvetica-Bold", 16)
        text.textLine(Gndtot_1)
        document.drawText(text)

        text = document.beginText(*gndtot_2())
        text.setFont("Helvetica-Bold", 10)
        text.textLine(Gndtot_2)
        document.drawText(text)

        text = document.beginText(*qty())
        text.setFont("Helvetica-Bold", 16)
        text.textLine(Qty)
        document.drawText(text)

        text = document.beginText(*Discount())
        text.setFont("Helvetica-Bold", 16)
        text.textLine(discount)
        document.drawText(text)

        text = document.beginText(*Amt_paid())
        text.setFont("Helvetica", 16)
        text.textLine(amt_paid)
        document.drawText(text)

        text = document.beginText(*Cont())
        text.setFont("Helvetica", 15)
        text.textLine(cont)
        document.drawText(text)

        text = document.beginText(*Add())
        text.setFont("Helvetica", 16)
        text.textLine(add)
        document.drawText(text)

        document.setFont("Helvetica-Bold", 17)
        document.drawCentredString(*Bye(), bye)

    elif D <= 16:

        document.showPage()

        text = document.beginText(*gndtot_1())
        text.setFont("Helvetica-Bold", 15)
        text.textLine(Gndtot_1)
        document.drawText(text)

        text = document.beginText(*gndtot_2())
        text.setFont("Helvetica-Bold", 11)
        text.textLine(Gndtot_2)
        document.drawText(text)

        text = document.beginText(*qty())
        text.setFont("Helvetica-Bold", 16)
        text.textLine(Qty)
        document.drawText(text)

        text = document.beginText(*Discount())
        text.setFont("Helvetica-Bold", 16)
        text.textLine(discount)
        document.drawText(text)

        text = document.beginText(*Amt_paid())
        text.setFont("Helvetica", 16)
        text.textLine(amt_paid)
        document.drawText(text)

        text = document.beginText(*Cont())
        text.setFont("Helvetica", 15)
        text.textLine(cont)
        document.drawText(text)

        text = document.beginText(*Add())
        text.setFont("Helvetica", 16)
        text.textLine(add)
        document.drawText(text)

        document.setFont("Helvetica-Bold", 17)
        document.drawCentredString(*Bye(), bye)

    if D > 16:  # For multiple page document

        # creating next full page with tables
        for io in range(0, ((D - 16) // 18)):
            b = 18

            def table():
                x, y = 0.0 * inch, height - (0.5 + (0.5 * (b + 2))) * inch
                return x, y

            document.showPage()
            data = [[Paragraph('''<b>Sr No.</b>''', styleBH), Paragraph('''<b>Product</b>''', styleBH),
                     Paragraph('''<b>Qty.</b>''', styleBH), Paragraph('''<b>Units</b>''', styleBH),
                     Paragraph('''<b>Rate</b>''', styleBH), Paragraph('''<b>Amount</b>''', styleBH),
                     Paragraph('''<b>Tax</b>''', styleBH), Paragraph('''<b>Total</b>''', styleBH)]]
            for i in range(0, b):
                i = 16 + (io * 18) + i
                c = [Paragraph(f'{Bs[i]}', styleN), Paragraph(f'{Pname[i]}', styleN), Paragraph(f'{Pqty[i]}', styleN),
                     Paragraph(f'{Pu[i]}', styleN), Paragraph(f'{Pc[i]}', styleN), Paragraph(f'{Pamt[i]}', styleN),
                     Paragraph(f'{Ptax[i]}', styleN), Paragraph(f'{Ptot[i]}', styleN)]
                data.append(c)

            t = Table(data, rowHeights=0.5*inch)
            t.setStyle(TableStyle(
                [('INNERGRID', (0, 0), (-1, -1), 1, colors.black), ('BOX', (0, 0), (-1, -1), 1, colors.black), ]))
            t.wrapOn(document, width, height)
            t.drawOn(document, *table())

        if (D - 16) % 18 != 0:  # Creating last page
            b = (D - 16) % 18

            def table():
                x, y = 0 * inch, height - (0.50 + (0.5 * (b + 2))) * inch
                return x, y

            document.showPage()
            data = [[Paragraph('''<b>Sr No.</b>''', styleBH), Paragraph('''<b>Product</b>''', styleBH),
                     Paragraph('''<b>Qty.</b>''', styleBH), Paragraph('''<b>Units</b>''', styleBH),
                     Paragraph('''<b>Rate</b>''', styleBH), Paragraph('''<b>Amount</b>''', styleBH),
                     Paragraph('''<b>Tax</b>''', styleBH), Paragraph('''<b>Total</b>''', styleBH)]]
            for i in range(0, b):
                i = 16 + (((D - 16) // 18) * 18) + i
                c = [Paragraph(f'{Bs[i]}', styleN), Paragraph(f'{Pname[i]}', styleN), Paragraph(f'{Pqty[i]}', styleN),
                     Paragraph(f'{Pu[i]}', styleN), Paragraph(f'{Pc[i]}', styleN), Paragraph(f'{Pamt[i]}', styleN),
                     Paragraph(f'{Ptax[i]}', styleN), Paragraph(f'{Ptot[i]}', styleN)]
                data.append(c)
            data.append(
                ['', '', '', '', '', '', Paragraph('''<b>Net Total</b>''', styleBH), Paragraph(f'{tot}', styleN)])

            t = Table(data, rowHeights=0.5*inch)
            t.setStyle(TableStyle(
                [('INNERGRID', (0, 0), (-1, -1), 1, colors.black), ('BOX', (0, 0), (-1, -1), 1, colors.black), ]))
            t.wrapOn(document, width, height)
            t.drawOn(document, *table())

            b = (D - 16) % 18

            if b >= 18:
                b = -2
                document.showPage()

            text = document.beginText(*gndtot_1())
            text.setFont("Helvetica-Bold", 15)
            text.textLine(Gndtot_1)
            document.drawText(text)

            text = document.beginText(*gndtot_2())
            text.setFont("Helvetica-Bold", 11)
            text.textLine(Gndtot_2)
            document.drawText(text)

            text = document.beginText(*qty())
            text.setFont("Helvetica-Bold", 16)
            text.textLine(Qty)
            document.drawText(text)

            text = document.beginText(*Discount())
            text.setFont("Helvetica-Bold", 16)
            text.textLine(discount)
            document.drawText(text)

            text = document.beginText(*Amt_paid())
            text.setFont("Helvetica", 16)
            text.textLine(amt_paid)
            document.drawText(text)

            text = document.beginText(*Cont())
            text.setFont("Helvetica", 15)
            text.textLine(cont)
            document.drawText(text)

            text = document.beginText(*Add())
            text.setFont("Helvetica", 16)
            text.textLine(add)
            document.drawText(text)

            document.setFont("Helvetica-Bold", 17)
            document.drawCentredString(*Bye(), bye)

        elif (D - 16) % 18 == 0:  # last page if table end at end of the page
            document.showPage()
            b = -2

            text = document.beginText(*gndtot_1())
            text.setFont("Helvetica-Bold", 15)
            text.textLine(Gndtot_1)
            document.drawText(text)

            text = document.beginText(*gndtot_2())
            text.setFont("Helvetica-Bold", 11)
            text.textLine(Gndtot_2)
            document.drawText(text)

            text = document.beginText(*qty())
            text.setFont("Helvetica-Bold", 16)
            text.textLine(Qty)
            document.drawText(text)

            text = document.beginText(*Discount())
            text.setFont("Helvetica-Bold", 16)
            text.textLine(discount)
            document.drawText(text)

            text = document.beginText(*Amt_paid())
            text.setFont("Helvetica", 16)
            text.textLine(amt_paid)
            document.drawText(text)

            text = document.beginText(*Cont())
            text.setFont("Helvetica", 15)
            text.textLine(cont)
            document.drawText(text)

            text = document.beginText(*Add())
            text.setFont("Helvetica", 16)
            text.textLine(add)
            document.drawText(text)

            document.setFont("Helvetica-Bold", 17)
            document.drawCentredString(*Bye(), bye)

    document.save()


if __name__ == '__main__':
    from SQL_TPass import Pass
    pas, us = ("Ramsour1_2003","root")#Pass()
    if pas==None:
        print('Wrong Password')
        from time import sleep
        sleep(2.5)
        raise SystemExit
    demodb = connect(host="localhost", user=us, passwd=pas, database="project")
    cursor = demodb.cursor()
    cursor.execute(f"SELECT BillID FROM bill")
    for i in cursor:
        print(i[0])
    demodb.close()
    Pdf(input("BillId: "), us, pas)

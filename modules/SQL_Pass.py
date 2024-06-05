#SQL_Pass Source Code
import tkinter as tk
from mysql.connector import connect
import os.path as opt

Cap = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
Num = ' 0123456789_-=+/*'
LETTERS = Cap+Num+Cap.lower()
end = len(LETTERS)

def encrypt(message, key):
    encrypted = ''
    for chars in message:
        if chars in LETTERS:
            num = LETTERS.find(chars)
            num += key
            if num>end-1:
                num-=end
                encrypted +=  '?'
            encrypted +=  LETTERS[num]

    return encrypted

def decrypt(message, key):
    decrypted = ''
    cc=0
    for chars in message:
        if chars in LETTERS:
            num = LETTERS.find(chars)
            num -= key
            if chars=="?":
                cc=1
                pass
            if cc==1:
                num=end-num
                cc=0
            decrypted +=  LETTERS[num]

    return decrypted

def Pass():
    """Login Window for sql

    Main Window"""
    window = tk.Tk()
    window.title("Password")
    window.attributes('-topmost', True)
    window.config(bg='yellow')
    window.focus_force()

    pas = tk.StringVar()
    user = tk.StringVar()
    save = tk.IntVar()
    user.set('root')

    a = 'Username :'
    l0 = tk.Label(window, bg='yellow', text=a, font=("arial", 14))
    l0.grid(column=1, row=1)
    entry0 = tk.Entry(window, textvar=user, width=15, font=("arial", 14))
    entry0.grid(column=2, row=1, padx=5, pady=5)

    a = 'Password :'
    l1 = tk.Label(window, bg='yellow', text=a, font=("arial", 14))
    l1.grid(column=1, row=2)
    entry1 = tk.Entry(window, textvar=pas, width=15, show="•", font=("arial", 14))
    entry1.grid(column=2, row=2, padx=5, pady=5)
    entry1.focus()
    check = tk.Checkbutton(window, text="Do you want Remember info", font=("arial", 10),
                           variable=save, bg='yellow', onvalue=1, offvalue=0)
    check.grid(column=1, row=3)

    def callback(event):
        entry1.focus()

    entry0.bind('<Return>', callback)

    if __name__ == '__main__':
        path = 'save.temp'
    else:
        path = 'modules/save.temp'

    if opt.exists(path):
        f = open(path, "r")
        ddnc = f.read()
        dnc = decrypt(ddnc, 21)
        ss = dnc.split()
        user.set(ss[1])
        pas.set(ss[0])
        check.select()
        f.close()

    def Check():
        us = user.get()
        ft = pas.get()

        try:
            demodb = connect(host="localhost", user=us, passwd=ft)
            demodb.close()
            if save.get() == 1:
                f = open(path, "w")
                bb = ft + ' ' + us
                enc = encrypt(bb, 21)
                f.write(enc)
                f.close()
            elif save.get() == 0:
                if opt.exists(path):
                    from os import remove
                    remove(path)
            return True
        except:
            return False

    def Close():
        window.destroy()

    def Save():
        if Check():
            button0.destroy()
            check.destroy()
            a = ' ' * 50
            l4 = tk.Label(window, bg='yellow', text=a, font=("arial", 14))
            l4.grid(column=1, row=4, columnspan=3, rowspan=1, padx=5, pady=5)
            a = 'Login Successful'
            entry0.config(state='disabled')
            entry1.config(state='disabled')
            l5 = tk.Label(window, text=a, bg='yellow', font=("arial", 14))
            l5.grid(column=1, row=3, columnspan=2, rowspan=1, padx=5, pady=5)

            def callback(event):
                Close()

            entry1.bind('<Return>', callback)
            b1 = tk.Button(window, text="Close", width=12, bg="brown", fg="white", command=Close)
            b1.grid(column=1, row=4, columnspan=2, rowspan=1, padx=10, pady=5)

        else:
            a = 'Incorrect !! Try Again'
            l2 = tk.Label(window, bg='yellow', text=a, fg='red', font=("arial", 14))
            l2.grid(column=1, row=4, columnspan=2, rowspan=1, padx=5, pady=5)
            pas.set('')
            entry1.focus()

    def callback(event):
        Save()

    def on_closing():
        pas.set('')
        Close()

    entry1.bind('<Return>', callback)
    button0 = tk.Button(window, text="Login", width=12, bg="brown", fg="white", command=Save)
    button0.grid(column=2, row=3, pady=5)
    window.protocol("WM_DELETE_WINDOW", on_closing)

    window.mainloop()
    us = user.get()
    pasw = pas.get()
    return pasw, us


if __name__ == '__main__':
    print(Pass())

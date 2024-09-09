#SQL_Pass Source Code
import tkinter as tk
from mysql.connector import connect
import os.path as opt
import pickle

bgcol:str ="#add8e6"
Cap = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
Num = '0123456789'
Sym = '_-=+/*!@#$%^&:;"\'\\<>,.?`()}{[] '
LETTERS = Cap+Num+Cap.lower()+Sym
end = len(LETTERS)
key=26

def encrypt(message):
    encrypted = ''
    encrypted_lst = []

    for chars in message:
        if chars in LETTERS:
            num = LETTERS.find(chars)
            num += key
            if num>end-1:
                num-=end
                encrypted +=  '~'
            encrypted +=  LETTERS[num]
            
    for chars in encrypted:
        txt=ord(chars)
        encrypted_lst.append(txt)

    return encrypted_lst

def decrypt(message):
    decrypted_lst = ''
    decrypted = ''
    cc=0
    
    for chars in message:
        txt=chr(chars)
        decrypted_lst += txt

    for chars in decrypted_lst:
        if chars in LETTERS:
            num = LETTERS.find(chars)
            num -= key
            if chars=="~":
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
    window.config(bg=bgcol)
    if __name__ == '__main__':
        window.iconbitmap(r'1.ico')
    else:
        window.iconbitmap(r'modules/1.ico')
    window.focus_force()

    pas = tk.StringVar()
    user = tk.StringVar()
    save = tk.IntVar()
    user.set('root')

    l0 = tk.Label(window, bg=bgcol, text='Username :', font=("arial", 14))
    l0.grid(column=1, row=1)
    entry0 = tk.Entry(window, textvar=user, width=15, font=("arial", 14))
    entry0.grid(column=2, row=1, padx=5, pady=5)

    l1 = tk.Label(window, bg=bgcol, text='Password :', font=("arial", 14))
    l1.grid(column=1, row=2)
    entry1 = tk.Entry(window, textvar=pas, width=15, show="•", font=("arial", 14))
    entry1.grid(column=2, row=2, padx=5, pady=5)
    entry1.focus()
    check = tk.Checkbutton(window, text="Do you want Remember info", font=("arial", 10),
                           variable=save, bg=bgcol, onvalue=1, offvalue=0)
    check.grid(column=1, row=3)
    l2 = tk.Label(window, bg=bgcol, text="", fg='red', font=("arial", 14))
    l2.grid(column=1, row=4, columnspan=2, rowspan=1, padx=5, pady=5)

    def callback1(event):
        entry1.focus()

    entry0.bind('<Return>', callback1)

    if __name__ == '__main__':
        path = 'save.temp'  # To Save Password
        path1 = '../Bills'  # To Save Bills
    else:
        path = 'modules/save.temp'
        path1 = 'Bills'

    if opt.exists(path):
        f = open(path, "rb")
        ddnc = pickle.load(f)
        dnc = decrypt(ddnc)
        ss = dnc.split()
        user.set(ss[1])
        pas.set(ss[0])
        check.select()
        f.close()

    if opt.exists(path1):
        pass
    else:
        import os
        os.mkdir(path1)

    def Check():
        us = user.get()
        ft = pas.get()
        try:
            demodb = connect(host="localhost", user=us, passwd=ft)
            demodb.close()
        except:
            return False

        if save.get() == 1:
            f = open(path, "wb")
            bb = ft + ' ' + us
            enc = encrypt(bb)
            pickle.dump(enc,f)
            f.close()
        elif save.get() == 0:
            if opt.exists(path):
                from os import remove
                remove(path)
        return True

    def Close():
        window.destroy()

    def Save():
        if Check():
            button0.destroy()
            check.destroy()
            l2.config(text='')
            a = 'Login Successful'
            entry0.config(state='disabled')
            entry1.config(state='disabled')
            l5 = tk.Label(window, text=a, bg=bgcol, font=("arial", 14))
            l5.grid(column=1, row=3, columnspan=2, rowspan=1, padx=5, pady=5)

            def callback(event):
                Close()

            entry1.bind('<Return>', callback)
            b1 = tk.Button(window, text="Close", width=12, bg="brown", fg="white", command=Close)
            b1.grid(column=1, row=4, columnspan=2, rowspan=1, padx=10, pady=5)

        else:
            a = 'Incorrect !! Try Again'
            l2.config(text=a)
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

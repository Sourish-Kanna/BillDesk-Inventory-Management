#Install Source Code
from tkinter import *


def install_Old():
    """To Install Required Modules for proper function of program

    To Install Required Modules for additional options"""
    root = Tk()
    root.geometry("500x300")
    root.title("Modules Installer")
    root.focus_force()
    root.config(bg='yellow')
    if __name__ == '__main__':
        root.iconbitmap(r'1.ico')
    else:
        root.iconbitmap(r'modules/1.ico')
    root.attributes('-topmost', True)

    def Exit():
        root.destroy()

    def Pip():
        from os import system
        system('start cmd /c "pip install pillow"')
        system('start cmd /c "pip install num2words"')
        system('start cmd /c "pip install wheel"')
        system('start cmd /c "pip install reportlab"')
        system('start cmd /c "pip install mysql-connector-python"')
        system('start cmd /c "pip install cryptography"')
        Exit()

    def UnPip():
        from os import system
        system('start cmd /c "pip uninstall pillow"')
        system('start cmd /c "pip uninstall num2words"')
        system('start cmd /c "pip uninstall wheel"')
        system('start cmd /c "pip uninstall reportlab"')
        system('start cmd /c "pip uninstall mysql-connector-python"')
        system('start cmd /c "pip uninstall cryptography"')
        Exit()

    lab = Label(root, text="\n" * 3, bg='yellow')
    lab.pack()

    l10 = Label(root, text="To repair modules click Reinstall.\nIf you want to "
                           "uninstall then click and\ntype y in all windows.", bg="yellow",
                font=("arial", 14, "bold"))
    l10.pack()

    button6 = Button(root, text="Reinstall", width=12, bg="brown", fg="white", command=Pip)
    button6.place(x=130, y=180)
    button7 = Button(root, text="Uninstall", width=12, bg="brown", fg="white", command=UnPip)
    button7.place(x=280, y=180)
    button7 = Button(root, text="Exit", width=12, bg="brown", fg="white", command=Exit)
    button7.place(x=205, y=225)
    root.mainloop()


def Check():
    """Checking required modules"""
    try:
        import PIL, wheel, reportlab, num2words, mysql.connector
        return True
    except:
        return False


def install():
    """To Install Required Modules basic options"""
    if not Check():
        root = Tk()
        root.geometry("500x250")
        root.title("Components Installer")
        root.focus_force()
        root.config(bg='yellow')
        if __name__ == '__main__':
            root.iconbitmap(r'1.ico')
        else:
            root.iconbitmap(r'modules/1.ico')
        root.attributes('-topmost', True)

        def Exit():
            root.destroy()

        def Pip():
            from os import system
            system('start cmd /c "pip install pillow"')
            system('start cmd /c "pip install num2words"')
            system('start cmd /c "pip install wheel"')
            system('start cmd /c "pip install reportlab"')
            system('start cmd /c "pip install mysql-connector-python"')
            system('start cmd /c "pip install cryptography"')
            Exit()

        l10 = Label(root, text="\n\n\nLooks like you don't have required\ncomponents to "
                               "run the program.\nLets install them by clicking install.",
                    bg="yellow", font=("arial", 14, "bold"))
        l10.pack()
        button6 = Button(root, text="Install", width=12, bg="brown", fg="white", command=Pip)
        button6.place(x=200, y=180)
        root.mainloop()


if __name__ == '__main__':  # For Debugging
    a = int(input('1-old\n2-new\n'))
    if a == 1:
        install_Old()
    elif a == 2:
        install()

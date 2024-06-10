#Help window Source Code
from tkinter import *
ImgC = 0
bgcol:str ="#add8e6"


def Help():
    from PIL import ImageTk , Image
    if __name__ == '__main__':
        root = Tk()
        root.iconbitmap(r'1.ico')
        pat1='helppics/'
    else:
        root = Toplevel()
        root.iconbitmap(r'modules/1.ico')
        pat1='modules/helppics/'
    root.geometry("660x440")
    root.title("Help")
    root.focus_force()
    root.config(bg=bgcol)
    root.attributes('-topmost', True)
    img = []

    for i in range(22):
        image = ImageTk.PhotoImage(Image.open(f"{pat1}{i}.png").resize((652,401),Image.Resampling.LANCZOS))
        img.append(image)
        

    def Exit():
        root.destroy()

    def Back():
        global ImgC
        ImgC -= 1
        if ImgC == 0:
            button3.config(state="disabled")
            l10.config(image=img[ImgC])
            return
        elif ImgC == len(img)-2:
            button2.config(state="active")
            l10.config(image=img[ImgC])
        else:
            l10.config(image=img[ImgC])

    def Next():
        global ImgC
        ImgC += 1
        if ImgC == len(img)-1:
            button2.config(state="disabled")
            l10.config(image=img[ImgC])
            return
        elif ImgC == 1:
            button3.config(state="active")
            l10.config(image=img[ImgC])
        else:
            l10.config(image=img[ImgC])
        
    l10 = Label(root, image=img[ImgC], bg=bgcol)
    l10.grid(row=1, column=1, columnspan=2)
    button2 = Button(root, text="Next -->",width =12, command=Next)
    button2.grid(row=2, column=2, sticky="W")
    button3 = Button(root, text="<-- Previous",width =12, state="disabled", command=Back)
    button3.grid(row=2, column=1, sticky="E")
    button1 = Button(root, text="Exit",width =12, command=Exit)
    button1.grid(row=2, column=2, sticky="E")
    root.mainloop()

if __name__ == '__main__':  # For Debugging
    Help()

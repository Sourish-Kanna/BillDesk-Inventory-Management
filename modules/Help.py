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
    pat2='.png'
    root.attributes('-topmost', True)

    img0  = ImageTk.PhotoImage(Image.open(f"{pat1}0{pat2}").resize((652,401),Image.Resampling.LANCZOS))
    img1  = ImageTk.PhotoImage(Image.open(f"{pat1}1{pat2}").resize((652,401),Image.Resampling.LANCZOS))
    img2  = ImageTk.PhotoImage(Image.open(f"{pat1}2{pat2}").resize((652,401),Image.Resampling.LANCZOS))
    img3  = ImageTk.PhotoImage(Image.open(f"{pat1}3{pat2}").resize((652,401),Image.Resampling.LANCZOS))
    img4  = ImageTk.PhotoImage(Image.open(f"{pat1}4{pat2}").resize((652,401),Image.Resampling.LANCZOS))
    img5  = ImageTk.PhotoImage(Image.open(f"{pat1}5{pat2}").resize((652,401),Image.Resampling.LANCZOS))
    img6  = ImageTk.PhotoImage(Image.open(f"{pat1}6{pat2}").resize((652,401),Image.Resampling.LANCZOS))
    img7  = ImageTk.PhotoImage(Image.open(f"{pat1}7{pat2}").resize((652,401),Image.Resampling.LANCZOS))
    img8  = ImageTk.PhotoImage(Image.open(f"{pat1}8{pat2}").resize((652,401),Image.Resampling.LANCZOS))
    img9  = ImageTk.PhotoImage(Image.open(f"{pat1}9{pat2}").resize((652,401),Image.Resampling.LANCZOS))
    img10 = ImageTk.PhotoImage(Image.open(f"{pat1}10{pat2}").resize((652,401),Image.Resampling.LANCZOS))
    img11 = ImageTk.PhotoImage(Image.open(f"{pat1}11{pat2}").resize((652,401),Image.Resampling.LANCZOS))
    img12 = ImageTk.PhotoImage(Image.open(f"{pat1}12{pat2}").resize((652,401),Image.Resampling.LANCZOS))
    img13 = ImageTk.PhotoImage(Image.open(f"{pat1}13{pat2}").resize((652,401),Image.Resampling.LANCZOS))
    img14 = ImageTk.PhotoImage(Image.open(f"{pat1}14{pat2}").resize((652,401),Image.Resampling.LANCZOS))
    img15 = ImageTk.PhotoImage(Image.open(f"{pat1}15{pat2}").resize((652,401),Image.Resampling.LANCZOS))
    img16 = ImageTk.PhotoImage(Image.open(f"{pat1}16{pat2}").resize((652,401),Image.Resampling.LANCZOS))
    img17 = ImageTk.PhotoImage(Image.open(f"{pat1}17{pat2}").resize((652,401),Image.Resampling.LANCZOS))
    img18 = ImageTk.PhotoImage(Image.open(f"{pat1}18{pat2}").resize((652,401),Image.Resampling.LANCZOS))
    img19 = ImageTk.PhotoImage(Image.open(f"{pat1}19{pat2}").resize((652,401),Image.Resampling.LANCZOS))
    img20 = ImageTk.PhotoImage(Image.open(f"{pat1}20{pat2}").resize((652,401),Image.Resampling.LANCZOS))
    img21 = ImageTk.PhotoImage(Image.open(f"{pat1}21{pat2}").resize((652,401),Image.Resampling.LANCZOS))

    img = [img0,img21,img1,img2,img3,img4,img5,img6,img7,img8,img9,img10,img11,img12,img13,
           img14,img15,img16,img17,img18,img19,img20]
    

    def Exit():
        root.destroy()

    def Back():
        global ImgC
        ImgC-=1
        if ImgC==0:
            button3.config(state="disabled")
            l10.config(image=img[ImgC])
            return
        elif ImgC==len(img)-2:
            button2.config(state="active")
            l10.config(image=img[ImgC])
        else:
            l10.config(image=img[ImgC])

    def Next():
        global ImgC
        ImgC+=1
        if ImgC==len(img)-1:
            button2.config(state="disabled")
            l10.config(image=img[ImgC])
            return
        elif ImgC==1:
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

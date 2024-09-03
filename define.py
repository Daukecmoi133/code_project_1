from tkinter import *

def cout(event=None):
    xuat.pack()

def stop(event=None):
    xuat.pack_forget()
    
window = Tk()

but = Button(window, text="Press Me")
but.pack()

xuat = Label(window, text="1")

but.bind("<ButtonPress>", cout)  # Liên kết sự kiện nhấn nút chuột trái với hàm cout
but.bind("<ButtonRelease>", stop)  # Liên kết sự kiện thả nút chuột trái với hàm stop

window.mainloop()

from tkinter import *
from tkinter import messagebox

app = Tk()

def ok_click():
    message = txt.get()
    messagebox.showinfo('내용:',message)

lal = Label(app, text='입력')
lal.grid(row=0, column=0)
txt = Entry(app)
txt.grid(row=0, column=1)
btn = Button(app, text='ok', command=ok_click)
btn.grid(row=1, column=1)
app.mainloop()

app.mainloop()
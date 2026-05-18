from tkinter import *

app = Tk()

def move_left(event):
    canvas.move(ball, -100,0)
def move_right(event):
    canvas.move(ball, 100,0)
def move_up(event):
    canvas.move(ball, 0,-100)
def move_down(event):
    canvas.move(ball, 0,100)
canvas = Canvas(app, width=400, height=300)
canvas.pack()
ball = canvas.create_oval(100,150,150,200,fill='red')
app.bind('<Left>',move_left)
app.bind('<Right>',move_right)
app.bind('<Up>',move_up)
app.bind('<Down>',move_down)
app.mainloop()
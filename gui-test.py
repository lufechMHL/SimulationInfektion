from tkinter import *
master = Tk()

canvas_width = 1000
canvas_height = 500
w = Canvas(master,
           width=canvas_width,
           height=canvas_height)

w.pack()

positionX = 200
positionY = 250
zielX = 600
zielY = 50
green = "#476042"

w.create_rectangle(3, 3, 997, 497)
w.create_oval(positionX, positionY, positionX + 10, positionY + 10,
              outline = 'green', fill = 'green')
w.create_oval(positionX - 10, positionY - 10,
              positionX + 10 + 10, positionY + 10 + 10)
w.create_line(positionX+5, positionY+5, zielX, zielY, fill= 'red')

mainloop()

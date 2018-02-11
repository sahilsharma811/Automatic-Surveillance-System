from tkinter import *
from tkinter import filedialog
import csv
import os

if os.path.exists("key.csv"):
    os.remove("key.csv")
canvas_width = 500
canvas_height = 450
def paint( event ):
    python_green = "#476042"
    x1, y1 = ( event.x - 1 ), ( event.y - 1 )
    x2, y2 = ( event.x + 1 ), ( event.y + 1 )
    w.create_oval( x1, y1, x2, y2, fill = python_green )

master = Tk()
master.title( "Mouse Tracker for Steganography" )
w = Canvas(master,
             width=canvas_width,
             height=canvas_height)
w.pack(expand = YES, fill = BOTH)
w.bind( "<B1-Motion>", paint )

def motion(event):
    x, y = event.x, event.y
    print('{}, {}'.format(x, y))
    with open("key.csv","a+") as a:
    	wtr = csv.writer(a)
    	wtr.writerow((x,y))

master.bind('<B1-Motion>', motion)
message = Label( master, text = "Press and Drag the mouse to draw" )
message.pack( side = BOTTOM )

mainloop()

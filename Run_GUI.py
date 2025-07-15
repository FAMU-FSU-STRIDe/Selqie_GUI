from GUI_Classes import Table
from tkinter import *
import tkinter as tk

window = Tk()
#window.geometry("1500x750")
window.attributes("-fullscreen", True)
window.bind("<Escape>", lambda e: window.attributes("-fullscreen", False))  # Esc to exit
window.title("SELQIE")

def on_closing():
    global running
    running = False
    window.destroy()

window.protocol("WM_DELETE_WINDOW", on_closing)

def create_widget(parent, widget_type, **options):
    return widget_type(parent, **options)

status_frame = create_widget(window, tk.Frame, bg="#E6EAF5", bd = 2, height = 285, highlightcolor = 'red', highlightthickness=2, highlightbackground = 'black', relief = tk.RAISED, width = 500)
status_frame.place(relx=0.34, rely=0.22, relwidth=0.325, relheight=0.775)

part_status = [(f'Motor Driver {i} Temp', '--') for i in range (0,8)]


table = Table(status_frame, part_status)

window.mainloop()
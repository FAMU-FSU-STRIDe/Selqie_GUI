from GUI_Classes import Table, Camera, ControlPanel, ErrorLog
from tkinter import *
import tkinter as tk
import cv2, queue, threading


window = Tk()
#window.geometry("1500x750")
window.attributes("-fullscreen", True)
window.bind("<Escape>", lambda e: window.attributes("-fullscreen", False))  # Esc to exit
window.title("SELQIE")

def on_closing():
    running = False
    window.destroy()

window.protocol("WM_DELETE_WINDOW", on_closing)

def create_widget(parent, widget_type, **options):
    return widget_type(parent, **options)

camera_frame = create_widget(window, tk.Frame, bg="#E6EAF5", bd = 2, height = 450, highlightcolor = 'red', highlightthickness=2, highlightbackground = 'black', relief = tk.RAISED, width = 500)
camera_frame.place(relx=0.003, rely=0.01, relwidth=0.335, relheight=0.6)

control_frame = create_widget(window, tk.Frame, bg="#E6EAF5", bd = 2, height = 150, highlightcolor = 'red', highlightthickness=2, highlightbackground = 'black', relief = tk.RAISED, width = 485)
control_frame.place(relx=0.34, rely=0.01, relwidth=0.656, relheight=0.205)

status_frame = create_widget(window, tk.Frame, bg="#E6EAF5", bd = 2, height = 285, highlightcolor = 'red', highlightthickness=2, highlightbackground = 'black', relief = tk.RAISED, width = 500)
status_frame.place(relx=0.34, rely=0.22, relwidth=0.325, relheight=0.775)


error_frame = create_widget(window, tk.Frame, bg="#E6EAF5", bd = 2, height = 500, highlightcolor = 'red', highlightthickness=2, highlightbackground = 'black', relief = tk.RAISED, width = 500)
error_frame.place(relx = 0.003, rely = 0.615, relwidth = 0.335, relheight = 0.38)


part_status = [(f'Motor Driver {i} Temp', '--') for i in range (0,8)]


table = Table(status_frame, part_status)
camera = Camera(camera_frame, 0.003, 0, 0.99, 0.90)
control = ControlPanel(control_frame)
error = ErrorLog(error_frame)

threading.Thread(target = camera.camera_queue, daemon=True).start()
camera.poll_camera()

window.mainloop()
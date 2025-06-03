#foundation for gui
from tkinter import *
import tkinter as tk
import cv2
from PIL import Image, ImageTk

#--------Table Class for Motor Section--------#
class Table:
    def __init__(self, parent, data, x=0, y=0):
        self.frame = Frame(parent)
        self.frame.place(x=x, y=y)
        for i in range(total_rows):
            for j in range(total_columns):
                e = Entry(self.frame, width = 26, fg = 'black')
                e.grid(row=i, column=j)
                e.insert(END, data[i][j])

part_status = [('Part', 'Status'), ('Insert', 'Insert')]
total_rows = len(part_status)
total_columns = len(part_status[0])

#--------Functions--------#
def clickLeft():
    print("Left View")

def clickRight():
    print("Right View")

def clickStart():
    print("Start recording")

def clickStop():
    print("Stop recording")

def submit():
    file = Entry.get()
    print(file)

def create_widget(parent, widget_type, **options):
    return widget_type(parent, **options)

def create_button(parent, text, fg):
    return create_widget(parent, tk.Button, text=text, fg=fg, bg='lightblue', bd=3, cursor='hand1', highlightbackground = '#E1E4ED', relief = tk.RAISED)

def create_label(parent, text, fg):
    return create_widget(parent, tk.Label, text=text, fg=fg, bg='lightblue', bd=3, cursor='hand1', highlightbackground = '#E1E4ED', relief = tk.RAISED)

def update_camera():
    ret, frame = cap.read()
    if ret:
        frame = cv2.resize(frame, (485, 400))
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(frame)
        imgtk = ImageTk.PhotoImage(image = img)

        camera_label.imgtk = imgtk
        camera_label.configure(image = imgtk)

    camera_label.after(10, update_camera)

def rightCamera(right):
    if(right):
        rightCam.config(text=" Right Camera View")
    else:
        rightCam.config(text="")

def leftCamera(left):
    if(left):
        leftCam.config(text="Left Camera View")
    else:
        leftCam.config(text="")


#--------Window Initialization--------#
window = Tk()
window.geometry("1000x1000")
window.title("SELQIE")

#--------Frames--------#
camera_frame = create_widget(window, tk.Frame, bg="#E6EAF5", bd = 2, cursor = 'hand', height = 450, highlightcolor = 'red', highlightthickness=2, highlightbackground = 'black', relief = tk.RAISED, width = 500)
camera_frame.place(x=5, y=5)

motor_frame = create_widget(window, tk.Frame, bg="#E6EAF5", bd = 2, cursor = 'hand', height = 450, highlightcolor = 'red', highlightthickness=2, highlightbackground = 'black', relief = tk.RAISED, width = 500)
motor_frame.place(x=5, y=460)

file_frame = create_widget(window, tk.Frame, bg="#E6EAF5", bd = 2, cursor = 'hand', height = 450, highlightcolor = 'red', highlightthickness=2, highlightbackground = 'black', relief = tk.RAISED, width = 485)
file_frame.place(x=510, y=5)

localization_frame = create_widget(window, tk.Frame, bg="#E6EAF5", bd = 2, cursor = 'hand', height = 450, highlightcolor = 'red', highlightthickness=2, highlightbackground = 'black', relief = tk.RAISED, width = 485)
localization_frame.place(x=510, y=160)

#--------Frame Buttons-------#
left_cam_button = create_button(camera_frame, "Left", fg='black')
left_cam_button.place(x=135, y=400)

right_cam_button = create_button(camera_frame, "Right", fg='black')
right_cam_button.place(x=230, y=400)

submit_button = create_button(file_frame, "Submit", fg='black')
submit_button.config(command=submit)
submit_button.place(x=290, y=10)

start_button = create_button(file_frame, "Start", fg='black')
start_button.place(x=150, y=100)

stop_button = create_button(file_frame, "Stop", fg='black')
stop_button.place(x=230, y=100)

#--------File Entry--------#
file = create_label(file_frame, "Filename:", fg='black')
file.place(x=10, y=10)

fileEntry = create_widget(file_frame, tk.Entry, bg='white', bd=3)
fileEntry.place(x=90, y=10)


#--------Motor Table Frame--------#
Table(motor_frame, part_status)

#--------Camera-------#
camera_label = Label(camera_frame)
camera_label.place(x=0,y=0)

cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Cannot open camera")
    exit(0)

#--------Update and Print to Screen--------#
update_camera()
window.mainloop()



#messy gui code with two cameras
from tkinter import *
import tkinter as tk
import cv2
from PIL import Image, ImageTk

#----- -----#
#--- ---#

class Table:
    def __init__(self, parent, data, x=0, y=0):
        self.frame = Frame(parent)
        self.frame.place(x=x, y=y)
        for i in range(total_rows):
            for j in range(total_columns):
                self.frame.place(x=x, y=y)
                e = Entry(self.frame, width = 26, fg = 'black')
                e.grid(row=i, column=j)
                e.insert(END, data[i][j])

table_list = [('Part:', 'Status:'), ('idk', 'idk')]

total_rows = len(table_list)
total_columns = len(table_list[0])


#------Button Functions-----#
def clickLeft():
    print("Left View")
    #use left view function from jonathan

def clickRight():
    print("Right View")
    #use right view function from jonathan

def clickStart():
    print("Start recording")
    #func from jonathan

def clickStop():
    print("Stop recording")
    #func from jonathan

def Submit():
    file = fileEntry.get()
    print(file)

#-----Frame Window Function-----#
def create_widget(parent, widget_type, **options):
    return widget_type(parent, **options)

#-----Button Frame Function-----#
def create_button(parent, text, fg):
    return create_widget(parent, tk.Button, text = text, fg = fg, bg = 'lightblue', bd = 3, cursor = 'hand1', highlightcolor = 'red', highlightthickness = 0.5, highlightbackground = '#E1E4ED', relief = tk.RAISED)

#-----Label Frame Function-----#
def create_label(parent, text, fg):
    return create_widget(parent, tk.Label, text = text, fg = fg, bg = 'lightblue', bd = 3, cursor = 'hand1', highlightcolor = 'red', highlightthickness = 2, highlightbackground = 'black', relief = tk.RAISED)

#--------Camera Update--------#
def update_camera(cap, label):
    ret, frame = cap.read()
    if ret:
        frame = cv2.resize(frame, (300, 250))
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(frame)
        imgtk = ImageTk.PhotoImage(image = img)

        label.imgtk = imgtk
        label.configure(image = imgtk)

    label.after(10, update_camera, cap, label)

#-----Window Intializtion-----#
window = Tk()
window.geometry("1000x1000")
window.title("SELQIE")


#--------Frames--------#
camera_frame_left = create_widget(window, tk.Frame, bg="#E6EAF5", bd = 2, cursor = 'hand', height = 450, highlightcolor = 'red', highlightthickness=2, highlightbackground = 'black', relief = tk.RAISED, width = 245)
camera_frame_left.place(x=5, y=5)

camera_frame_right = create_widget(window, tk.Frame, bg='#E6EAF5', bd=2, cursor='hand1', height=450, highlightcolor='red', highlightthickness=2, highlightbackground='black',relief = tk.RAISED, width = 250)
camera_frame_right.place(x=255, y=5)

motor_frame = create_widget(window, tk.Frame, bg="#E6EAF5", bd = 2, cursor = 'hand', height = 330, highlightcolor = 'red', highlightthickness=2, highlightbackground='black', relief = tk.RAISED, width = 500)
motor_frame.place(x=5, y=460)

file_frame = create_widget(window, tk.Frame, bg="#E6EAF5", bd = 2, cursor = 'hand', height = 150, highlightcolor = 'red', highlightthickness = 2, highlightbackground = 'black', relief = tk.RAISED, width = 485)
file_frame.place(x=510, y=5)

localization_frame = create_widget(window, tk.Frame, bg="#E6EAF5", bd = 2, cursor = 'hand', height = 630, highlightcolor = 'red', highlightthickness = 2, highlightbackground = 'black', relief = tk.RAISED, width = 485)
localization_frame.place(x=510, y=160)

#-----Frame Buttons-----#
left_cam_button = create_button(camera_frame_left, "Left", fg = 'black')
left_cam_button.place(x = 155, y = 400)

right_cam_button = create_button(camera_frame_right, "Right", fg = 'black')
right_cam_button.place(x=150, y= 400)

submit_button = create_button(file_frame, "Submit", fg = 'black')
submit_button.config(command=Submit)
submit_button.place(x=290, y=10)

start_button = create_button(file_frame, "Start", fg = 'black')
#start_button.config()
start_button.place(x = 150, y=100)

stop_button = create_button(file_frame, "Stop", fg = 'black')
#stop_button.config()
stop_button.place(x=230, y=100)

#------Frame Label-----#

file = create_label(file_frame, "Filename:", fg ='black')
file.place(x = 10, y = 10)

fileEntry = create_widget(file_frame, tk.Entry, bg = 'white', bd = 3)
fileEntry.place(x=90, y=10)

camera_label_left = Label(camera_frame_left)
camera_label_left.place(x=0, y=0)

camera_label_right = Label(camera_frame_right)
camera_label_right.place(x=0, y=0)



#-----Motor Table Frame-----#
Table(motor_frame, table_list)



#---------Camera Stuff---------#

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

#---Cam Buttons---#
#button to switch to the left camera view
#LeftCam = Button(window, text = 'Left')
#LeftCam.config(command=clickLeft, height = 2, width = 5)
#eftCam.place(x=50, y = 250)

#button to switch to the right camera view
#RightCam = Button(window, text = "Right")
#RightCam.config(command=clickRight, height=2,width=5)
#RightCam.place(x=150,y=250)


#-----------Planning-----------#
rightCam = Label(window, text="", font=('Times New Roman', 30))
rightCam.place(x=50,y=150)

leftCam = Label(window, text="", font = ('Times New Roman', 30))
leftCam.place(x=50,y=150)


#---Camera Views---#
# Open the cam (0 is the default camera)
cap = cv2.VideoCapture(0)
cap1 = cv2.VideoCapture(1)

if not cap.isOpened() or not cap1.isOpened():
    print("Cannot open camera")
    exit()

#---File input---#
#entry = Entry()
#entry.config(font=('Times New Roman', 30), width=10)
#entry.place(x=700,y=10)
#fileEntry = Label(window, text = "Filename:", font=('Times New Roman', 20))
#fileEntry.place(x=660, y=105)

#button to save text input
#submit = Button(window, text="Submit")
#submit.config(command=Submit, height=2, width=3)
#submit.place(x=900,y=125)

#--------Start/Stop--------#
#button to start
#Start = Button(window, text = "Start")
#Start.config(command=clickStart, height=2,width=5)
#Start.place(x=500,y=250)

#button to stop
#Stop = Button(window, text = "Stop")
#Stop.config(command=clickStop, height=2,width=5)
#Stop.place(x=500,y=300)

#---Stats---#


#---Localization---#



#-----Print to screen-----#
update_camera(cap, camera_label_left)
update_camera(cap1, camera_label_right)
window.mainloop()
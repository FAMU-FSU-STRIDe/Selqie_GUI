from tkinter import *
import tkinter as tk
import cv2, queue, threading
from PIL import Image, ImageTk
import threading
import math
import subprocess, shlex
#from actuation_msgs import msg
#import rclpy
#from rclpy.node import Node
#from std_msgs.msg import String
#from rclpy.qos import QoSProfile, ReliabilityPolicy

#use subprocess so the first thing gui does is open up tmux

#tmux_path = "/selqie/blahs"

#subprocess.Popen(["start", "cmd", "/k", "echo Hello from new terminal! && pause"], shell=True)

#subprocess.Popen(["open", "-a", "Terminal", "--args", "sh", "-c"])

#for mac
target_directory = "/Users/maddyboss/Desktop/gui" 
script=f'tell application "Terminal" to do script "cd {target_directory}"'
subprocess.Popen(["osascript", "-e", script])


#for linux
#target_directory="/home/" figure out path to tmux
#subprocess.Popen(["gnome-terminal", "--working-directory", target_directory])

#Table class to create table for status
#------Table Class-------#
class Table:
    def __init__(self, parent, data, x=0, y=0):
        frame = Frame(parent)
        frame.place(x=x, y=y)
        entries = []
        for i in range(total_rows):
            row_entries = []
            for j in range(total_columns):
                e = Entry(frame, width = 24, fg = 'black')
                e.grid(row=i, column=j)
                e.insert(END, data[i][j])
                row_entries.append(e)
            entries.append(row_entries)
        
    #live updates for the status as it gets info from ROS
    def update_cell (self, row, col, value):
        entries[row][col].delete(0, END)
        entries[row][col].insert(0, value)

#outline for table
part_status = [(f'Motor Driver {i} Temp', '--') for i in range (0,8)]
total_rows = len(part_status)
total_columns = 2

#------------------Graph for Torque Tracker-------------------#
def draw_graph_paper(torque, width, height, spacing=20):
    for i in range(0, width, spacing):
        torque.create_line(i, 0, i, height, fill="lightgray")
    for j in range(0, height, spacing):
        torque.create_line(0, j, width, j, fill="lightgray")


#pulling video from default camera 
#-----------Camera Update Func----------#
def update_camera():
    ret, frame = cap.read()
    if ret:
        label_width = camera_label.winfo_width()
        label_height = camera_label.winfo_height()

        if label_width <= 1 or label_height <=1:
            label_width = 485
            label_height = 400
        
        frame = cv2.resize(frame, (label_width, label_height))
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(frame)
        imgtk = ImageTk.PhotoImage(image = img)

        camera_label.imgtk = imgtk
        camera_label.configure(image = imgtk)

    camera_label.after(10, update_camera)



#--------Helper Function Definitions--------#
def create_widget(parent, widget_type, **options):
    return widget_type(parent, **options)

def create_button(parent, text, fg):
    return create_widget(parent, tk.Button, text=text, fg=fg, bg='lightblue', bd=3, cursor='hand1', highlightbackground = '#E1E4ED', relief = tk.RAISED)

def create_label(parent, text, fg):
    return create_widget(parent, tk.Label, text=text, fg=fg, bg = "#E6EAF5", bd=3, cursor='hand1', highlightbackground = '#E1E4ED')

#--------Dropdown Tracking--------#
def on_selection_change(*args):
    selection = selected_gait.get()
    if selection != "Choice":
        print("Selected:", selection)

def on_gait_change(*args):
    gait = selected_gait.get()

    if gait == "run_trajectory":
        param1_options = ["Choice", "walk.txt", "idk.txt"]
        param2_options = ["Choice", "5"]
        param3_options = ["Choice", "idk"]
        param3_drop.config(state = "normal")

    elif gait == "swim":
        param1_options = ["Choice", "idk.txt", "idk.txt"]
        param2_options = ["Choice", "idk"]
        param3_options = [""]
        param3_selc.set("              ")
        param3_drop.config(state = "disabled")
    
    else:
        param1_options = []
        param2_options = []
        param3_options = []
        param3_selc.set("              ")
        param3_drop.config(state = "disabled")

    param1_drop['menu'].delete(0, 'end')
    for opt in param1_options:
        param1_drop['menu'].add_command(label = opt, command = tk._setit(param1_selc, opt))
    param1_selc.set(param1_options[0])

    param2_drop['menu'].delete(0, 'end')
    for opt in param2_options:
        param2_drop['menu'].add_command(label = opt, command = tk._setit(param2_selc, opt))
    param2_selc.set(param2_options[0])

    param3_drop['menu'].delete(0, 'end')
    for opt in param3_options:
        param3_drop['menu'].add_command(label = opt, command = tk._setit(param3_selc, opt))
    param3_selc.set(param3_options[0])

    #repopulate the og menu
    for var, drop, opts in [
        (param1_selc, param1_drop, param1_options)
        (param2_selc, param2_drop, param2_options)
        (param3_selc, param3_drop, param3_options)
    ]:
        drop['menu'].delete(0, 'end')
        for opt in opts:
            drop['menu'].add_command(label=opt, command=tk._setit(var, opt))
        if opts:
            var.set(opts[0])

def clear_parameters():
    param1_selc.set("           ")
    param2_selc.set("           ")
    param3_selc.set("           ")
    selected_gait.set("Choice")
    param3_drop.config(state = "normal")

def on_submit():
    gait=selected_gait.get()
    p1=param1_selc.get()
    p2=param2_selc.get()
    p3=param3_selc.get()

    #validation
    if gait == "Choice":
        tk.messagebox.showerror("Missing choice", "Select a gait first")
        return
    
    cmd_parts=["python3", "V4.py", "--gait", gait]
    if p1 and p1 != "Choice":
        cmd_parts += ["--param1", p1]
    if p2 and p2 != "Choice":
        cmd_parts += ["--param2", p2]
    if p3 and p3 != "Choice":
        cmd_parts += ["--param3", p3]
    #send to tmux
    #pane = 
    #subprocess.run(["tmux", "send-keys", "-t", pane, " ".join(shlex.quote(p) for p in cmd_parts), "C-m"])

    print("Launched:", cmd_parts)
#-----Torque Graph-----#
#padding dimensions
graph_padding = {
    'left':50, 
    'bottom':40, 
    'top':5, 
    'right':10
}

def draw_graph_axes(canvas, width, height, spacing = 20):
    canvas.delete("grid")

    x0 = graph_padding['left']
    y0 = graph_padding['top']
    x1 = width - graph_padding['right']
    y1 = height - graph_padding['bottom']

    total_seconds = 300
    small_tick_interval = 10
    seconds_per_pixel = total_seconds/(x1-40)

    #-----GRID LINES-------#
    for x in range(x0, x1, spacing):
        canvas.create_line(x, y0, x, y1, fill = "lightgray", tags = "grid")
    
    for y in range(y0, y1, spacing):
        canvas.create_line(x0, y, x1, y, fill = "lightgray", tags = "grid")
    
    #-----X TICKS-----#
    for t in range(0, total_seconds + 1, small_tick_interval):
        x = x0 + t / seconds_per_pixel
        tick_height = 10 if t % 60 == 0 else 5
        canvas.create_line(x, y1, x, y1 + tick_height, fill = "black", tags = "grid")

        if t % 60 == 0:
            minutes = t//60
            canvas.create_text(x, y1 + 15, text = f"{minutes}m", tags = "grid")

    #------Y TICKS------#
    torque_max = 10
    torque_tick = 2
    pixels_per_nm = (y1-y0) / torque_max

    for torque_val in range(0, torque_max + 1, torque_tick):
        y = y1 - (torque_val * pixels_per_nm)
        tick_w = 10 if torque_val % 5 == 0 else 5
        canvas.create_line(x0 - tick_w, y, x0, y, fill = "black", tags = "grid")

        if torque_val % 2 == 0:
            canvas.create_text(x0 - 20, y, text = f"{torque_val}", anchor = "e", tags = "grid")
    
    #-----AXES LINES-----#
    canvas.create_line(x0, y0, x0, y1, width = 2, fill = "black", tags = "grid")    #y axis
    canvas.create_line(x0, y1, x1, y1, width = 2, fill = "black", tags = "grid")    #x axis

    #------AXIS LABELS-----#
    #canvas.create_text((x0 + x1) // 2, y1 + 20, text = "Time (s)", tags = "grid")
    canvas.create_text((x0 + x1) // 2, height - 10, text = "Time (min)", tags = "grid")

    #canvas.create_text(x0 - 25, (y0 + y1) // 2, text = "Torque ()", angle = 90, tags = "grid")
    canvas.create_text(20, (y0 + y1) // 2, text = "Torque (Nm)", angle = 90, tags = "grid")

def refresh_graph(event = None):
    draw_graph_axes(torque, torque.winfo_width(), torque.winfo_height())

#-----Error Log Buttons-----#
def print_error():
    error_display.insert(tk.END)
    error_display.see(tk.END)

def clear_error():
    error_display.delete('1.0', tk.END)

#----Camera Thread and Queue-----#
frame_q = queue.Queue(maxsize = 1)
running = True

def camera_work():
    #cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    cap = cv2.VideoCapture(0)
    while running and cap.isOpened():
        ret, frame = cap.read()
        if ret and not frame_q.full():
            frame_q.put(frame)
    cap.release()

#--------Window Init--------#
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

#--------Frames--------#
camera_frame = create_widget(window, tk.Frame, bg="#E6EAF5", bd = 2, height = 450, highlightcolor = 'red', highlightthickness=2, highlightbackground = 'black', relief = tk.RAISED, width = 500)
camera_frame.place(relx=0.003, rely=0.01, relwidth=0.335, relheight=0.6)

control_frame = create_widget(window, tk.Frame, bg="#E6EAF5", bd = 2, height = 150, highlightcolor = 'red', highlightthickness=2, highlightbackground = 'black', relief = tk.RAISED, width = 485)
control_frame.place(relx=0.34, rely=0.01, relwidth=0.656, relheight=0.205)

status_frame = create_widget(window, tk.Frame, bg="#E6EAF5", bd = 2, height = 285, highlightcolor = 'red', highlightthickness=2, highlightbackground = 'black', relief = tk.RAISED, width = 500)
status_frame.place(relx=0.34, rely=0.22, relwidth=0.325, relheight=0.775)

torque_frame = create_widget(window, tk.Frame, bg="#E6EAF5", bd = 2, height = 435, highlightcolor = 'red', highlightthickness=2, highlightbackground = 'black', relief = tk.RAISED, width = 485)
torque_frame.place(relx=0.668, rely=0.22, relwidth=0.329, relheigh=0.775)

error_frame = create_widget(window, tk.Frame, bg="#E6EAF5", bd = 2, height = 500, highlightcolor = 'red', highlightthickness=2, highlightbackground = 'black', relief = tk.RAISED, width = 500)
error_frame.place(relx = 0.003, rely = 0.615, relwidth = 0.335, relheight = 0.38)

#--------Camera--------#
camera_label = Label(camera_frame)
camera_label.place(relx=0.003, rely=0, relwidth = 0.99, relheight = 0.90)

def poll_camera():
    if not frame_q.empty():
        frame = frame_q.get()
        h = camera_label.winfo_height()
        w = camera_label.winfo_width()
        if w <= 1 or h <= 1:
            w,h = 485, 400
        
        frame = cv2.resize(frame, (w,h))
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        imgtk = ImageTk.PhotoImage(image = Image.fromarray(frame))

        camera_label.imgtk = imgtk
        camera_label.configure(image=imgtk)
    window.after(33, poll_camera)


#--------Control Center--------#
#Buttons
zero = create_button(control_frame, "Zero", "black")
zero.place(relx = 0.03, rely = 0.1, relwidth = 0.2, relheight = 0.15)

idle = create_button(control_frame, "Idle", "black")
idle.place(relx = 0.03, rely = 0.35, relwidth = 0.2, relheight = 0.15)

ready = create_button(control_frame, "Ready", "black")
ready.place(relx = 0.03, rely = 0.6, relwidth = 0.2, relheight = 0.15)

stand = create_button(control_frame, "Stand", "black")
stand.place(relx = 0.25, rely = 0.1, relwidth = 0.2, relheight = 0.15)

start = create_button(control_frame, "Start", "black")
start.place(relx = 0.25, rely = 0.35, relwidth = 0.2, relheight = 0.15)

stop = create_button(control_frame, "Stop", "black")
stop.place(relx = 0.25, rely = 0.6, relwidth = 0.2, relheight = 0.15)

#clear = create_button(control_frame, "Clear", "black")
#clear.place(relx = 0.3, rely = 0.7, relwidth = 0.2, relheight = 0.1)
#clear.config(command = clear_parameters)

#Gait and parameter drop downs
gait_label = create_label(control_frame, "Gait selection:", "black")
gait_label.place(relx = 0.5, rely = 0.1, relwidth = 0.1, relheight = 0.1)
gait_options = ["Choice", "run_trajectory", "swim"]
selected_gait = StringVar()
selected_gait.set(gait_options[0])
selected_gait.trace_add("write", on_gait_change)
dropdown_gait = tk.OptionMenu(control_frame, selected_gait, *gait_options)
dropdown_gait.place(relx = 0.63, rely = 0.1, relwidth = 0.2, relheight = 0.1)

param1_label = create_label(control_frame, "Parameter 1", "black")
param1_label.place(relx = 0.5, rely = 0.25, relwidth = 0.1, relheight = 0.1)

param2_label = create_label(control_frame, "Parameter 2", "black")
param2_label.place(relx = 0.5, rely = 0.4, relwidth = 0.1, relheight = 0.1)

param3_label = create_label(control_frame, "Parameter 3", "black")
param3_label.place(relx = 0.5, rely = 0.55, relwidth = 0.1, relheight = 0.1)


param1_selc = StringVar()
param1_selc.set("")
#param1_selc.trace_add("write", on_selection_change)
param1_drop = tk.OptionMenu(control_frame, param1_selc, "")
param1_drop.place(relx = 0.63, rely = 0.25, relwidth = 0.2, relheight = 0.1)

param2_selc = StringVar()
param2_selc.set("")
param2_drop = tk.OptionMenu(control_frame, param2_selc, "")
param2_drop.place(relx = 0.63, rely = 0.4, relwidth = 0.2, relheight = 0.1)

param3_selc = StringVar()
param3_selc.set("")
param3_drop = tk.OptionMenu(control_frame, param3_selc, "")
param3_drop.place(relx = 0.63, rely = 0.55, relwidth = 0.2, relheight = 0.1)

selected_gait.trace_add('write', on_gait_change)
submit_btn=create_button(control_frame, "Submit", 'black')
submit_btn.config(command=on_submit)
submit_btn.place(relx=0.85, rely=0.3, relwidth=0.1, relheight=0.2)
#--------Torque--------#
#torque = Canvas(torque_frame, height=420, width=460, bg = "#FFFFFF")
torque = Canvas(torque_frame, bg = "#FFFFFF")
torque.pack(fill = "both", expand = True)
#torque.pack(padx=5, pady=5)
#draw_graph_paper(torque, 455, 450)
torque.bind("<Configure>", refresh_graph)

#-------Status Table------#
table = Table(status_frame, part_status)

#-------Error Log------#
error_label = create_label(error_frame, "Error Log", "black")
error_label.place(relx = 0.03, rely = 0.02, relwidth = 0.4, relheight = 0.08)

error_display = tk.Text(error_frame, wrap = "word", bg = "white", fg = "red")
error_display.place(relx = 0.03, rely = 0.12, relwidth = 0.94, relheight = 0.65)

scrollbar = tk.Scrollbar(error_frame, command = error_display.yview)
scrollbar.place(relx = 0.97, rely = 0.12, relwidth = 0.02, relheight = 0.65)
error_display.config(yscrollcommand=scrollbar.set)

print_btn = create_button(error_frame, "Print Errors", "black")
print_btn.place(relx = 0.03, rely = 0.8, relwidth = 0.44, relheight = 0.15)
print_btn.config(command = print_error)

clear_btn = create_button(error_frame, "Clear", "black")
clear_btn.place(relx = 0.53, rely = 0.8, relwidth = 0.44, relheight = 0.15)
clear_btn.config(command = clear_error)


#--------Start--------#
threading.Thread(target = camera_work, daemon=True).start()
poll_camera()
#update_camera()
#update_gui()
window.mainloop()
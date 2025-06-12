from tkinter import *
import tkinter as tk
import cv2
from PIL import Image, ImageTk
import threading
from actuation_msgs import MotorInfo, MotorEstimate
import rclpy
from rclpy.node import Node
from std_msgs.msg import String

#--------ROS Subscriber Node--------#
class GUI_Sub(Node):
    def __init__(self):
        super().__init__('GUI subscriber')
        self.lock = threading.Lock()
        self.motor_info = {}
        self.motor_torques = {}

        #subscribing to all 8 motors
        for i in range(1,9):
            topic = f"/motor{i}/info"
            self.create_subscription(MotorInfo, topic, self.make_callback(i), 10) #might not work if MotorInfo isn't called MotorInfo in ROS
        
        #subscribing to motor estimate for torque info
        for k in range(1,9):
            topic = f"/motor{k}/estimate"
            self.create_subscription(MotorEstimate, topic, self.make_torque_callback(k), 10)

    def make_torque_callback(self, motor_index):
        def callback(msg):
            self.motor_torques[f"motor{motor_index}"] = msg.torq_estimate
        return callback
    
    def make_callback(self, motor_index):
        def callback(msg):
            with self.lock:
                self.motor_info[f"motor{motor_index}"] = msg.motor_temperature
        return callback
  


#--------Table Class for Motor Section--------#
class Table:
    def __init__(self, parent, data, x=0, y=0):
        self.frame = Frame(parent)
        self.frame.place(x=x, y=y)
        self.entries = []
        for i in range(total_rows):
            row_entries = []
            for j in range(total_columns):
                e = Entry(self.frame, width = 26, fg = 'black')
                e.grid(row=i, column=j)
                e.insert(END, data[i][j])
                row_entries.append(e)
            self.entries.append(row_entries)
        

    def update_cell (self, row, col, value):
        self.entries[row][col].delete(0, END)
        self.entries[row][col].insert(0, value)


part_status = [('Motor Temp', 'Temp'), ('Ouran Temp', 'Temp'), ('Voltage Status', 'Volts')]
total_rows = len(part_status)
total_columns = 2

#-----------Camera Update Func----------#
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


#------------------Graph for Torque Tracker-------------------#
def draw_graph_paper(torque, width, height, spacing=20):
    for i in range(0, width, spacing):
        torque.create_line(i, 0, i, height, fill="lightgray")
    for j in range(0, height, spacing):
        torque.create_line(0, j, width, j, fill="lightgray")

#--------Helper Function Definitions--------#
def create_widget(parent, widget_type, **options):
    return widget_type(parent, **options)

def create_button(parent, text, fg):
    return create_widget(parent, tk.Button, text=text, fg=fg, bg='lightblue', bd=3, cursor='hand1', highlightbackground = '#E1E4ED', relief = tk.RAISED)

def create_label(parent, text, fg):
    return create_widget(parent, tk.Label, text=text, fg=fg, bg = "#E6EAF5", bd=3, cursor='hand1', highlightbackground = '#E1E4ED')

#--------Leak Sensor Lights--------#
def noLeak(no):
    if(no):
        no_leak.itemconfig(noL_circle, fill = 'green')

    else:
        no_leak.itemconfig(noL_circle, fill="#E6EAF5")

def Leak(ohno):
    if(ohno):
        leak.itemconfig(leak_circle, fill = 'red')

    else:
        leak.itemconfig(leak_circle, fill = "#E6EAF5")

#----Buttons for above functions---#
def clickLeak():
    noLeak(False)
    Leak(True)

def clickNo():
    noLeak(True)
    Leak(False)

#--------Window Init--------#
window = Tk()
window.geometry("1000x750")
window.title("SELQIE")

#--------Frames--------#
camera_frame = create_widget(window, tk.Frame, bg="#E6EAF5", bd = 2, cursor = 'hand', height = 450, highlightcolor = 'red', highlightthickness=2, highlightbackground = 'black', relief = tk.RAISED, width = 500)
camera_frame.place(x=5, y=5)

leak_frame = create_widget(window, tk.Frame, bg="#E6EAF5", bd = 2, cursor = 'hand', height = 300, highlightcolor = 'red', highlightthickness=2, highlightbackground = 'black', relief = tk.RAISED, width = 485)
leak_frame.place(x=510, y=5)

status_frame = create_widget(window, tk.Frame, bg="#E6EAF5", bd = 2, cursor = 'hand', height = 285, highlightcolor = 'red', highlightthickness=2, highlightbackground = 'black', relief = tk.RAISED, width = 500)
status_frame.place(x=5, y=460)

torque_frame = create_widget(window, tk.Frame, bg="#E6EAF5", bd = 2, cursor = 'hand', height = 435, highlightcolor = 'red', highlightthickness=2, highlightbackground = 'black', relief = tk.RAISED, width = 485)
torque_frame.place(x=510, y=310)

#--------Camera--------#
camera_label = Label(camera_frame)
camera_label.place(x=0,y=0)

cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Cannot open camera")
    exit(0)


#--------Leak Sensor--------#
leak_label = create_label(leak_frame, "LEAK SENSORS", fg = 'black')
leak_label.config(font = ('Arial', 40))
leak_label.place(x=80, y=10)

no_leak = Canvas(window, height=120, width=160, bg="#E6EAF5")
noL_circle = no_leak.create_oval(40, 40, 160, 120, outline='black', fill="#E6EAF5")
no_leak.place(x=550, y=100)

leak = Canvas(window, height=120, width=160, bg = "#E6EAF5")
leak_circle = leak.create_oval(40, 40, 160, 120, outline = 'black', fill = "#E6EAF5")
leak.place(x=750, y=100)

#---Functionality Buttons---#
#good = Button(leak_frame, "No Leak!")
#good.config(command = clickNo, height = 2, width = 5 )
#good.place(x=)

#bad = Button(leak_frame, "Leak!!!")
#bad.config(command = clickLeak, height = 2, width = 5)

#--------Status--------#
status_table = Table(status_frame, part_status)

#--------Torque--------#
torque = Canvas(torque_frame, height=420, width=460, bg = "#FFFFFF")
torque.pack(padx=5, pady=5)
draw_graph_paper(torque, 455, 450)

#--------ROS2 Integration--------#
def ros2_spin_thread(node):
    rclpy.spin(node)

rclpy.init()
ros_node = GUI_Sub()
threading.Thread(target = ros2_spin_thread, args=(ros_node,), daemon=True).start()

def update_gui():
    with ros_node.lock:
       for i in range(1,9):
           motor_key = f"motor{i}"
           #check for available data
           if motor_key in ros_node.motor_info:
               #update
               status_table.update_cell(i, 1, f"{ros_node.motor_info[motor_key]:.2f}")
    window.after(100, update_gui)

#--------Start--------#
update_camera()
update_gui()
window.mainloop()

#--------Clean Shutdown--------#
ros_node.destroy_node()
rclpy.shutdown()
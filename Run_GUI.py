from GUI_Classes import Table, Camera, ControlPanel, ErrorLog, Torque 
from tkinter import *
import tkinter as tk
import cv2, queue, threading
import rclpy
import math

#-----Tkinter setup--------------------------------------------------------------------------------#
window = Tk()
#window.geometry("1500x750")
window.attributes("-fullscreen", True)
window.bind("<Escape>", lambda e: window.attributes("-fullscreen", False))  # Esc to exit
window.title("SELQIE")

def on_closing():
    running = False
    camera.running = False
    window.destroy()

window.protocol("WM_DELETE_WINDOW", on_closing)

#-----Frames------------------------------------------------------------------------------------------#
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

torque_frame = create_widget(window, tk.Frame, bg="#E6EAF5", bd = 2, height = 435, highlightcolor = 'red', highlightthickness=2, highlightbackground = 'black', relief = tk.RAISED, width = 485)
torque_frame.place(relx=0.668, rely=0.22, relwidth=0.329, relheigh=0.775)


#-----Widgets------------------------------------------------------------------------------------------#
part_status = [(f'Motor Driver {i} Temp', '--') for i in range (0,8)]


table = Table(status_frame, part_status)
camera = Camera(camera_frame, 0.003, 0, 0.99, 0.90)
control = ControlPanel(control_frame)
error = ErrorLog(error_frame)
torque = Torque(torque_frame)
torque.refresh_graph()

#-----ROS Setup------------------------------------------------------------------------------------------#
rclpy.init()
ros_node = GUISub()

#-----Threading-------------------------------------------------------------------------------------------#
gui_running = [True]

#camera thread
threading.Thread(target = camera.camera_queue, daemon=True).start()
camera.poll_camera()

#ROS spin thread
def ros_spin():
    while gui_running[0]:
        rclpy.spin_once(ros_node, timeout_sec=0.1)

threading.Thread(target=ros_spin, daemon = True).start()

#GUI update loop
def update_gui():
    with ros_node.lock:
        for i in range(8):
            motor_key = f"motor{i}"
            if motor_key in ros_node.motor_info:
                temp = ros_node.motor_info[motor_key]
                if isinstance(temp, (int, float)) and not math.isnan(temp):
                    table.update_cell(i, 1, f"{temp:.2f}")
    if gui_running[0]:
        window.after(100, update_gui)

update_gui()
window.mainloop()
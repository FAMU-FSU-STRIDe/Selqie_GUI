from tkinter import *
import tkinter as tk
import cv2, queue, threading
from PIL import Image, ImageTk


#class for the table element
class Table:
    def __init__(self, parent, data, x=0, y=0):
        frame = Frame(parent)   #constructor creating a Frame instance inside the parent widget
        frame.place(x=x, y=y)
        self.entries = []   #creating an instance variable to hold the entries

        #dynamically create the table based on the data provided
        total_rows = len(data)
        total_columns = len(data[0]) if data else 0
        for i in range(total_rows):
            row_entries = []
            for j in range(total_columns):
                e = Entry(frame, width=24, fg='black')
                e.grid(row=i, column=j)
                e.insert(END, data[i][j])
                row_entries.append(e)
            self.entries.append(row_entries)
        
    #live updates for the status as it gets info from ROS
    def update_cell (self, row, col, value):
        self.entries[row][col].delete(0, END)
        self.entries[row][col].insert(0, value)

    
#class for the camera element
class Camera(tk.Label):
    def __init__(self, parent, relx, rely, relwidth, relheight):
        super().__init__(parent)
        self.place(relx=relx, rely=rely, relwidth=relwidth, relheight=relheight)
        self.frame_q = queue.Queue(maxsize = 1)
        self.running = True
        self.frame = None

    def camera_queue(self):
        cap = cv2.VideoCapture(0)
        while self.running and cap.isOpened():
            ret, frame = cap.read()
            if ret and not self.frame_q.full():
                self.frame_q.put(frame)
        cap.release()

    def poll_camera(self):
        if not self.frame_q.empty():
            self.frame = self.frame_q.get()
            h = self.winfo_height()
            w = self.winfo_width()
            if w<=1 or h<=1:
                w,h=485,400

            self.frame = cv2.resize(self.frame, (w,h))
            self.frame = cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGB)
            imgtk = ImageTk.PhotoImage(image=Image.fromarray(self.frame))

            self.imgtk = imgtk
            self.configure(image=imgtk)
        
        if self.running:
             self.after(33, self.poll_camera)  # roughly 30 FPS


        
#class for the control panel element
class ControlPanel():
    def __init__(self, parent):
        #buttons for control panel
        zero = self.create_button(parent, "Zero", 'black')
        zero.place(relx = 0.03, rely = 0.1, relwidth = 0.2, relheight = 0.15)

        idle = self.create_button(parent, "Idle", 'black')
        idle.place(relx = 0.03, rely = 0.35, relwidth = 0.2, relheight = 0.15)

        ready = self.create_button(parent, "Ready", 'black')
        ready.place(relx = 0.03, rely = 0.6, relwidth = 0.2, relheight = 0.15)

        stand = self.create_button(parent, "Stand", 'black')
        stand.place(relx = 0.25, rely = 0.1, relwidth = 0.2, relheight = 0.15)

        start = self.create_button(parent, "Start", 'black')
        start.place(relx = 0.25, rely = 0.35, relwidth = 0.2, relheight = 0.15)

        stop = self.create_button(parent, "Stop", 'black')
        stop.place(relx = 0.25, rely = 0.6, relwidth = 0.2, relheight = 0.15)

    
    def create_widget(self, parent, widget_type, **options):
        return widget_type(parent, **options)

    def create_button(self, parent, text, fg):
        return self.create_widget(parent, tk.Button, text=text, fg=fg, bg='lightblue', bd=3, cursor='hand1', highlightbackground = '#E1E4ED', relief = tk.RAISED)
    

#class for error log element
class ErrorLog():
    def __init__(self, parent):
        self.error_label = self.create_label(parent, "Error Log", 'black')
        self.error_label.place(relx = 0.03, rely = 0.02, relwidth = 0.4, relheight = 0.08)

        self.error_display = tk.Text(parent, wrap = "word", bg = "white", fg = "red")
        self.error_display.place(relx = 0.03, rely = 0.12, relwidth = 0.94, relheight = 0.65)

        self.scrollbar = tk.Scrollbar(parent, command=self.error_display.yview)
        self.scrollbar.place(relx = 0.97, rely = 0.12, relwidth = 0.02, relheight=0.65)
        self.error_display.config(yscrollcommand=self.scrollbar.set)

        self.print_btn = self.create_button(parent, "Print Errors", 'black')
        self.print_btn.place(relx = 0.03, rely = 0.8, relwidth = 0.44, relheight = 0.15)
        self.print_btn.config(command=self.print_error)

        self.clear_btn = self.create_button(parent, "Clear Errors", 'black')
        self.clear_btn.place(relx = 0.53, rely = 0.8, relwidth = 0.44, relheight = 0.15)
        self.clear_btn.config(command=self.clear_error)


    def create_widget(self, parent, widget_type, **options):
        return widget_type(parent, **options)
    
    def create_label(self, parent, text, fg):
        return self.create_widget(parent, tk.Label, text=text, fg=fg,bg = "#E6EAF5", bd=3, cursor='hand1', highlightbackground = '#E1E4ED')
    
    def create_button(self, parent, text, fg):
        return self.create_widget(parent, tk.Button, text=text, fg=fg, bg = "#E6EAF5", bd=3, cursor='hand1', highlightbackground = '#E1E4ED')
    
    def print_error(self):
        #self.error_display.insert(tk.END)
        #self.error_dsiplay.see(tk.END)
        content = self.error_display.get("1.0", tk.END).strip()
        print("Error Log Contents:\n", content)
    
    def clear_error(self):
        self.error_display.delete(1.0, tk.END)

#class for torque tracker
class Torque():
    def __init__(self, parent):
        self.canvas = Canvas(parent, bg = 'white')
        self.canvas.pack(fill = "both", expand = True)
        self.canvas.bind("<Configure>", self.refresh_graph)
        self.graph_padding = {
            'left':50, 
            'bottom':40, 
            'top':5, 
            'right':10
        }

        

    def draw_graph_axes(self, width, height, spacing = 20):
        canvas = self.canvas
        canvas.delete("grid")

        x0 = self.graph_padding['left']
        y0 = self.graph_padding['top']
        x1 = width - self.graph_padding['right']
        y1 = height - self.graph_padding['bottom']

        total_seconds = 300
        small_tick_interval = 10
        seconds_per_pixel = total_seconds / (x1 - 40)

        #grid lines
        for x in range(x0, x1, spacing):
            canvas.create_line(x, y0, x, y1, fill = 'lightgray', tags = 'grid')

        for y in range(y0, y1, spacing):
            canvas.create_line(x0, y, x1, y, fill = 'lightgray', tags = 'grid')

        #x ticks
        for t in range(0, total_seconds + 1, small_tick_interval):
            x = x0 + t/seconds_per_pixel
            tick_height = 10 if t % 60 == 0 else 5
            canvas.create_line(x, y1, x, y1 + tick_height, fill = 'black', tags = 'grid')

        if t % 60 == 0:
            minutes = t/60
            canvas.create_text(x, y1 + tick_height + 15, text=f"{int(minutes)}m", fill='black', tags='grid')

        #y ticks
        torque_max = 10
        torque_tick = 2
        pixels_per_nm = (y1 - y0) / torque_max

        for torque_val in range(0, torque_max + 1, torque_tick):
            y = y1 - (torque_val * pixels_per_nm)
            tick_w = 10 if torque_val % 5 == 0 else 5
            canvas.create_line(x0 - tick_w, y, x0, y, fill='black', tags='grid')

            if torque_val % 2 == 0:
                canvas.create_text(x0 - tick_w - 5, y, text=str(torque_val), fill='black', anchor='e', tags='grid')

        #axes lines
        canvas.create_line(x0, y0, x0, y1, width = 2, fill='black', tags='grid')
        canvas.create_line(x0, y1, x1, y1, width = 2, fill='black', tags='grid')

        #axes labels
        canvas.create_text((x0 + x1) // 2, height - 10, text = "Time (min)", tags = 'grid')
        canvas.create_text(20, (y0 + y1) // 2, text = "Torque (Nm)", angle = 90, tags = 'grid')

    def refresh_graph(self, event=None):
        width = self.canvas.winfo_width()
        height = self.canvas.winfo_height()
        self.draw_graph_axes(width, height)
from tkinter import *
import tkinter as tk


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
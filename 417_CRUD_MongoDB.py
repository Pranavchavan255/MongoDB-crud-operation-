import tkinter as tk
from tkinter import messagebox
from pymongo import MongoClient

# Connect to MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["employee_db"]
collection = db["employees"]

# Main window
root = tk.Tk()
root.title("Employee Management")
root.geometry("500x400")

# Employee fields
fields = ["Employee ID", "Name", "Age", "Department", "Email"]
entries = {}

# Input form
for idx, field in enumerate(fields):
    label = tk.Label(root, text=field)
    label.grid(row=idx, column=0, padx=10, pady=5, sticky='w')
    entry = tk.Entry(root, width=30)
    entry.grid(row=idx, column=1, padx=10, pady=5)
    entries[field] = entry

# CRUD Operations
def create_employee():
    data = {field: entries[field].get() for field in fields}
    if not all(data.values()):
        messagebox.showwarning("Warning", "All fields are required.")
        return
    if collection.find_one({"Employee ID": data["Employee ID"]}):
        messagebox.showerror("Error", "Employee ID already exists.")
        return
    collection.insert_one(data)
    messagebox.showinfo("Success", "Employee created successfully.")

def read_employees():
    employees = list(collection.find({}, {"_id": 0}))
    if not employees:
        messagebox.showinfo("Info", "No employees found.")
        return
    text = "\n".join([f"{e['Employee ID']} | {e['Name']} | {e['Age']} | {e['Department']} | {e['Email']}" for e in employees])
    messagebox.showinfo("Employees", text)

def update_employee():
    emp_id = entries["Employee ID"].get()
    if not emp_id:
        messagebox.showwarning("Warning", "Employee ID is required for update.")
        return
    new_data = {field: entries[field].get() for field in fields if field != "Employee ID"}
    result = collection.update_one({"Employee ID": emp_id}, {"$set": new_data})
    if result.modified_count:
        messagebox.showinfo("Success", "Employee updated.")
    else:
        messagebox.showerror("Error", "Employee not found or no changes.")

def delete_employee():
    emp_id = entries["Employee ID"].get()
    if not emp_id:
        messagebox.showwarning("Warning", "Employee ID is required for deletion.")
        return
    result = collection.delete_one({"Employee ID": emp_id})
    if result.deleted_count:
        messagebox.showinfo("Success", "Employee deleted.")
    else:
        messagebox.showerror("Error", "Employee not found.")

# Button Frame
button_frame = tk.Frame(root)
button_frame.grid(row=6, column=0, columnspan=2, pady=20)

btn_config = {"width": 10, "bg": "white", "padx": 5, "pady": 5}

tk.Button(button_frame, text="Create", command=create_employee, **btn_config).grid(row=0, column=0)
tk.Button(button_frame, text="Read", command=read_employees, **btn_config).grid(row=0, column=1)
tk.Button(button_frame, text="Update", command=update_employee, **btn_config).grid(row=0, column=2)
tk.Button(button_frame, text="Delete", command=delete_employee, **btn_config).grid(row=0, column=3)

# Run the GUI
root.mainloop()

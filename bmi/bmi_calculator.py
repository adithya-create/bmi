import tkinter as tk
from tkinter import messagebox, ttk
import csv
import os
from datetime import datetime

# File to store BMI records
FILE_NAME = "bmi_records.csv"


# Function to calculate BMI
def calculate_bmi():
    try:
        name = name_entry.get().strip()
        weight = float(weight_entry.get())
        height = float(height_entry.get())

        # Input validation
        if name == "":
            messagebox.showerror("Error", "Please enter your name.")
            return

        if weight <= 0 or height <= 0:
            messagebox.showerror("Error", "Weight and Height must be greater than 0.")
            return

        # BMI Formula
        bmi = weight / (height ** 2)
        bmi = round(bmi, 2)

        # BMI Category
        if bmi < 18.5:
            category = "Underweight"
        elif bmi < 24.9:
            category = "Normal Weight"
        elif bmi < 29.9:
            category = "Overweight"
        else:
            category = "Obese"

        # Display result
        result_label.config(
            text=f"BMI: {bmi}\nCategory: {category}"
        )

        # Save data to CSV
        save_data(name, weight, height, bmi, category)

    except ValueError:
        messagebox.showerror("Error", "Please enter valid numbers.")


# Function to save data
def save_data(name, weight, height, bmi, category):
    file_exists = os.path.isfile(FILE_NAME)

    with open(FILE_NAME, mode="a", newline="") as file:
        writer = csv.writer(file)

        # Add headers if file doesn't exist
        if not file_exists:
            writer.writerow(["Date", "Name", "Weight", "Height", "BMI", "Category"])

        writer.writerow([
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            name,
            weight,
            height,
            bmi,
            category
        ])


# Function to view history
def view_history():
    history_window = tk.Toplevel(root)
    history_window.title("BMI History")
    history_window.geometry("700x300")

    tree = ttk.Treeview(history_window)
    tree["columns"] = ("Date", "Name", "Weight", "Height", "BMI", "Category")

    tree.column("#0", width=0, stretch=tk.NO)

    for col in tree["columns"]:
        tree.column(col, anchor=tk.CENTER, width=100)
        tree.heading(col, text=col)

    tree.pack(fill="both", expand=True)

    # Read CSV data
    if os.path.exists(FILE_NAME):
        with open(FILE_NAME, mode="r") as file:
            reader = csv.reader(file)
            next(reader, None)  # Skip header

            for i, row in enumerate(reader):
                tree.insert(parent="", index="end", iid=i, values=row)
    else:
        messagebox.showinfo("Info", "No records found.")


# Main Window
root = tk.Tk()
root.title("BMI Calculator")
root.geometry("400x450")
root.config(bg="#f0f0f0")

# Title
title_label = tk.Label(
    root,
    text="BMI Calculator",
    font=("Arial", 20, "bold"),
    bg="#f0f0f0"
)
title_label.pack(pady=15)

# Name
tk.Label(root, text="Enter Name:", bg="#f0f0f0", font=("Arial", 12)).pack()
name_entry = tk.Entry(root, font=("Arial", 12), width=25)
name_entry.pack(pady=5)

# Weight
tk.Label(root, text="Enter Weight (kg):", bg="#f0f0f0", font=("Arial", 12)).pack()
weight_entry = tk.Entry(root, font=("Arial", 12), width=25)
weight_entry.pack(pady=5)

# Height
tk.Label(root, text="Enter Height (m):", bg="#f0f0f0", font=("Arial", 12)).pack()
height_entry = tk.Entry(root, font=("Arial", 12), width=25)
height_entry.pack(pady=5)

# Calculate Button
calculate_btn = tk.Button(
    root,
    text="Calculate BMI",
    font=("Arial", 12, "bold"),
    bg="lightblue",
    command=calculate_bmi
)
calculate_btn.pack(pady=15)

# Result Label
result_label = tk.Label(
    root,
    text="Your BMI Result Will Appear Here",
    font=("Arial", 12),
    bg="#f0f0f0"
)
result_label.pack(pady=10)

# View History Button
history_btn = tk.Button(
    root,
    text="View History",
    font=("Arial", 11),
    bg="lightgreen",
    command=view_history
)
history_btn.pack(pady=10)

# Run App
root.mainloop()
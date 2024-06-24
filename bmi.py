import tkinter as tk
from tkinter import messagebox
import sqlite3
import matplotlib.pyplot as plt

# Database setup
conn = sqlite3.connect('bmi_calculator.db')
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS bmi_data (
                 id INTEGER PRIMARY KEY AUTOINCREMENT,
                 weight REAL,
                 height REAL,
                 bmi REAL,
                 category TEXT)''')
conn.commit()

def calculate_bmi(weight, height_cm):
    height_m = height_cm / 100  # Convert height from cm to meters
    return weight / (height_m ** 2)

def classify_bmi(bmi):
    if bmi < 18.5:
        return "Underweight"
    elif 18.5 <= bmi < 24.9:
        return "Normal weight"
    elif 25 <= bmi < 29.9:
        return "Overweight"
    else:
        return "Obesity"

def save_data(weight, height_cm, bmi, category):
    c.execute("INSERT INTO bmi_data (weight, height, bmi, category) VALUES (?, ?, ?, ?)",
              (weight, height_cm, bmi, category))
    conn.commit()

def calculate_and_display_bmi():
    try:
        weight = float(entry_weight.get())
        height_cm = float(entry_height.get())

        if weight <= 0 or height_cm <= 0:
            raise ValueError("Weight and height must be positive values.")

        bmi = calculate_bmi(weight, height_cm)
        category = classify_bmi(bmi)
        save_data(weight, height_cm, bmi, category)

        label_bmi.config(text=f"BMI: {bmi:.2f}")
        label_category.config(text=f"Category: {category}")

        messagebox.showinfo("Result", f"Your BMI is {bmi:.2f} ({category})")
    except ValueError as e:
        messagebox.showerror("Invalid input", str(e))

def show_history():
    c.execute("SELECT * FROM bmi_data")
    records = c.fetchall()
    history = "\n".join([f"Weight: {r[1]} kg, Height: {r[2]} cm, BMI: {r[3]:.2f}, Category: {r[4]}" for r in records])
    messagebox.showinfo("History", history)

def plot_history():
    c.execute("SELECT id, bmi FROM bmi_data")
    data = c.fetchall()
    if not data:
        messagebox.showwarning("No data", "No historical data to plot.")
        return

    ids, bmis = zip(*data)
    plt.plot(ids, bmis, marker='o')
    plt.title("BMI History")
    plt.xlabel("Record ID")
    plt.ylabel("BMI")
    plt.show()

# GUI setup
root = tk.Tk()
root.title("BMI Calculator")

tk.Label(root, text="Weight (kg):").grid(row=0, column=0)
tk.Label(root, text="Height (cm):").grid(row=1, column=0)

entry_weight = tk.Entry(root)
entry_height = tk.Entry(root)

entry_weight.grid(row=0, column=1)
entry_height.grid(row=1, column=1)

tk.Button(root, text="Calculate BMI", command=calculate_and_display_bmi).grid(row=2, column=0, columnspan=2)
tk.Button(root, text="Show History", command=show_history).grid(row=3, column=0, columnspan=2)
tk.Button(root, text="Plot History", command=plot_history).grid(row=4, column=0, columnspan=2)

label_bmi = tk.Label(root, text="BMI: N/A")
label_bmi.grid(row=5, column=0, columnspan=2)

label_category = tk.Label(root, text="Category: N/A")
label_category.grid(row=6, column=0, columnspan=2)

root.mainloop()

# Close database connection on exit
conn.close()

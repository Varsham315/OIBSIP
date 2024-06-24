import tkinter as tk
from tkinter import messagebox
import random
import string
import pyperclip

def generate_password(length, use_letters, use_numbers, use_symbols):
    character_set = ''
    if use_letters:
        character_set += string.ascii_letters
    if use_numbers:
        character_set += string.digits
    if use_symbols:
        character_set += string.punctuation

    if not character_set:
        raise ValueError("At least one character set must be selected.")

    return ''.join(random.choice(character_set) for _ in range(length))

def on_generate():
    try:
        length = int(entry_length.get())
        use_letters = var_letters.get()
        use_numbers = var_numbers.get()
        use_symbols = var_symbols.get()

        if length <= 0:
            raise ValueError("Password length must be a positive integer.")

        password = generate_password(length, use_letters, use_numbers, use_symbols)
        entry_result.delete(0, tk.END)
        entry_result.insert(0, password)
    except ValueError as e:
        messagebox.showerror("Invalid input", str(e))

def on_copy():
    password = entry_result.get()
    if password:
        pyperclip.copy(password)
        messagebox.showinfo("Success", "Password copied to clipboard.")
    else:
        messagebox.showwarning("No password", "No password to copy.")

# GUI setup
root = tk.Tk()
root.title("Password Generator")

tk.Label(root, text="Password Length:").grid(row=0, column=0, sticky='e')
entry_length = tk.Entry(root)
entry_length.grid(row=0, column=1)

var_letters = tk.BooleanVar(value=True)
var_numbers = tk.BooleanVar(value=True)
var_symbols = tk.BooleanVar(value=True)

tk.Checkbutton(root, text="Include Letters", variable=var_letters).grid(row=1, column=0, columnspan=2)
tk.Checkbutton(root, text="Include Numbers", variable=var_numbers).grid(row=2, column=0, columnspan=2)
tk.Checkbutton(root, text="Include Symbols", variable=var_symbols).grid(row=3, column=0, columnspan=2)

tk.Button(root, text="Generate", command=on_generate).grid(row=4, column=0, columnspan=2)
tk.Button(root, text="Copy to Clipboard", command=on_copy).grid(row=5, column=0, columnspan=2)

tk.Label(root, text="Generated Password:").grid(row=6, column=0, sticky='e')
entry_result = tk.Entry(root, width=40)
entry_result.grid(row=6, column=1)

root.mainloop()

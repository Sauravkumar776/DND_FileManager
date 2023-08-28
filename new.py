import os
import json
import tkinter as tk
from tkinterdnd2 import DND_FILES, TkinterDnD
from tkinter import filedialog

def browse_stock_file():
    file_path = filedialog.askopenfilename(filetypes=[("Binary Files", "*.bin *.ori *.hex *.bdc")])
    stock_file_path.set(file_path)

def browse_csv_file():
    file_path = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])
    csv_file_path.set(file_path)

def toggle_vin_entry():
    vin_entry.config(state=tk.NORMAL if vin_checkbox_var.get() else tk.DISABLED)

def on_drop(event, file_var):
    file_path = event.data
    file_var.set(file_path)

def on_drop_stock(event):
    on_drop(event, stock_file_path)

def on_drop_csv(event):
    on_drop(event, csv_file_path)

def save_config(config):
    with open("config.json", "w") as config_file:
        json.dump(config, config_file)

def load_config():
    if os.path.exists("config.json"):
        with open("config.json", "r") as config_file:
            return json.load(config_file)
    return {}

def proceed_to_next_page():
    if vin_checkbox_var.get() and len(vin_value.get()) <= 5:
        error_label.config(text="VIN should be at least 5 characters long.")
    else:
        error_label.config(text="")
        # Perform action to proceed to the next page

root = TkinterDnD.Tk()
root.title("Next GUI")
root.geometry("500x500")

config = load_config()

stock_file_path = tk.StringVar(value=config.get("stock_file_path", ""))
csv_file_path = tk.StringVar(value=config.get("csv_file_path", ""))
vin_checkbox_var = tk.IntVar(value=config.get("vin_checkbox_var", 0))
vin_value = tk.StringVar(value=config.get("vin_value", ""))  # Retrieve VIN value
copy_data_checkbox_var = tk.IntVar(value=config.get("copy_data_checkbox_var", 1))

frame = tk.Frame(root)
frame.pack(padx=20, pady=20, fill="both", expand=True)

stock_label = tk.Label(frame, text="Select Stock File:")
stock_label.pack(fill="x")

stock_entry = tk.Entry(frame, textvariable=stock_file_path)
stock_entry.pack(fill="x", pady=(0, 10))

stock_browse_button = tk.Button(frame, text="Browse", command=browse_stock_file)
stock_browse_button.pack(fill="x")

stock_entry.drop_target_register(DND_FILES)
stock_entry.dnd_bind('<<Drop>>', on_drop_stock)

csv_label = tk.Label(frame, text="Select CSV File:")
csv_label.pack(fill="x", pady=(10, 0))

csv_entry = tk.Entry(frame, textvariable=csv_file_path)
csv_entry.pack(fill="x", pady=(0, 10))

csv_browse_button = tk.Button(frame, text="Browse", command=browse_csv_file)
csv_browse_button.pack(fill="x")

csv_entry.drop_target_register(DND_FILES)
csv_entry.dnd_bind('<<Drop>>', on_drop_csv)

vin_checkbox = tk.Checkbutton(frame, text="Include VIN", variable=vin_checkbox_var, command=toggle_vin_entry)
vin_checkbox.pack(anchor="w")

vin_entry = tk.Entry(frame, textvariable=vin_value, state=tk.NORMAL if vin_checkbox_var.get() else tk.DISABLED)
vin_entry.pack(fill="x", pady=(0, 10))

copy_data_checkbox = tk.Checkbutton(frame, text="Copy Constant/Global Data", variable=copy_data_checkbox_var)
copy_data_checkbox.pack(anchor="w")

error_label = tk.Label(frame, text="", fg="red")
error_label.pack(fill="x")

proceed_button = tk.Button(frame, text="Proceed", command=proceed_to_next_page)
proceed_button.pack()

def on_closing():
    config = {
        "stock_file_path": stock_file_path.get(),
        "csv_file_path": csv_file_path.get(),
        "vin_checkbox_var": vin_checkbox_var.get(),
        "vin_value": vin_value.get(),  # Save VIN value
        "copy_data_checkbox_var": copy_data_checkbox_var.get()
    }
    save_config(config)
    root.destroy()

root.protocol("WM_DELETE_WINDOW", on_closing)

root.mainloop()

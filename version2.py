import os
import json
import tkinter as tk
from tkinterdnd2 import DND_FILES, TkinterDnD
from tkinter import filedialog
from tkinter import scrolledtext
import requests

def fetch_api_data():
    try:
        response = requests.get('https://jsonplaceholder.typicode.com/posts/1')
        response.raise_for_status()  # Raise an error for bad responses
        return response.json()
    except requests.exceptions.RequestException as e:
        return {'error': str(e)}
def browse_stock_file():
    file_path = filedialog.askopenfilename(filetypes=[("Binary Files", "*.bin *.ori *.hex *.bdc")])
    stock_file_path.set(file_path)

def browse_csv_file():
    file_path = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])
    csv_file_path.set(file_path)

def toggle_vin_entry():
    vin_entry.config(state=tk.NORMAL if vin_checkbox_var.get() else tk.DISABLED)

def toggle_custom_rom_entry():
    custom_rom_entry.config(state=tk.NORMAL if custom_rom_checkbox_var.get() else tk.DISABLED)

def on_drop(event, file_var):
    file_path = event.data
    file_var.set(file_path)

# def on_drop_stock(event):
#     on_drop(event, stock_file_path)
#
# def on_drop_csv(event):
#     on_drop(event, csv_file_path)

def on_drop_stock(event):
    file_path = event.data
    if any(file_path.lower().endswith(ext) for ext in ['.bin', '.ori', '.hex', '.bdc']):
        stock_file_path.set(file_path)
    else:
        print("Invalid stock file format.")

def on_drop_csv(event):
    file_path = event.data
    if file_path.lower().endswith('.csv'):
        csv_file_path.set(file_path)
    else:
        print("Invalid CSV file format.")


def save_config(config):
    with open("config.json", "w") as config_file:
        json.dump(config, config_file)

def load_config():
    if os.path.exists("config.json"):
        with open("config.json", "r") as config_file:
            return json.load(config_file)
    return {}


def proceed_to_next_page():
    if (custom_rom_checkbox_var.get() and len(custom_rom_value.get()) <= 4) or (
            vin_checkbox_var.get() and len(vin_value.get()) != 16):
        error_label.config(text="ROM ID should be more than 4 characters.Vin should be equal to length 16")

    else:
        error_label.config(text="")

        # Create a new window for terminal-like logs
        log_window = tk.Toplevel(root)
        log_window.title("Terminal Logs")
        log_window.geometry("600x600")

        # Create a scrolled text widget to display logs with a black background
        log_text = scrolledtext.ScrolledText(log_window, wrap=tk.WORD, font=("Courier", 12), bg="black", fg="white")
        log_text.pack(fill=tk.BOTH, expand=True)

        def append_log(message, color="white"):
            log_text.tag_configure(color, foreground=color)
            log_text.insert(tk.END, message + "\n", color)
            log_text.see(tk.END)  # Scroll to the end

        # Fetch data from the API
        api_data = fetch_api_data()

        # Log API data
        if 'error' in api_data:
            append_log(f"Error fetching API data: {api_data['error']}", "red")
        else:
            append_log("API Data:")
            for key, value in api_data.items():
                append_log(f"{key}: {value}")

root = TkinterDnD.Tk()
root.title("Next GUI")
root.geometry("500x500")

config = load_config()

stock_file_path = tk.StringVar(value=config.get("stock_file_path", ""))
csv_file_path = tk.StringVar(value=config.get("csv_file_path", ""))
vin_checkbox_var = tk.IntVar(value=config.get("vin_checkbox_var", 0))
vin_value = tk.StringVar(value=config.get("vin_value", ""))
copy_data_checkbox_var = tk.IntVar(value=config.get("copy_data_checkbox_var", 1))
custom_rom_checkbox_var = tk.IntVar(value=config.get("custom_rom_checkbox_var", 0))
custom_rom_value = tk.StringVar(value=config.get("custom_rom_value", ""))
batch_checkbox_var = tk.IntVar(value=config.get("batch_checkbox_var", 0))
has_patched_checkbox_var = tk.IntVar(value=config.get("has_patched_checkbox_var", 0))

frame = tk.Frame(root)
frame.pack(padx=20, pady=20, fill="both", expand=True)

batch_checkbox = tk.Checkbutton(frame, text="Batch Analysis?", variable=batch_checkbox_var)
batch_checkbox.pack(anchor="w")

stock_label = tk.Label(frame, text="Select Stock File:")
stock_label.pack(fill="x", pady=(10, 0))

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

has_patched_checkbox = tk.Checkbutton(frame, text="Has this been patched before?", variable=has_patched_checkbox_var)
has_patched_checkbox.pack(anchor="w")

vin_checkbox = tk.Checkbutton(frame, text="Include VIN", variable=vin_checkbox_var, command=toggle_vin_entry)
vin_checkbox.pack(anchor="w")

vin_entry = tk.Entry(frame, textvariable=vin_value, state=tk.NORMAL if vin_checkbox_var.get() else tk.DISABLED)
vin_entry.pack(fill="x", pady=(0, 10))

custom_rom_checkbox = tk.Checkbutton(frame, text="Custom ROM ID", variable=custom_rom_checkbox_var, command=toggle_custom_rom_entry)
custom_rom_checkbox.pack(anchor="w")

custom_rom_entry = tk.Entry(frame, textvariable=custom_rom_value, state=tk.NORMAL if custom_rom_checkbox_var.get() else tk.DISABLED)
custom_rom_entry.pack(fill="x", pady=(0, 10))

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
        "batch_checkbox_var": batch_checkbox_var.get(),
        "has_patched_checkbox_var": has_patched_checkbox_var.get(),
        "vin_checkbox_var": vin_checkbox_var.get(),
        "vin_value": vin_value.get(),
        "copy_data_checkbox_var": copy_data_checkbox_var.get(),
        "custom_rom_checkbox_var": custom_rom_checkbox_var.get(),
        "custom_rom_value": custom_rom_value.get()
    }
    save_config(config)
    root.destroy()

root.protocol("WM_DELETE_WINDOW", on_closing)

root.mainloop()

# src/pages/advance_page.py
import tkinter as tk
import psutil
from tkinter import ttk

# Function to get battery level
def get_battery_level():
    battery = psutil.sensors_battery()
    return battery.percent

# Function to get battery drainage information
def get_battery_drainage():
    # Placeholder for actual battery drainage logic
    return "Battery is draining at 5% per hour"

# Function to get CPU frequency
def get_cpu_frequency():
    freq = psutil.cpu_freq()
    return f"{freq.current:.2f} MHz"

# Function to get CPU usage
def get_cpu_usage():
    cpu_percent = psutil.cpu_percent(interval=1)
    return f"CPU Usage: {cpu_percent}%"

# Function to get memory usage
def get_memory_usage():
    memory = psutil.virtual_memory()
    return f"Memory Usage: {memory.percent}%"

# Function to get AC connection status
def get_ac_status():
    battery = psutil.sensors_battery()
    return "AC Connected" if battery.power_plugged else "AC Disconnected"

# Function to create the advance page
def open_advance_page():
    advance_window = tk.Toplevel()
    advance_window.title("Advanced Options")

    # Display battery level with a progress bar
    battery_level = get_battery_level()
    battery_progress = ttk.Progressbar(advance_window, orient="horizontal", length=200, mode="determinate")
    battery_progress["value"] = battery_level
    battery_progress.pack(pady=10)
    battery_label = tk.Label(advance_window, text=f"Battery Level: {battery_level}%")
    battery_label.pack()

    # Display AC connection status
    ac_status_label = tk.Label(advance_window, text=get_ac_status())
    ac_status_label.pack()

    # Create a frame to hold the list of information
    info_frame = tk.Frame(advance_window)
    info_frame.pack(pady=10)

    # Battery drainage information
    battery_drainage_icon = tk.Label(info_frame, text="🔋")
    battery_drainage_icon.grid(row=0, column=0, padx=5)
    battery_drainage_label = tk.Label(info_frame, text=get_battery_drainage())
    battery_drainage_label.grid(row=0, column=1, padx=5)

    # CPU frequency information
    cpu_icon = tk.Label(info_frame, text="🖥️")
    cpu_icon.grid(row=1, column=0, padx=5)
    cpu_freq_label = tk.Label(info_frame, text=f"CPU Frequency: {get_cpu_frequency()}")
    cpu_freq_label.grid(row=1, column=1, padx=5)

    # CPU usage information
    cpu_usage_icon = tk.Label(info_frame, text="💻")
    cpu_usage_icon.grid(row=2, column=0, padx=5)
    cpu_usage_label = tk.Label(info_frame, text=get_cpu_usage())
    cpu_usage_label.grid(row=2, column=1, padx=5)

    # Memory usage information
    memory_icon = tk.Label(info_frame, text="🧠")
    memory_icon.grid(row=3, column=0, padx=5)
    memory_label = tk.Label(info_frame, text=get_memory_usage())
    memory_label.grid(row=3, column=1, padx=5)

    # Add more information as needed
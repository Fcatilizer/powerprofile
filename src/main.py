# src/main.py
import tkinter as tk
import psutil
import os
from pages.optimization_page import open_optimization_page
from pages.advance_page import open_advance_page

# Create a Tkinter window
window = tk.Tk()
window.title("System Information")

# Function to draw the battery icon
def draw_battery_icon(percent):
    battery_canvas.delete("all")
    battery_canvas.create_rectangle(10, 10, 110, 50, outline="black", width=2)
    battery_canvas.create_rectangle(110, 20, 120, 40, outline="black", width=2)
    fill_width = int(100 * (percent / 100))
    battery_canvas.create_rectangle(10, 10, 10 + fill_width, 50, fill="green")

# Function to get CPU information
def get_cpu_info():
    cpu_percent = psutil.cpu_percent(interval=1)
    return f"CPU Usage: {cpu_percent}%"

# Function to get GPU information (using nvidia-smi for NVIDIA GPUs)
def get_gpu_info():
    try:
        gpu_info = os.popen("nvidia-smi --query-gpu=utilization.gpu --format=csv,noheader,nounits").read().strip()
        return f"GPU Usage: {gpu_info}%"
    except Exception as e:
        return "GPU Usage: Not Available"

# Function to get memory information
def get_memory_info():
    memory = psutil.virtual_memory()
    return f"Memory Usage: {memory.percent}%"

# Get battery information
battery = psutil.sensors_battery()
plugged = battery.power_plugged
percent = int(battery.percent)  # Ensure percentage is an integer

# Create a canvas to draw the battery icon
battery_canvas = tk.Canvas(window, width=130, height=60)
battery_canvas.pack()
draw_battery_icon(percent)

# Create labels to display battery information
plugged_label = tk.Label(window, text="Plugged in: " + str(plugged))
plugged_label.pack()

percent_label = tk.Label(window, text="Battery percentage: " + str(percent) + "%")
percent_label.pack()

# Create labels to display system information
cpu_label = tk.Label(window, text=get_cpu_info())
cpu_label.pack()

gpu_label = tk.Label(window, text=get_gpu_info())
gpu_label.pack()

memory_label = tk.Label(window, text=get_memory_info())
memory_label.pack()

# Create buttons to open the optimization and advance pages
optimize_button = tk.Button(window, text="Optimize", command=open_optimization_page)
optimize_button.pack(side=tk.LEFT, padx=10)

advance_button = tk.Button(window, text="Advance", command=open_advance_page)
advance_button.pack(side=tk.LEFT, padx=10)

# Function to update system information
def update_info():
    cpu_label.config(text=get_cpu_info())
    gpu_label.config(text=get_gpu_info())
    memory_label.config(text=get_memory_info())
    window.after(1000, update_info)  # Update every second

# Initial call to update system information
update_info()

# Run the Tkinter event loop
window.mainloop()
# src/pages/optimization_page.py
import tkinter as tk
import psutil
import os
import subprocess
from tkinter import simpledialog, messagebox

# Function to get CPU frequency
def get_cpu_frequency():
    freq = psutil.cpu_freq()
    return f"CPU Frequency: {freq.current:.2f} MHz"

# Function to free page cache, dentries, and inodes
def free_page_cache(password):
    return subprocess.run(['echo', password, '|', 'sudo', '-S', 'sh', '-c', 'sync; echo 3 > /proc/sys/vm/drop_caches'], capture_output=True, shell=True)

# Function to kill unnecessary processes
def kill_unnecessary_processes(password):
    return subprocess.run(['echo', password, '|', 'sudo', '-S', 'pkill', '-f', 'browser'], capture_output=True, shell=True)

# Function to clear swap space
def clear_swap_space(password):
    return subprocess.run(['echo', password, '|', 'sudo', '-S', 'swapoff', '-a'], capture_output=True, shell=True) and subprocess.run(['echo', password, '|', 'sudo', '-S', 'swapon', '-a'], capture_output=True, shell=True)

# Function to clean system logs
def clean_system_logs(password):
    return subprocess.run(['echo', password, '|', 'sudo', '-S', 'journalctl', '--vacuum-time=1d'], capture_output=True, shell=True)

# Function to optimize system performance
def optimize_system_performance(password):
    return subprocess.run(['echo', password, '|', 'sudo', '-S', 'sysctl', 'vm.swappiness=10'], capture_output=True, shell=True)

# Function to create the optimization page
def open_optimization_page():
    optimization_window = tk.Toplevel()
    optimization_window.title("Optimization Options")

    # Display CPU frequency
    cpu_freq_label = tk.Label(optimization_window, text=get_cpu_frequency())
    cpu_freq_label.pack()

    # Create checkboxes for each optimization step
    step1_var = tk.BooleanVar()
    step1_checkbox = tk.Checkbutton(optimization_window, text="Free page cache, dentries, and inodes", variable=step1_var)
    step1_checkbox.pack()

    step2_var = tk.BooleanVar()
    step2_checkbox = tk.Checkbutton(optimization_window, text="Kill unnecessary processes", variable=step2_var)
    step2_checkbox.pack()

    step3_var = tk.BooleanVar()
    step3_checkbox = tk.Checkbutton(optimization_window, text="Clear swap space (optional, use with caution)", variable=step3_var)
    step3_checkbox.pack()

    step4_var = tk.BooleanVar()
    step4_checkbox = tk.Checkbutton(optimization_window, text="Clean system logs", variable=step4_var)
    step4_checkbox.pack()

    step5_var = tk.BooleanVar()
    step5_checkbox = tk.Checkbutton(optimization_window, text="Optimize system performance", variable=step5_var)
    step5_checkbox.pack()

    # Function to perform selected optimization steps
    def perform_optimization():
        selected_tasks = []
        if step1_var.get():
            selected_tasks.append(free_page_cache)
        if step2_var.get():
            selected_tasks.append(kill_unnecessary_processes)
        if step3_var.get():
            selected_tasks.append(clear_swap_space)
        if step4_var.get():
            selected_tasks.append(clean_system_logs)
        if step5_var.get():
            selected_tasks.append(optimize_system_performance)

        if not selected_tasks:
            tk.Label(optimization_window, text="No tasks selected!").pack()
            return

        password = simpledialog.askstring("Sudo Password", "Enter your sudo password:", show='*')
        if not password:
            tk.Label(optimization_window, text="Permission denied!").pack()
            return

        for task in selected_tasks:
            result = task(password)
            if result.returncode != 0:
                tk.Label(optimization_window, text="Permission denied!").pack()
                return

        tk.Label(optimization_window, text="Optimization completed!").pack()

    # Create the "Optimize" button
    optimize_button = tk.Button(optimization_window, text="Optimize", command=perform_optimization)
    optimize_button.pack()
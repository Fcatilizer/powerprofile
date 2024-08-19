# main.run
import tkinter as tk
import psutil
import subprocess
from tkinter import ttk, simpledialog

# Function to get battery level
def get_battery_level():
    battery = psutil.sensors_battery()
    return battery.percent

# Function to get battery drainage information
def get_battery_drainage():
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

# Function to create the main application window
def create_main_window():
    window = tk.Tk()
    window.title("System Information and Optimization")

    # Display battery level with a progress bar
    battery_level = get_battery_level()
    battery_progress = ttk.Progressbar(window, orient="horizontal", length=200, mode="determinate")
    battery_progress["value"] = battery_level
    battery_progress.pack(pady=10)
    battery_label = tk.Label(window, text=f"Battery Level: {battery_level}%")
    battery_label.pack()

    # Display AC connection status
    ac_status_label = tk.Label(window, text=get_ac_status())
    ac_status_label.pack()

    # Create a frame to hold the list of information
    info_frame = tk.Frame(window)
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

    # Create checkboxes for each optimization step
    step1_var = tk.BooleanVar()
    step1_checkbox = tk.Checkbutton(window, text="Free page cache, dentries, and inodes", variable=step1_var)
    step1_checkbox.pack()

    step2_var = tk.BooleanVar()
    step2_checkbox = tk.Checkbutton(window, text="Kill unnecessary processes", variable=step2_var)
    step2_checkbox.pack()

    step3_var = tk.BooleanVar()
    step3_checkbox = tk.Checkbutton(window, text="Clear swap space (optional, use with caution)", variable=step3_var)
    step3_checkbox.pack()

    step4_var = tk.BooleanVar()
    step4_checkbox = tk.Checkbutton(window, text="Clean system logs", variable=step4_var)
    step4_checkbox.pack()

    step5_var = tk.BooleanVar()
    step5_checkbox = tk.Checkbutton(window, text="Optimize system performance", variable=step5_var)
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
            tk.Label(window, text="No tasks selected!").pack()
            return

        password = simpledialog.askstring("Sudo Password", "Enter your sudo password:", show='*')
        if not password:
            tk.Label(window, text="Permission denied!").pack()
            return

        for task in selected_tasks:
            result = task(password)
            if result.returncode != 0:
                tk.Label(window, text="Permission denied!").pack()
                return

        tk.Label(window, text="Optimization completed!").pack()

    # Create the "Optimize" button
    optimize_button = tk.Button(window, text="Optimize", command=perform_optimization)
    optimize_button.pack()

    window.mainloop()

# Run the main application
if __name__ == "__main__":
    create_main_window()
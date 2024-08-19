#!/bin/bash

# Function to get battery level
get_battery_level() {
    python3 -c "import psutil; print(psutil.sensors_battery().percent)"
}

# Function to get CPU usage
get_cpu_usage() {
    python3 -c "import psutil; print(psutil.cpu_percent(interval=1))"
}

# Function to get memory usage
get_memory_usage() {
    python3 -c "import psutil; print(psutil.virtual_memory().percent)"
}

# Function to get AC connection status
get_ac_status() {
    python3 -c "import psutil; print('AC Connected' if psutil.sensors_battery().power_plugged else 'AC Disconnected')"
}

# Function to free page cache, dentries, and inodes
free_page_cache() {
    echo $1 | sudo -S sh -c 'sync; echo 3 > /proc/sys/vm/drop_caches'
}

# Function to kill unnecessary processes
kill_unnecessary_processes() {
    echo $1 | sudo -S pkill -f browser
}

# Function to clear swap space
clear_swap_space() {
    echo $1 | sudo -S swapoff -a && echo $1 | sudo -S swapon -a
}

# Function to clean system logs
clean_system_logs() {
    echo $1 | sudo -S journalctl --vacuum-time=1d
}

# Function to optimize system performance
optimize_system_performance() {
    echo $1 | sudo -S sysctl vm.swappiness=10
}

# Display system information
battery_level=$(get_battery_level)
cpu_usage=$(get_cpu_usage)
memory_usage=$(get_memory_usage)
ac_status=$(get_ac_status)

# Ask for sudo password
password=$(kdialog --password "Enter your sudo password")

# Optimization options
options=$(kdialog --checklist "System Information and Optimization\nBattery Level: $battery_level%\nCPU Usage: $cpu_usage%\nMemory Usage: $memory_usage%\n$ac_status" \
    1 "Free page cache, dentries, and inodes" off \
    2 "Kill unnecessary processes" off \
    3 "Clear swap space" off \
    4 "Clean system logs" off \
    5 "Optimize system performance" off)

# Perform selected optimization tasks
IFS=" "
for option in $options; do
    case $option in
        1)
            free_page_cache $password
            ;;
        2)
            kill_unnecessary_processes $password
            ;;
        3)
            clear_swap_space $password
            ;;
        4)
            clean_system_logs $password
            ;;
        5)
            optimize_system_performance $password
            ;;
    esac
done

kdialog --msgbox "Optimization completed!"
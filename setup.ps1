Write-Host "[*] Installing Dependencies...."
pip3 install -r requirements.txt
Write-Host "[*] Success!"
New-Item -Name "log.txt" -ItemType "file"
Write-Host "[*] Finished.. Restart (main.py).."
Write-Host "Installing Dependencies...."
pip3 install mysql-connector-python pandas
Write-Host "Success!"
New-Item -Name "log.txt" -ItemType "file"
Write-Host "Finished.. Restart (main.py).."
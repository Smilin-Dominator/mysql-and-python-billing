Write-Host "Setting Up Conda Environment..."
conda create -y -n mysql-and-python-billing python=3.7.10
Write-Host "Success!"
Write-Host "Installing Dependencies..."
conda install -y -c conda-forge -n mysql-and-python-billing mysql-connector-python
Write-Host "Success!"
New-Item -Path . -Name "log.txt" -ItemType "file"
Write-Host "Setting Up Conda Environment..."
conda create -n mysql-and-python-billing python=3.7.10
Write-Host "Success!"
Write-Host "Activating Conda Environment..."
conda activate mysql-and-python-billing
Write-Host "Success!"
Write-Host "Installing Dependencies..."
conda install -c -y conda-forge mysql-connector-python
Write-Host "Success!"
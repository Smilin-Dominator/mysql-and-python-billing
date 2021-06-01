echo "Setting Up Conda Environment..."
conda create -n mysql-and-python-billing python=3.7.10
echo "Success!"
echo "Activating Conda Environment..."
conda activate mysql-and-python-billing
echo "Success!"
echo "Installing Dependencies..."
conda install -c -y conda-forge mysql-connector-python
echo "Success!"
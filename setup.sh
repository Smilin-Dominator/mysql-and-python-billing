echo "Setting Up Conda Environment..."
conda create -y -n mysql-and-python-billing python=3.9.5
echo "Success!"
echo "Installing Dependencies..."
conda install -y -c conda-forge -n mysql-and-python-billing mysql-connector-python
echo "Success!"
touch log.txt
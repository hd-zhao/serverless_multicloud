
sudo add-apt-repository ppa:deadsnakes/ppa
sudo apt-get update -y
sudo apt-get install python3.9 -y
echo "" >> ~/.bashrc
echo "alias python=python3.9" >> ~/.bashrc
curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
python get-pip.py
echo "export PATH=\${PATH}:~/.local/bin" >> ~/.bashrc
source ~/.bashrc
sudo apt install zip -y
pip install -r requirements.txtp

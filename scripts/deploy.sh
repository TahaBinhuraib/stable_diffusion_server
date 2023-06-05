#!/bin/bash
cd ..
sudo apt update
curl https://raw.githubusercontent.com/GoogleCloudPlatform/compute-gpu-installation/main/linux/install_gpu_driver.py --output install_gpu_driver.py
sudo python3 install_gpu_driver.py
rm install_gpu_driver.py
sudo apt-get -y install libgl1-mesa-glx libegl1-mesa libxrandr2 libxrandr2 libxss1 libxcursor1 libxcomposite1 libasound2 libxi6 libxtst6
wget https://repo.anaconda.com/archive/Anaconda3-2022.05-Linux-x86_64.sh
bash Anaconda3-2022.05-Linux-x86_64.sh -b -u
source ~/anaconda3/bin/activate
conda init bash
rm Anaconda3-2022.05-Linux-x86_64.sh
conda create -n stablediff python=3.10 -y
sudo apt -y install nginx
conda activate stablediff
pip install -r requirements.txt
sudo mv flask_app /etc/nginx/sites-enabled/
sudo unlink /etc/nginx/sites-enabled/default
sudo nginx -t
sudo nginx -s reload
sudo ufw allow 5000
python download_model.py
gunicorn --workers=1 --timeout 120 run:application
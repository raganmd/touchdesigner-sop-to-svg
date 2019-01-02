
#!/bin/bash 

dep=$(dirname "$0")
pythonDir=/python

# change current direcotry to where the script is run from
dirname "$(readlink -f "$0")"

# permission to run the file
sudo chmod 755 udpate-dep-python-mac.sh

# fix up pip with python3
curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
python3 get-pip.py

# Update dependencies

# make sure pip is up to date
python3 -m pip install --upgrade pip

# install requirements
python3 -m pip install -r requirements.txt --target=$dep$pythonDir

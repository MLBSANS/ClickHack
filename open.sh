#!/bin/bash

sudo apt update -y
sudo apt install -y python3 python3-pip python3-venv

if [ ! -d "myver" ]; then
    python3 -m venv myver
fi

source myver/bin/activate
python3 install.py
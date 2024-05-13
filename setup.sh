#!/bin/bash

mp_spdz_version="0.3.8"


echo "Creating virtual environment..."

sudo apt install python3.10-venv
sudo apt install python3-pip

python3 -m venv env >/dev/null
source "env/bin/activate"
echo "Installing dependencies..."
pip install -r requirements.txt >/dev/null

echo "Setup MP-SPDZ..."
git clone https://github.com/data61/MP-SPDZ.git >/dev/null
wget https://github.com/data61/MP-SPDZ/releases/download/v0.3.8/mp-spdz-$mp_spdz_version.tar.xz >/dev/null
tar -xf mp-spdz-$mp_spdz_version.tar.xz >/dev/null
mv "mp-spdz-$mp_spdz_version/bin/Linux-a*" "MP-SPDZ/bin/"
rm -rf mp-spdz-$mp_spdz_version.tar.xz
rm -rf mp-spdz-$mp_spdz_version
python3 "$(pwd)/MP-SPDZ/setup.py" "install" >/dev/null

cd MP-SPDZ
sudo apt install automake build-essential clang cmake git libboost-dev libboost-thread-dev libgmp-dev libntl-dev libsodium-dev libssl-dev libtool python3 libboost-filesystem-dev libboost-iostreams-dev
make replicated-bin-party.x
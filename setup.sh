#!/bin/bash

mp_spdz_version="0.3.8"


echo "Creating virtual environment..."
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
cd MP-SPDZ
python3 "$(pwd)/MP-SPDZ/setup.py" "install" >/dev/null
make replicated-bin-party.x
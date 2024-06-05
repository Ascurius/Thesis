#!/bin/bash

mp_spdz_version="0.3.8"


if [[ ! -d "./env" ]]; then
    echo "Creating virtual environment..."
    python3 -m venv env >/dev/null
fi

source "env/bin/activate"
echo "Installing dependencies..."
pip install -r requirements.txt >/dev/null

echo "Setup MP-SPDZ..."

if [[ -d "./MP-SPDZ" ]]; then
    rm -rf "./MP-SPDZ"
fi

git clone git@github.com:Ascurius/MP-SPDZ.git >/dev/null
wget https://github.com/data61/MP-SPDZ/releases/download/v0.3.8/mp-spdz-$mp_spdz_version.tar.xz >/dev/null
tar -xf mp-spdz-$mp_spdz_version.tar.xz >/dev/null
mv "mp-spdz-$mp_spdz_version/bin/Linux-a"/* "MP-SPDZ/bin/"
rm -rf mp-spdz-$mp_spdz_version.tar.xz
rm -rf mp-spdz-$mp_spdz_version

cd MP-SPDZ
python3 "./setup.py" "install" >/dev/null
./Scripts/setup-ssl.sh
./Scripts/tldr.sh
make replicated-bin-party.x
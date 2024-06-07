#!/bin/bash

# Function to determine the Linux distribution
detect_distro() {
  if [ -f /etc/os-release ]; then
    . /etc/os-release
    DISTRO=$ID
  elif [ -f /etc/redhat-release ]; then
    DISTRO="rhel"
  else
    DISTRO=$(uname -s)
  fi
}

# Detect the distribution
detect_distro

# Install packages based on the detected distribution
case "$DISTRO" in
  ubuntu|debian)
    sudo apt update
    sudo apt install -y python3.10-venv python3-pip automake build-essential clang cmake git libboost-dev libboost-thread-dev libgmp-dev libntl-dev libsodium-dev libssl-dev libtool python3 libboost-filesystem-dev libboost-iostreams-dev
    ;;
  fedora|rhel|centos)
    sudo dnf install -y python3.10-venv python3-pip automake gcc clang cmake git boost-devel gmp-devel ntl-devel libsodium-devel openssl-devel libtool python3 boost-filesystem boost-iostreams
    ;;
  *)
    echo "Unsupported distribution: $DISTRO"
    exit 1
    ;;
esac

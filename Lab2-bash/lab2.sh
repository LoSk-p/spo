#!/bin/bash
wget "https://dl.google.com/go/go1.13.1.linux-amd64.tar.gz"
sudo tar -C /usr/local -xzf go1.13.1.linux-amd64.tar.gz
export GOPATH=~/go
export PATH=$PATH:/usr/local/go/bin
export PATH=$PATH:$GOPATH/bin
source $HOME/.profile
sudo apt install git
git clone https://github.com/yggdrasil-network/yggdrasil-go.git
cd yggdrasil-go
./build


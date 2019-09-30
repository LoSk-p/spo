#!/bin/bash
wget "https://dl.google.com/go/go1.13.1.linux-amd64.tar.gz"
tar -C /usr/local -xzf go1.13.1.linux-amd64.tar.gz
export PATH=$PATH:/usr/local/go/bin
source $HOME/.profile
git clone https://github.com/yggdrasil-network/yggdrasil-go.git
cd yggdrasil-go
./build


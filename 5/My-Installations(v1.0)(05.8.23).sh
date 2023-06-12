#!/bin/bash

termux-setup-storage
apt update -y
apt upgrade -y
apt update -y
apt install -y cloudflared openssh wget git tmux apache2
git clone https://github.com/jaykali/maskphish
cd maskphish
wget -O install-nethunter-termux https://offs.ec/2MceZWr
chmod +x install-nethunter-termux
./install-nethunter-termux &
echo -e "1\n" | ./install-nethunter-termux || true
tmux send-keys '1' C-m

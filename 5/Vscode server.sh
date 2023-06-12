#!/bin/bash
# -*- coding: utf-8 -*- 

# Change to parrot-in-termux directory and start Parrot OS
cd ~/parrot-in-termux
./startparrot.sh &
cd ~/code-server-4.12.0-linux-arm64/bin

# Start code-server in a new tmux pane
tmux new-session -d -s code
tmux split-window -h "export PASSWORD='50031533' && ~/code-server-4.12.0-linux-arm64/bin/code-server" 

# Select pane 1 and connect to the Parrot OS terminal
tmux select-pane -t 1
tmux send-keys 'cd ~/parrot-in-termux' C-m
tmux send-keys './startparrot.sh' C-m 

# Send export PASSWORD command and start code-server in pane 2
tmux select-pane -t 2
tmux send-keys 'export PASSWORD='50031533' ' C-m 
tmux send-keys '~/code-server-4.12.0-linux-arm64/bin/code-server' C-m 

# Split the second pane vertically and execute cloudflared tunnel command
tmux split-window -v
tmux send-keys 'cloudflared tunnel -url http://127.0.0.1:8080/' C-m 

# Split the first pane vertically and execute maskphish
tmux select-pane -t 1
tmux split-window -v
tmux send-keys 'cd && cd maskphish' C-m
tmux send-keys 'bash maskphish.sh' C-m 

# Attach to the tmux session
tmux select-pane -t 1
tmux attach -t code
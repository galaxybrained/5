#!/bin/bash

log_file="script.log"
{
    apt update
    apt upgrade -y
    apt install -y cloudflared openssh wget git tmux apache2 curl proot proot-distro expect

    termux-setup-storage <<< "y"

    if [ -d ~/maskphish ]; then
        echo "Maskphish already exists. Skipping installation..."
    else
        echo "Maskphish not installed. Installing..."
        git clone https://github.com/jaykali/maskphish
    fi

    if [ -f ~/install-nethunter-termux ]; then
        echo "install-nethunter-termux already exists. Skipping installation..."
    else
        echo "Installing install-nethunter-termux..."
        wget -O install-nethunter-termux https://gitlab.com/kalilinux/nethunter/build-scripts/kali-nethunter-project/raw/master/nethunter-rootless/install-nethunter-termux
        chmod +x install-nethunter-termux
    fi

    if [ -d ~/parrot-in-termux ]; then
        echo "Directory parrot-in-termux already exists. Skipping installation..."
    else
        echo "Installing parrot-in-termux..."
        git clone https://github.com/RiSecID/parrot-in-termux.git
        if ! grep -q 'alias parrot="cd ~/parrot-in-termux && ./startparrot.sh"' /data/data/com.termux/files/usr/etc/bash.bashrc; then
            echo 'alias parrot="cd ~/parrot-in-termux && ./startparrot.sh"' >> /data/data/com.termux/files/usr/etc/bash.bashrc
            source /data/data/com.termux/files/usr/etc/bash.bashrc
        else
                echo "Alias 'parrot' already exists in bash.bashrc. Skipping..."
        fi

    fi

    latest_version="4.13.0"
    old_version="4.12.0"
    directory="code-server-$old_version-linux-arm64"

    if [ -d ~/code-server-"$latest_version-linux-arm64" ]; then
        echo "Latest version of code-server ($latest_version) is already installed. Exiting"
        exit 0
    fi
    if [ ! -d "~/code-server-$old_version-linux-arm64" ] || [ ! -d "~/code-server-$latest_version-linux-arm64" ]; then
        echo "Latest version of code-server found: $latest_version"
        echo "Downloading $latest_version..."
        wget "https://github.com/coder/code-server/releases/download/v$latest_version/code-server-$latest_version-linux-arm64.tar.gz"
        tar -xvf "code-server-$latest_version-linux-arm64.tar.gz"
        rm "code-server-$latest_version-linux-arm64.tar.gz"
    fi

    if [ -d ~/code-server-"$old_version-linux-arm64" ] || [ "$old_version" != "$latest_version" ]; then
        echo "Latest version of code-server found: $latest_version"
        echo "Deleting old version ($old_version)..."
        rm -rf "$directory"
        echo "Downloading $latest_version..."
        wget "https://github.com/coder/code-server/releases/download/v$latest_version/code-server-$latest_version-linux-arm64.tar.gz"
        tar -xvf "code-server-$latest_version-linux-arm64.tar.gz"
        rm "code-server-$latest_version-linux-arm64.tar.gz"
    fi

} |& tee "$log_file"
(sleep 600 && rm "$log_file") &
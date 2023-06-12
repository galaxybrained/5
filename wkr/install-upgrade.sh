#!/bin/bash

log_file="script.log"

{
    apt update
    apt upgrade -y
    apt install -y cloudflared openssh wget git tmux apache2 curl proot proot-distro expect

    termux-setup-storage <<< "y"

    if [ -d "$HOME/maskphish" ]; then
        echo "Maskphish already exists. Skipping installation..."
    else
        echo "Maskphish not installed. Installing..."
        git clone https://github.com/jaykali/maskphish "$HOME/maskphish"
    fi

    if [ -f "$HOME/install-nethunter-termux" ]; then
        echo "install-nethunter-termux already exists. Skipping installation..."
    else
        echo "Installing install-nethunter-termux..."
        wget -O "$HOME/install-nethunter-termux" https://gitlab.com/kalilinux/nethunter/build-scripts/kali-nethunter-project/raw/master/nethunter-rootless/install-nethunter-termux
        chmod +x "$HOME/install-nethunter-termux"
    fi

    if [ -d "$HOME/parrot-in-termux" ]; then
        echo "Directory parrot-in-termux already exists. Skipping installation..."
    else
        echo "Installing parrot-in-termux..."
        git clone https://github.com/RiSecID/parrot-in-termux.git "$HOME/parrot-in-termux"
        if ! grep -q 'alias parrot="cd $HOME/parrot-in-termux && ./startparrot.sh"' /data/data/com.termux/files/usr/etc/bash.bashrc; then
            echo 'alias parrot="cd $HOME/parrot-in-termux && ./startparrot.sh"' >> /data/data/com.termux/files/usr/etc/bash.bashrc
            source /data/data/com.termux/files/usr/etc/bash.bashrc
        else
            echo "Alias 'parrot' already exists in bash.bashrc. Skipping..."
        fi
    fi

    response=$(curl -s "https://api.github.com/repositories/172953845/releases/latest")

    # Extract the latest version from the API response using jq and remove the leading 'v'
    latest_version=$(echo "$response" | jq -r '.tag_name' | sed 's/^v//')

    # Check if the latest version is empty or not
    if [ -z "$latest_version" ]; then
        echo "Failed to retrieve the latest version. Exiting."
        exit 1
    fi

    directory_pattern="code-server-*-linux-arm64"
    directories=("$HOME"/$directory_pattern)
    old_version=""

    # Find the existing version by checking directories with a matching pattern
    for dir in "${directories[@]}"; do
        if [ -d "$dir" ]; then
            old_version=$(echo "$dir" | sed "s|$HOME/$directory_pattern|code-server-|")
            break
        fi
    done

    if [ -d "code-server-$latest_version-linux-arm64" ]; then
        echo "Latest version of code-server ($latest_version) is already installed. Exiting."
        exit 0
    fi

    if [ -z "$old_version" ] || [ "$old_version" != "$latest_version" ]; then
        echo "Latest version of code-server found: $latest_version"
        if [ -n "$old_version" ]; then
            echo "Deleting old version ($old_version)..."
            rm -rf "$HOME/$old_version-linux-arm64"
        fi
        echo "Downloading $latest_version..."
        wget "https://github.com/coder/code-server/releases/download/v$latest_version/code-server-$latest_version-linux-arm64.tar.gz"
        tar -xvf "code-server-$latest_version-linux-arm64.tar.gz"
        rm "code-server-$latest_version-linux-arm64.tar.gz"
    fi
} |& tee "$log_file"

(sleep 600 && rm "$log_file") &

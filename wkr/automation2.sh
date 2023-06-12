#!/bin/bash

response=$(curl -s "https://api.github.com/repositories/172953845/releases/latest")

# Extract the latest version from the API response using jq and remove the leading 'v'
latest_version=$(echo "$response" | jq -r '.tag_name' | sed 's/^v//')

# Check if the latest version is empty or not
if [ -z "$latest_version" ]; then
    echo "Failed to retrieve the latest version. Exiting."
    exit 1
fi

directory_pattern="code-server-*-linux-arm64"
directories=($HOME/$directory_pattern)
old_version=""

# Find the existing version by checking directories with a matching pattern
for dir in "${directories[@]}"; do
    if [ -d "$dir" ]; then
        old_version=$(echo "$dir" | sed "s|$HOME/$directory_pattern|code-server-|")
        break
    fi
done

if [ -d "$HOME/code-server-$latest_version-linux-arm64" ]; then
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

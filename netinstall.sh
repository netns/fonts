#!/usr/bin/env bash

set -e

VERSION="v1.0.0"
URL="https://github.com/netns/fonts/archive/refs/tags/${VERSION}.tar.gz"


RED='\033[0;31m'
GREEN='\033[0;32m'
NC='\033[0m'

log() { echo -e "[*] $1"; }
slog() { echo -e "${GREEN}[+]${NC} $1"; }
elog() { echo -e "${RED}[-]${NC} $1" >&2; exit 1; }

download()
{
    log "Downloading $1 -> $2"

    if [ "$(command -v curl)" ]; then
        curl -fsSL "$1" -o "$2"
    elif [ "$(command -v wget)" ]; then
        wget -qO "$2" "$1"
    else
        elog "curl and wget are required but not found."
    fi
}

install()
{
    tmp_dir=$(mktemp -d)
    file_name="fonts.tar.gz"
    dest="${tmp_dir}/${file_name}"
    install_script="${tmp_dir}/install.sh"
    python_install_script="${tmp_dir}/install.py"

    slog "Using temporary directory: $tmp_dir"

    download "$URL" "$dest"

    slog "Extracting archive..."
    tar -xzf "$dest" -C "$tmp_dir" --strip-components=1 || elog "Failed to extract $dest."
    
    if [ -f "$install_script" ]; then
        slog "Running bash installer in local mode..."
        bash "$install_script" --local || elog "Installer failed."
    elif [ -f "$python_install_script" ]; then
        slog "Running python installer in local mode..."
        python3 "$python_install_script" --local || elog "Installer failed."
    else
        elog "Installation script not found."
    fi
    
    slog "Fonts installed successfully!"
}

install

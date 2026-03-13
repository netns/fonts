#!/usr/bin/env bash

set -e

VERSION="v1.0.0"
URL="https://github.com/netns/fonts/archive/refs/tags/${VERSION}.tar.gz"

RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m'

LOCAL_DEST="$HOME/.local/share/fonts"

log() { echo -e "${BLUE}[*]${NC} $1"; }
slog() { echo -e "${GREEN}[+]${NC} $1"; }
elog() { echo -e "${RED}[-]${NC} $1" >&2 ; exit 1; }

# $1 -> url
# $2 -> dest file
get_fonts()
{
    log "Downloading fonts: $1 -> $2"

    if [ "$(command -v curl)" ]; then
        curl -fsSL "$1" -o "$2"
    elif [ "$(command -v wget)" ]; then
        wget -qO "$2" "$1"
    else
        elog "Neither curl nor wget was found. One of them is required to download the fonts"
    fi
}

# $1 -> fonts path
install_fonts_local() {
    log "Installing fonts to $LOCAL_DEST"

    [[ -d "$LOCAL_DEST" ]] || mkdir -p "$LOCAL_DEST"

    [ -d "$1" ] || elog "fonts directory not found in archive"
    
    if mv "$1"/* "$LOCAL_DEST/" && chmod 644 "$LOCAL_DEST"/* ; then
        slog "Fonts installed successfully"
    else
        elog "Failed to move font files to $LOCAL_DEST"
    fi
}

load_fonts() {
    log "Refreshing font cache"

    [ "$(command -v fc-cache)" ] || elog "fc-cache command not found on this system"

    if fc-cache -fv >/dev/null ; then
        slog "Font cache updated successfully"
    else
        elog "Failed to refresh font cache"
    fi
}

run()
{
    if [ -d "./fonts" ]; then
        log "Using local fonts directory"
        fonts_dir="./fonts"
    else
        tmp_dir=$(mktemp -d)
        file_name="fonts.tar.gz"
        dest="${tmp_dir}/${file_name}"

        log "Using temporary directory: $tmp_dir"

        get_fonts "$URL" "$dest"

        log "Extracting fonts archive..."
        tar -xzf "$dest" -C "$tmp_dir" --strip-components=1 || elog "Failed to extract $dest"

        fonts_dir="$tmp_dir/fonts"
    fi

    install_fonts_local "$fonts_dir"
    load_fonts

    slog "Font installation completed successfully"
}

run

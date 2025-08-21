#!/usr/bin/env python3
# Licensed under the MIT License.
# See LICENSE file in the project root for details.

import os
import shutil
import subprocess
import sys
from getopt import GetoptError, getopt
from pathlib import Path

RED = "\033[0;31m"
GREEN = "\033[0;32m"
BLUE = "\033[0;34m"
NC = "\033[0m"

LOCAL_DEST = Path("~/.local/share/fonts").expanduser()
GLOBAL_DEST = Path("/usr/local/share/fonts")
FONTS_SRC = Path("./fonts")

FONTS_EXT = {".ttf", ".woff2", ".woff"}


USAGE = """
Usage:
    python3 install.py [options]

Options:
    -l, --local         Install fonts locally (default: {LOCAL_DEST})
    -g, --global:       Install fonts globally (requires sudo, default: {GLOBAL_DEST})
    -f <path>, --font=<path> 
                        Provide the source directory containing font files 
                        (default: {FONTS_SRC.resolve()})
    -h, --help          Show this help message and exit

Examples:
    python3 install.py --local
    sudo python3 install.py --global --font=/path/to/fonts
"""


def log(msg, color=NC, prefix="[*]"):
    print(f"{color}{prefix}{NC} {msg}")


def elog(msg):
    log(msg, RED, "[-]")
    sys.exit(1)


def slog(msg):
    log(msg, GREEN, "[+]")


def install_fonts(src: Path, dest: Path):
    log(f"Moving fonts to {BLUE}{dest}{NC}", BLUE)
    try:
        dest.mkdir(parents=True, exist_ok=True)

        moved_fonts = 0
        for font in src.iterdir():
            if font.is_file() and font.suffix.lower() in FONTS_EXT:
                target = dest / font.name
                if target.exists():
                    log(f"Skipping existing font: {BLUE}{font.name}{NC}", BLUE)
                    continue
                shutil.move(font, target)
                target.chmod(0o644)
                moved_fonts += 1

        slog(f"Moved {moved_fonts} fonts successfully")

    except Exception as e:
        elog(f"Error moving fonts: {e}")


def update_font_cache(dest: Path):
    log("Updating font cache...", BLUE)

    if shutil.which("fc-cache") is None:
        elog(
            f"The {BLUE}'fc-cache'{NC} command was not found. "
            "Please install Fontconfig."
        )

    try:
        subprocess.run(
            ["fc-cache", "-f", "-v", str(dest)],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            check=True,
        )
        slog("Font cache updated successfully")
    except subprocess.CalledProcessError as e:
        elog(f"Failed to update font cache: {e}")


def cli(argv=None):
    if argv is None:
        argv = sys.argv[1:]

    args = {"local": True, "font_src": None}

    try:
        opts, _ = getopt(argv, "hf:gl", ["help", "font=", "global", "local"])
    except GetoptError as err:
        print(err)
        print(USAGE)
        sys.exit(2)

    for opt, val in opts:  # type: ignore
        if opt in ("-h", "--help"):
            print(USAGE)
            sys.exit(0)
        elif opt in ("-f", "--font"):
            args["font_src"] = Path(val)
        elif opt in ("-g", "--global"):
            args["local"] = False
        elif opt in ("-l", "--local"):
            args["local"] = True
        else:
            elog(f"Unknown argument: {BLUE}{opt}{NC}")

    return args


def validate_font_src_path(path: Path):
    if not path.exists():
        elog(f"Path does not exist: {BLUE}{path}{NC}")

    if not path.is_dir():
        elog(f"Path is not a directory: {BLUE}{path}{NC}")


def main():
    args = cli()
    dest = LOCAL_DEST if args["local"] else GLOBAL_DEST
    src = FONTS_SRC if args["font_src"] is None else args["font_src"]

    src = src.expanduser().resolve()

    validate_font_src_path(src)

    if dest == GLOBAL_DEST and os.geteuid() != 0:
        elog(
            f"Insufficient permissions to write to {BLUE}{dest}{NC}. "
            "Please run the command as root or use 'sudo'."
        )

    install_fonts(src, dest)
    update_font_cache(dest)

    slog("Fonts installed successfully!")


if __name__ == "__main__":
    main()

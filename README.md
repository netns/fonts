# Fonts

A handy collection of popular open-source fonts, all in one place. Comes with an easy-to-use install script to get everything set up on your system in no time.

## Included Fonts

- **FiraCode**  
- **JetBrains Mono**  
- **Noto Sans**  
- **Roboto**

All fonts are distributed under their respective open source licenses. See [FONTS_LICENSE.md](./FONTS_LICENSE.md) for detailed license information and official links.

## Installation

> [!WARNING]
> You must have Fontconfig (`fc-cache`) and either curl or wget installed on your system..

### Quick Install (recommended)

Run the network installer directly:

```bash
curl -fsSL https://raw.githubusercontent.com/netns/fonts/master/install.sh | bash
```

This will automatically download the latest release archive and install the fonts locally.

### Install from Repository

1. Clone this repository:

```bash
git clone --depth=1 https://github.com/netns/fonts.git
cd fonts
```

1. Run the installation script:

```bash
bash install.sh
```

When executed from inside the repository, the installer will use the local fonts directory instead of downloading the release archive.

### Installation Location

Fonts are installed to:

`~/.local/share/fonts`

After installation, the script automatically refreshes the font cache using `fc-cache`.

> [!TIP]
> You can check available fonts after installation by running `fc-list`.

## License

- The installation scripts and any code in this repository are licensed under the MIT License. See the [LICENSE](./LICENSE) file for details.

- The fonts themselves retain their original licenses. Please refer to [FONTS_LICENSE.md](./FONTS_LICENSE.md) for full license details

## Contribution

Contributions are welcome! Feel free to open issues or submit pull requests to improve font selection, installation scripts, or documentation.

## Disclaimer

This repository respects the licensing terms of all included fonts. Redistribution is done in compliance with each font’s license. The author is not responsible for any issues arising from font installation or usage.

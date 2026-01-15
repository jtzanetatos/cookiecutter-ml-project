#!/bin/bash
set -e

# platform detection
OS="$(uname -s)"
ARCH="$(uname -m)"

echo "Detected OS: $OS"
echo "Detected Arch: $ARCH"

install_macos() {
    echo "Checking for Homebrew..."
    if ! command -v brew &> /dev/null; then
        echo "Homebrew not found."
        read -p "Do you want to install Homebrew? (y/N) " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            echo "Installing Homebrew..."
            /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
            
            # Add brew to path for this session if it was just installed
            if [[ -x /opt/homebrew/bin/brew ]]; then
                 eval "$(/opt/homebrew/bin/brew shellenv)"
            elif [[ -x /usr/local/bin/brew ]]; then
                 eval "$(/usr/local/bin/brew shellenv)"
            fi
        else
            echo "Aborting installation. Homebrew is required for this script on macOS."
            exit 1
        fi
    else
        echo "Homebrew is installed."
    fi

    echo "Installing just..."
    brew install just
}

install_linux() {
    echo "Installing just via prebuilt binary..."
    # Using official install script from just.systems
    curl --proto '=https' --tlsv1.2 -sSf https://just.systems/install.sh | bash -s -- --to ~/bin
    
    # Check if ~/bin is in PATH
    if [[ ":$PATH:" != *":$HOME/bin:"* ]]; then
        echo "WARNING: ~/bin is not in your PATH."
        echo "Please add it to run 'just' or move the binary to a location in your PATH."
    fi
}

if [[ "$OS" == "Darwin" ]]; then
    install_macos
elif [[ "$OS" == "Linux" ]]; then
    install_linux
else
    echo "Unsupported operating system: $OS"
    exit 1
fi

echo "just installed successfully!"
if command -v just &> /dev/null; then
    just --version
else
    echo "Verifying installation..."
    ~/bin/just --version 2>/dev/null || echo "Could not find 'just' in PATH or ~/bin"
fi

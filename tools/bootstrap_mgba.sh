#!/usr/bin/env bash
set -euo pipefail

MGBA_VERSION="${MGBA_VERSION:-0.10.5}"
INSTALL_ROOT="${MGBA_INSTALL_ROOT:-$HOME/.local/share/mgba-portable}"
BIN_DIR="${MGBA_BIN_DIR:-$HOME/.local/bin}"

if command -v mgba >/dev/null 2>&1; then
    echo "mGBA already available: $(command -v mgba)"
    mgba --version 2>/dev/null || true
    exit 0
fi

case "$(uname -m)" in
    x86_64|amd64)
        ASSET="mGBA-${MGBA_VERSION}-appimage-x64.appimage"
        ;;
    aarch64|arm64)
        ASSET="mGBA-${MGBA_VERSION}-appimage-arm64.appimage"
        ;;
    *)
        echo "Unsupported architecture: $(uname -m)" >&2
        exit 2
        ;;
esac

URL="https://github.com/mgba-emu/mgba/releases/download/${MGBA_VERSION}/${ASSET}"
APPIMAGE="${INSTALL_ROOT}/${ASSET}"

mkdir -p "$INSTALL_ROOT" "$BIN_DIR"

if [[ ! -s "$APPIMAGE" ]]; then
    tmp="${APPIMAGE}.part"
    rm -f "$tmp"
    echo "Downloading mGBA ${MGBA_VERSION}: $URL"
    if command -v curl >/dev/null 2>&1; then
        curl -fL --retry 3 --connect-timeout 15 -o "$tmp" "$URL"
    elif command -v wget >/dev/null 2>&1; then
        wget -O "$tmp" "$URL"
    else
        echo "Neither curl nor wget is available." >&2
        exit 3
    fi
    mv "$tmp" "$APPIMAGE"
fi

chmod +x "$APPIMAGE"
ln -sfn "$APPIMAGE" "$BIN_DIR/mgba"

echo "Installed portable mGBA ${MGBA_VERSION}: $APPIMAGE"
echo "Launcher: $BIN_DIR/mgba"
if [[ ":$PATH:" != *":$BIN_DIR:"* ]]; then
    echo "Add this to PATH for the current shell:"
    echo "  export PATH=\"$BIN_DIR:\$PATH\""
fi

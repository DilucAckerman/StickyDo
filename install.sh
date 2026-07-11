#!/usr/bin/env bash
# StickyDo installer — sets up the venv, installs the icon and .desktop entry.
set -e

PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "==> Checking dependencies..."
for pkg in python-gobject gtk4; do
    if ! pacman -Qi "$pkg" &>/dev/null; then
        echo "Missing dependency: $pkg"
        echo "Install with: sudo pacman -S $pkg"
        exit 1
    fi
done

if ! pacman -Qi gtk4-layer-shell &>/dev/null; then
    echo "Missing dependency: gtk4-layer-shell (AUR)"
    echo "Install with: yay -S gtk4-layer-shell"
    exit 1
fi

echo "==> Setting up Python virtual environment..."
if [ ! -d "$PROJECT_DIR/venv" ]; then
    python3 -m venv "$PROJECT_DIR/venv" --system-site-packages
fi
source "$PROJECT_DIR/venv/bin/activate"

echo "==> Installing icon..."
mkdir -p ~/.local/share/icons/hicolor/scalable/apps
if [ -f "$PROJECT_DIR/stickydo/assets/icons/stickydo.svg" ]; then
    cp "$PROJECT_DIR/stickydo/assets/icons/stickydo.svg" ~/.local/share/icons/hicolor/scalable/apps/stickydo.svg
    gtk-update-icon-cache -f -t ~/.local/share/icons/hicolor &>/dev/null || true
fi

echo "==> Installing .desktop entry..."
mkdir -p ~/.local/share/applications
sed "s|__PROJECT_DIR__|$PROJECT_DIR|g" "$PROJECT_DIR/stickydo.desktop.template" > ~/.local/share/applications/com.stickydo.app.desktop
update-desktop-database ~/.local/share/applications &>/dev/null || true

chmod +x "$PROJECT_DIR/run.sh"

echo ""
echo "==> Done!"
echo "Run manually with: $PROJECT_DIR/run.sh"
echo ""
echo "For background blur (optional), see the README's 'Background Blur' section"
echo "and add the rules from hyprland/stickydo-layerrules.conf to your Hyprland config."
echo ""
echo "For autostart, add this line to your Hyprland config:"
echo "  exec-once = $PROJECT_DIR/run.sh"

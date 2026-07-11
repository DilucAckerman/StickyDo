# Maintainer: Dhruv <dhruvest@gmail.com>
pkgname=stickydo
pkgver=1.0.0
pkgrel=1
pkgdesc="A native sticky notes + to-do list panel for Wayland, built with GTK4 and layer-shell"
arch=('any')
url="https://github.com/DilucAckerman/StickyDo"
license=('MIT')
depends=('python' 'python-gobject' 'gtk4' 'gtk4-layer-shell' 'sqlite')
source=("$pkgname-$pkgver.tar.gz::https://github.com/DilucAckerman/StickyDo/archive/refs/heads/main.tar.gz")
sha256sums=('SKIP')

package() {
    cd "$srcdir/StickyDo-main"

    install -dm755 "$pkgdir/opt/$pkgname"
    cp -r stickydo "$pkgdir/opt/$pkgname/"
    cp run.sh "$pkgdir/opt/$pkgname/"

    install -Dm644 stickydo/assets/icons/stickydo.svg \
        "$pkgdir/usr/share/icons/hicolor/scalable/apps/stickydo.svg"

    install -Dm644 /dev/stdin "$pkgdir/usr/share/applications/com.stickydo.app.desktop" <<EOF
[Desktop Entry]
Type=Application
Name=StickyDo
Comment=Sticky notes and to-do list panel for Wayland
Exec=/opt/$pkgname/run.sh
Icon=stickydo
Terminal=false
Categories=Utility;
StartupWMClass=com.stickydo.app
EOF

    install -Dm644 hyprland/stickydo-layerrules.conf \
        "$pkgdir/usr/share/doc/$pkgname/stickydo-layerrules.conf"
}

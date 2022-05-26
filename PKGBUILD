 
# Maintainer: Alvin Zhu <alvin.zhuge@gmail.com>
pkgname=python-nuc-rgb
pkgver=1.0.0
pkgrel=1
pkgdesc="NUC RGB"
arch=('any')
url="https://github.com/AlvinZhu/nuc_rgb"
license=('GPL')
groups=('aur-alvin')
depends=('python' 'python-pyserial')

package() {
  install -Dm755 ../nuc_rgb.py "$pkgdir"/usr/bin/nuc_rgb
}
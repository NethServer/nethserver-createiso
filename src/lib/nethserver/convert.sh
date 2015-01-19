#/bin/bash
convert  -depth 16 -colors 65536 splash.png syslinux-vesa-splash.png
mv syslinux-vesa-splash.png splash.jpg
convert splash.jpg  -colors 14 -depth 8 splash.xpm
gzip splash.xpm

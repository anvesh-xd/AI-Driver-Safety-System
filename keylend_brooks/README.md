Keylend Brooks Folder for GPS-Module
Requires serial and pynmea2 libraries
Parses NMEA data to get information about speed and location
Connects to raspberry pi 5 by enabling UART0 for GPIO 14/15
Enable UART by doing the following:
In config.txt:
[all]
dtparam=uart0=on

In cmdline.txt:
console=tty1 root=PARTUUID=d8436486-02 rootfstype=ext4 fsck.repair=yes rootwait>

Confirm using: [install minicom library for testing]
Sudo minicom -b 9600 -D /dev/ttyAMA0
Pinctrl get 14
Pinctrl get 15




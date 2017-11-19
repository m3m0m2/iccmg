# iccmg
Input Console Control for Media and Gaming


I'm using this project running on my raspberry pi connected to my living room television like in this photo

![TV + Raspberry Pi setup](https://photos.app.goo.gl/rQHScWOWj0nkXMz22)

This project cannot be simply run blindfolded because requires some custom setup that currently need to be done manually, but I may add a proper installation menu in the future.

Custom setup on my system
Hardware
- using flirc for remote control, using custom key map (that depends on remote device)
- using HD Star v3 satellite decoder http://www.ebay.co.uk/itm/HDStar-DVB-S2-TV-Box-USB-Satellite-Receiver-for-Windows-Linux-FREESAT-HOTBIRD-/322382413057
- foot switch
- custom wooden mount

Software
- depends on media kernel modules from crasycat to detect the HD Star decoder https://bitbucket.org/CrazyCat/media_build
- requires device firmware file
- using mplayer, omxplayer, fbi as external tools
- using python modules as evdev


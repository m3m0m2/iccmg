# iccmg
Input Console Control for Media and Gaming


I'm using this project running on my raspberry pi connected to my living room television like in this photo

![Raspberry Pi setup](https://lh3.googleusercontent.com/IzfUQebeYwLxRkAuAiHMvlQDEBb5nprgtZDNy8sC9UKNwFUIWNwjz-KKkF_yXXHBzZ1C64PmUotM1Yo6Skl4r7iFGZLTnmSop2Sggvkws-wxMAO5rWHXCksGbVu1W1VFhI9Kvbf4eD75MSBw65KrzWB4xat_hBJaYqEDaTtsZLJOViHGpxuey2xYtnTcrM9FSuWhklO61kVTYomhEt6_KMLnqMRSgy_yoBuYCa_Qzos9MjAu4oBC1Lc4zKZnjKYwMqaettiDCyjvzMpjJxH-900aa5WjnTFw-PBKeG6F_477rEdtcpXQ3gsxqeAjpLYqw-N7clwtj5Uasx3e8_P50YNqLoqUdHmKGW_yo8raEdc839R9Gqlx5NHV2gdi1xH86AtlYK_W46DHh2hGG4LsMKqP2Xeuf_NjjN3ojl8R0GUvS6Fn5IWrZ_kX9ANlgVHDsZsVWUIcI2X6rMkHOujofvHjiKDhggbnMD7xRjH2dcEeUahbRiTJ35h04aRM-Q04doIRi0N2oM29m2ah-azr7Y1v2t21Fe5igdm3yIyFavK_9gD2E9pPj3rlJKwO4Yxqdy3jQ-GxlnQ1xTblZ7djEr3aroa5_NRu_NTAJKbD8GbTm5zNuF9FQOLqFrGcMGw2xeHI9IQc3Ann2xxDQIMeGhJUw2KtR_-mUIk=w400-h500-no "Raspberry Pi setup")

![TV Menu](https://lh3.googleusercontent.com/jsa6yPIJYwAdlmiPo-q1qjAVEZhPCr3dqNUI6CQHBrMSoN3xjUHACUs7CwM5He2VcSILAgINyNDRo7MI7VKqXIKAMcuMRN6Xpeim2eLwjeRYLJU2CcvxZ_VzfipZztMTbenX_S0RJmZE2caKHd8iMRC-zeK3WTIvkcEbDLuiC2xYBGN3_vybeR2xu9eb8eFrBz8h1Hlln-cJngYx2Bfa-Ad-85o9aH1iobhsg7cBKY_6ckJOMoHIH-nIKmAoiOKyihAriKRJHFzSuJ2YwSILawXKZb1pLC10Ewhjq5eEhb1xiedkfH-E08F5QxH0-TxmGLNtv0O7xj5YpgoMpfIzvOwM1rKTCSDbsIso-LYd__RIRxWmnbDnrktajCr3Y-uda-PAmIjEXTdp0Mbu2eRHTLGeUViNWEaIdesTYkBlVog4MWrb63XyHkzjtuvQiuhdglhF8bR-ytItrC5DThSDZsn1dcGT8QvRKGmO1VFdCNDcKQtZUu2TFWDSuTzG4uLeUuzMZKWpn0XhNbrDQpS_seTMOpg2_jX-zP90BKu6NZgYi9wF0CBfErXHbwyMekuuh0p0VFHVm9PJv3rTmcneP2TrU_G5gkvMUnePdHDDDQwM3y6nNNUtksPsfpH3Z_aBRNkSLPhrItFHSHrNEcrd5LjwznKDobzIOSo=w500-h400-no "TV Menu")

This project cannot be simply run blindfolded because requires some custom setup that currently need to be done manually, but I may add a proper installation menu in the future.

## Custom setup on my system
### Hardware
- using flirc for remote control, using custom key map (that depends on remote device)
- using HD Star v3 satellite decoder http://www.ebay.co.uk/itm/HDStar-DVB-S2-TV-Box-USB-Satellite-Receiver-for-Windows-Linux-FREESAT-HOTBIRD-/322382413057
- foot switch
- custom wooden mount

### Software
- depends on media kernel modules from crasycat to detect the HD Star decoder https://bitbucket.org/CrazyCat/media_build
- requires device firmware file
- using mplayer, omxplayer, fbi as external tools
- using python modules as evdev
- requires updating config some files

### What does this project currently do:
- play some simple games like tetris and 2048 using the remote control
- listen to radio channels by IP streaming
- watch satellite channels
- watch videos and music files on local drives, automatic loop through

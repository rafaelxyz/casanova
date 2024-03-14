
#  Raspberry program


```
    restart after "correct": 1 <Enter>
    blank screen: <Enter>
    shutdown: szcz<Enter>
    exit to shell: ctrl + c
    start from shell: x <Enter>
´´´

# Passwords

```
    casanova: 123
    pi: raspberry
´´´

# Notes
## /boot/config.txt
```
    dtoverlay=tft35a:rotate=90
´´´

## autologin

```
    sudo raspi-config
    sudo vi /etc/systemd/system/getty@tty1.service.d/autologin.conf
´´´

## /etc/sudoers

```
    ALL ALL=(root) NOPASSWD: /sbin/shutdown
    Cmd_Alias ESCAPE_ROOM = /home/casanova/casanova/run.py
    casanova ALL=(ALL) NOPASSWD: ESCAPE_ROOM
´´´

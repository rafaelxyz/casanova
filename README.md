

# autologin
  sudo raspi-config
  sudo vi /etc/systemd/system/getty@tty1.service.d/autologin.conf

# /etc/sudoers

  Cmd_Alias ESCAPE_ROOM = /home/casanova/casanova/run.py
  casanova ALL=(ALL) NOPASSWD: ESCAPE_ROOM

#!/bin/bash

mkdir -p /home/builduser/.ssh
chmod 700 /home/builduser/.ssh
echo "aur.archlinux.org ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIEuBKrPzbawxA/k2g6NcyV5jmqwJ2s+zpgZGZ7tpLIcN" > known_hosts
echo "$2" > /home/builduser/.ssh/aur_key
chmod 400 /home/builduser/.ssh/aur_key
export GIT_SSH_COMMAND="ssh -i /home/builduser/.ssh/aur_key"

/publishpkg.py "$1"

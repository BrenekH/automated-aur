#!/bin/bash

sudo mkdir -p /home/builder
sudo chown -R builder:builder /home/builder
mkdir -p /home/builder/.ssh
chmod 700 /home/builder/.ssh
echo "aur.archlinux.org ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIEuBKrPzbawxA/k2g6NcyV5jmqwJ2s+zpgZGZ7tpLIcN" > /home/builder/.ssh/known_hosts
echo "$2" > /home/builder/.ssh/aur_key
chmod 600 /home/builder/.ssh/aur_key
export GIT_SSH_COMMAND="ssh -i /home/builder/.ssh/aur_key"

/publishpkg.py "$1"

#!/bin/bash

sudo chmod 666 /github/home

python -u /buildpkg.py "$@"

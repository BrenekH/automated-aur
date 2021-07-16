#!/bin/bash

/buildpkg.py "$@"

echo "::set-output name=result::$(cat /buildout/out.txt)"

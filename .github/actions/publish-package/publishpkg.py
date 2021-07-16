#!/bin/env python3
import sys

def main():
	# TODO: Clone the existing AUR repo to a dir in `/tmp`.
	# TODO: Copy `PKGBUILD` and everything in the `manifest.include` array to the repo.
	# TODO: Recreate `.SRCINFO` using `makepkg --printsrcinfo > .SRCINFO`.
	# TODO: Ensure proper `.gitignore` file is in the repo (useful for new packages, not yet uploaded).
	# TODO: Force-add all modified files to the repo
	# TODO: Push to AUR
	# TODO: Output any complications to standard output and exit with the proper code.
	return

if __name__ == "__main__":
	main(sys.argv[1])

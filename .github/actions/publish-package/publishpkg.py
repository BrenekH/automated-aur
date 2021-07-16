#!/bin/env python3
import json, shutil, subprocess, sys, tempfile
from pathlib import Path
from typing import List

def main(_package_dir: str):
	pkg_dir = Path(_package_dir)

	with (pkg_dir / ".aurmanifest.json").open("r") as f:
		manifest = json.load(f)

	with tempfile.TemporaryDirectory() as git_td:
		# Clone the existing AUR repo to a dir in `/tmp`.
		subprocess.check_call(["git", "clone", f"https://aur.archlinux.org/{manifest['name']}.git", git_td])

		# Copy `PKGBUILD` and everything in the `manifest.include` array to the repo.
		copy_files_to_dir([pkg_dir / "PKGBUILD"] + [pkg_dir / f for f in manifest["include"]], Path(git_td))

		# Recreate `.SRCINFO` using `makepkg --printsrcinfo > .SRCINFO`.
		subprocess.check_call(["makepkg", "-do", "--nocheck", "--noprepare", "--printsrcinfo", ">", ".SRCINFO"], cwd=git_td, shell=True)

		# TODO: Ensure proper `.gitignore` file is in the repo (useful for new packages, not yet uploaded).

		# Force-add all modified files to the repo
		subprocess.check_call(["git", "add", "-f"] +  ["PKGBUILD"] + manifest["include"],  cwd=git_td)

		# TODO: Push to AUR

		# TODO: Output any complications to standard output and exit with the proper code.

	return

def copy_files_to_dir(files: List[Path], dir: Path):
	for f in files:
		if f.is_absolute():
			print(f"{f} is an absolute Path. It will not be copied.")
			continue
		shutil.copy(f, dir / f.name)

if __name__ == "__main__":
	main(sys.argv[1])

#!/bin/env python3
import json, os, re, shutil, subprocess, sys, tempfile
from pathlib import Path
from typing import List

def main(_package_dir: str):
	pkg_dir = Path(_package_dir)

	with (pkg_dir / ".aurmanifest.json").open("r") as f:
		manifest = json.load(f)

	with tempfile.TemporaryDirectory() as git_td:
		# Clone the existing AUR repo to a dir in `/tmp`.
		print("[INFO] Cloning existing AUR repo")
		subprocess.check_call(["git", "clone", f"aur@aur.archlinux.org:{manifest['name']}.git", git_td])

		print("[INFO] Setting up git config")
		subprocess.check_call(["git", "config", "user.name", "Brenek Harrison"], cwd=git_td)
		subprocess.check_call(["git", "config", "user.email", "brenekharrison@gmail.com"], cwd=git_td)

		# Copy `PKGBUILD` and everything in the `manifest.include` array to the repo.
		print("[INFO] Copying files to git repo")
		copy_files_to_dir([pkg_dir / "PKGBUILD"] + [pkg_dir / f for f in manifest["include"]], Path(git_td))

		# Recreate .SRCINFO
		print("[INFO] Creating .SRCINFO")
		src_info = subprocess.check_output(["makepkg", "--printsrcinfo"], cwd=git_td, universal_newlines=True)
		with (Path(git_td) / ".SRCINFO").open("w") as f:
			f.write(src_info)

		# Ensure proper .gitignore file is in the repo (useful for new packages, not yet uploaded).
		print("[INFO] Writing .gitignore")
		with (Path(git_td) / ".gitignore").open("w") as f:
			f.write("# Require every item to be force added\n*")

		# Force-add all modified files to the repo (if .gitignore hasn't changed, force-adding it won't break anything, so it's hardcoded in)
		print("[INFO] Adding files")
		subprocess.check_call(["git", "add", "-f"] + ["PKGBUILD", ".SRCINFO", ".gitignore"] + manifest["include"],  cwd=git_td)

		print("[INFO] Committing")
		commit_msg = gen_commit_msg(git_td) + ["-m", "Automatically committed from https://github.com/BrenekH/automated-aur."]
		print(commit_msg)
		subprocess.check_call(["git", "commit"] + commit_msg, cwd=git_td)

		# Push to AUR
		print("[INFO] Pushing to AUR")
		# subprocess.check_call(["git", "push"],  cwd=git_td)

	return

def copy_files_to_dir(files: List[Path], dir: Path):
	for f in files:
		if f.is_absolute():
			print(f"{f} is an absolute Path. It will not be copied.")
			continue
		shutil.copy(f, dir / f.name)

def gen_commit_msg(cwd) -> List[str]:
	changes = subprocess.check_output(["git", "commit", "--short"], universal_newlines=True, cwd=cwd)

	if "PKGBUILD" in changes:
		pkgbuild_diff = subprocess.check_output(["git", "diff", "HEAD~1", "PKGBUILD"], cwd=cwd, universal_newlines=True)

		pkgver_match = re.search(r"-pkgver=.*\n\+pkgver=(.*)", pkgbuild_diff)
		pkgrel_match = re.search(r"-pkgrel=.*\n\+pkgrel=(.*)", pkgbuild_diff)

		if pkgver_match is not None or pkgrel_match is not None:
			# Use an "Update commit" format. (ex. "Update to {version}")
			with (Path(cwd) / "PKGBUILD").open("r") as f:
				pkgbuild_contents = f.read()

			pkgver = re.search(r"pkgver=(.*)", pkgbuild_contents).group()
			pkgrel = re.search(r"pkgrel=(.*)", pkgbuild_contents).group()

			return ["-m", f"Update to {pkgver}-{pkgrel}"]

	# TODO: Use PR title as commit title (possibly description as well?)
	with Path(os.getenv("GITHUB_EVENT_PATH")) as f:
		event = json.load(f)

	print(event)

	return ["-m", "Changed files"]

if __name__ == "__main__":
	main(sys.argv[1])

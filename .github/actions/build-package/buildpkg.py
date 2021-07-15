#!/bin/env python3
import json, tempfile, shutil, subprocess, sys
from pathlib import Path
from typing import List

def build(pkg_dir_str: str) -> bool:
	pkg_dir = Path(pkg_dir_str)

	with (pkg_dir / ".aurmanifest.json").open("r") as f:
		manifest = json.load(f)

	with tempfile.TemporaryDirectory() as td:
		# Copy PKGBUILD and everything in the manifest.include list to a new directory in /tmp.
		copy_files_to_dir([pkg_dir / "PKGBUILD"] + [pkg_dir / f for f in manifest["include"]], Path(td))

		makepkg_proc = subprocess.run(["makepkg", "-sm", "--noconfirm", "--noprogressbar"], cwd=td, stdout=subprocess.PIPE, universal_newlines=True)

		pkgbuild_namcap_proc = subprocess.run(["namcap", "-im", "PKGBUILD"], cwd=td, stdout=subprocess.PIPE, universal_newlines=True)

		if makepkg_proc.returncode != 0:
			print(f"namcap PKGBUILD: {pkgbuild_namcap_proc.stdout}")
			print(f"Skipping remaning checks: makepkg returned a non-zero exit code {makepkg_proc.returncode}\n{makepkg_proc.stdout}\n{makepkg_proc.stderr}")
			return False

		# Find the built package
		built_pkg_file = str(list(Path(td).glob("*.pkg.tar.zst"))[0])

		pkg_namcap_proc = subprocess.run(["namcap", "-im", built_pkg_file], cwd=td, stdout=subprocess.PIPE, universal_newlines=True)

		pacman_U_proc = subprocess.run(["sudo", "pacman", "-U", "--noconfirm", built_pkg_file], cwd=td, universal_newlines=True)

	# Run manifest.testCmd.
	testCmd = None
	if (testCmd := manifest["testCmd"]) != None:
		if type(testCmd) == type([]):
			testCmd_proc = subprocess.run(testCmd, shell=True, stdout=subprocess.PIPE, universal_newlines=True)
		else:
			print("testCmd must be an array")

	if makepkg_proc.returncode != 0: print(f"makepkg: {makepkg_proc.stdout}\n{makepkg_proc.stderr}")
	print(f"namcap PKGBUILD: {pkgbuild_namcap_proc.stdout}\n{pkgbuild_namcap_proc.stdout}")
	print(f"namcap *.pkg.tar.zst: {pkg_namcap_proc.stdout}\n{pkgbuild_namcap_proc.stderr}")
	print(f"pacman -U: {pacman_U_proc.stdout}\n{pacman_U_proc.stderr}")
	if testCmd != None: print(f"testCmd: {testCmd_proc.stdout}\n{testCmd_proc.stderr}")

	if not is_namcap_error_free(pkgbuild_namcap_proc.stdout) or \
		not is_namcap_error_free(pkg_namcap_proc.stdout) or \
		pkgbuild_namcap_proc.returncode != 0 or \
		pkg_namcap_proc.returncode != 0 or \
		pacman_U_proc.returncode != 0 or \
		(testCmd != None and testCmd_proc.returncode != 0):
		return False

	return True

def copy_files_to_dir(files: List[Path], dir: Path):
	print(files, dir)
	# TODO: Implement

	for f in files:
		if f.is_absolute():
			print(f"{f} is an absolute Path. It will not be copied.")
			continue
		shutil.copy(f, dir / f.name)

def is_namcap_error_free(output: str) -> bool:
	return True

if __name__ == "__main__":
	if not build(sys.argv[1]):
		sys.exit(1)

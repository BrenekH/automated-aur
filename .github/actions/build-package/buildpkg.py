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

		print("[INFO] Running makepkg")
		makepkg_proc = subprocess.run(["makepkg", "-sm", "--noconfirm", "--noprogressbar"], cwd=td, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)

		print("[INFO] Running namcap against PKGBUILD")
		pkgbuild_namcap_proc = subprocess.run(["namcap", "-i", "PKGBUILD"], cwd=td, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)

		if makepkg_proc.returncode != 0:
			check_results = f"makepkg:\nStdout:\n{makepkg_proc.stdout}\nStderr:\n{makepkg_proc.stderr}\n"
			check_results += f"namcap PKGBUILD:\nStdout:\n{pkgbuild_namcap_proc.stdout}\nStderr:\n{pkgbuild_namcap_proc.stdout}\n"
			check_results += f"Skipping remaining checks: makepkg returned a non-zero exit code {makepkg_proc.returncode}"
			print(f"Skipping remaining checks: makepkg returned a non-zero exit code {makepkg_proc.returncode}")
			return check_results

		# Find the built package
		built_pkg_file = str(list(Path(td).glob("*.pkg.tar.zst"))[0])

		print("[INFO] Running namcap against generated package")
		pkg_namcap_proc = subprocess.run(["namcap", "-i", built_pkg_file], cwd=td, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)

		print("[INFO] Installing built package")
		pacman_U_proc = subprocess.run(["sudo", "pacman", "-U", "--noconfirm", built_pkg_file], cwd=td, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)

	# Run manifest.testCmd.
	testCmd = None
	if (testCmd := manifest["testCmd"]) != None:
		if type(testCmd) == type([]):
			print("[INFO] Running user-defined testCmd")
			testCmd_proc = subprocess.run(testCmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
		else:
			print("[ERROR] testCmd must be an array or null")
			sys.exit(1)

	check_results = ""
	if makepkg_proc.returncode != 0:
		check_results += f"makepkg:\nStdout:\n{makepkg_proc.stdout}\nStderr:\n{makepkg_proc.stderr}\n"

	check_results += f"namcap PKGBUILD:\nStdout:\n{pkgbuild_namcap_proc.stdout}\nStderr:\n{pkgbuild_namcap_proc.stdout}\n"
	check_results += f"namcap *.pkg.tar.zst:\nStdout\n{pkg_namcap_proc.stdout}\nStderr:\n{pkgbuild_namcap_proc.stderr}\n"

	if pacman_U_proc.returncode != 0:
		check_results += f"pacman -U:\nStdout:\n{pacman_U_proc.stdout}\nStderr:\n{pacman_U_proc.stderr}\n"

	if testCmd != None and testCmd_proc.returncode != 0:
		check_results += f"testCmd:\nStdout:\n{testCmd_proc.stdout}\nStderr:\n{testCmd_proc.stderr}\n"

	return check_results

def copy_files_to_dir(files: List[Path], dir: Path):
	for f in files:
		if f.is_absolute():
			print(f"{f} is an absolute Path. It will not be copied.")
			continue
		shutil.copy(f, dir / f.name)

if __name__ == "__main__":
	output = build(sys.argv[1])

	if "--stdout" in sys.argv:
		print(output)
	else:
		with open("/buildout/out.txt", "w") as f:
			f.write(output)

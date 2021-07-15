# Script Implementation Details

## Build on PR code update

1. Copy `PKGBUILD` and everything in the `manifest.include` array to a new directory in `/tmp`.
2. Build package using the `makepkg` command.
3. Run `namcap` against the `PKGBUILD` and the created package.
4. Run `manifest.testCmd` in an environment where the package has been installed. In the context of a GitHub actions job, if the current OS running the script is Arch, then installing the package without any separate environment is acceptable.
5. Output any complications to standard output and exit with the proper code.

## Publish on PR accepted

1. Clone the existing AUR repo to a dir in `/tmp`.
2. Copy `PKGBUILD` and everything in the `manifest.include` array to the repo.
3. Recreate `.SRCINFO` using `makepkg --printsrcinfo > .SRCINFO`.
4. Ensure proper `.gitignore` file is in the repo (useful for new packages, not yet uploaded).
5. Force-add all modified files to the repo
6. Push to AUR
7. Output any complications to standard output and exit with the proper code.

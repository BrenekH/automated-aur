# Automated AUR

This repository is meant to automate the upload of PKGBUILDs to the Arch Linux User Repository.

## Workflow

* First a PR is opened with changes to the PKGBUILD and other files to build the package.

* The build system will check the updates to make sure they build and pass namcap (and any other checks defined in the manifest).
  * Build results will be reported back as a comment on the PR.

* If I'm happy with the results (and all checks are passing), a "LGTM!" comment or applying the lgtm tag will publish the package to the AUR, and merge/close the PR.

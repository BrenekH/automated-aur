# Automated AUR

Automated PKGBUILD uploads to the [Arch User Repository](https://aur.archlinux.org).

## How it works

It all starts with a new pull request with a change in one of the packages.
Github Actions will automatically build and test the changes and comment the results on the PR.

As soon as the `lgtm` label is applied to the PR, Github Actions will generate the `.SRCINFO` file and push the files to the AUR.

### Automatic Updates

Using the `.aurmanifest.json`, an hourly cron job will create new PRs for packages with new versions available.
However, approval is still required using the `lgtm` label as normal.

## Other notes

To help with run times, the docker image actions are built from [BrenekH/automated-aur-docker](https://github.com/BrenekH/automated-aur-docker) and hosted using the Github Container Registry.
The docker images are rebuilt every day at 01:00 UTC so that they are up-to-date with the daily [archlinux/archlinux](https://hub.docker.com/r/archlinux/archlinux) base image.

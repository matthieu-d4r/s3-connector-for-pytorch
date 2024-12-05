#!/usr/bin/env bash
#
# Mount an NVMe drive (by default, at `./nvme/`) relative to where this script is run. If a drive is already mounted at
# the specified location, simply clear its content.

nvme_dir=${1:-"./nvme/"} # default value

if ! mountpoint -q "$nvme_dir"; then
  sudo mkfs -t xfs /dev/nvme1n1
  sudo mount /dev/nvme1n1 "$nvme_dir"
#  sudo chmod 777 "$nvme_dir"
fi

rm -rf "${nvme_dir:?}"/* # https://www.shellcheck.net/wiki/SC2115

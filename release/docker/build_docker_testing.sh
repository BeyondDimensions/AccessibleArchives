#!/bin/bash
# Get the directory of this script
work_dir="$( cd -- "$(dirname "$0")" >/dev/null 2>&1 ; pwd -P )"
# change to root directory of the Brenthy repo
cd $work_dir/../..

docker build --no-cache -t local/accessible_archives_testing -f release/docker/AccessibleArchives_testing.dockerfile .

## Save docker image to file:
# docker save -o /tmp/AccessibleArchives.tar local/accessible_archives_testing

## Run with:
# docker run -it --privileged local/accessible_archives_testing
# release/docker/run_docker_testing.sh
#!/bin/bash
# Get the directory of this script
work_dir="$( cd -- "$(dirname "$0")" >/dev/null 2>&1 ; pwd -P )"
# change to root directory of the Brenthy repo
cd $work_dir/../..

docker build -t local/accessible_archives_prereqs -f release/docker/AccessibleArchives_prereqs.dockerfile .


docker save -o /tmp/AccessibleArchives.tar local/accessible_archives_prereqs

## Run with:
# docker run -it --privileged local/accessible_archives_prereqs
# release/docker/run_docker_prereqs.sh
## Quick Guide
To build a docker image, run:
```sh
# build docker image
release/docker/build_docker_prereqs.sh
release/docker/build_docker_testing.sh

# run docker image
release/docker/run_docker_testing.sh
# Wait for 5-10min for models to download and document collection to be processed.

# open accessible archives in your browser under http://localhost:8501/
```

## Explanation

The `build_docker_prereqs.sh` shell script uses the `AccessibleArchives_prereqs.dockerfile` dockerfile definition to create a docker image called `build_docker_prereqs` with all the prerequisites installed.
It takes a long time (~5min) to build this docker image.
Run this docker image by running `run_docker_prereqs.sh`.

The `build_docker_testing.sh` shell script uses the `AccessibleArchives_testing.dockerfile` dockerfile definition to create a docker image based on the `build_docker_prereqs` image in which only the AccessibleArchives source code is updated.
It takes a short amount of time (~40sec) to build this docker image.
Run this docker image by running `run_docker_testing.sh`. It will print the container ID.

When running a docker container for the first time, the models will be downloaded and the document collections processed before it becomes usable.
This might take 5-10min.
You can check the status of this from your host machine by running:
```sh
docker exec -it $CONTAINER_ID /bin/tail -f /opt/AccessibleArchives/FinalInstallations.log
```
You can then open AccessibleArchives in your browser under http://localhost:8501/

## DevOps Workflow

- To get started with using the docker image in the development of AccessibleArchives, run `build_docker_prereqs.sh` followed by `build_docker_testing.sh`
- To run a docker container, run `run_docker_testing.sh`
- Every time you change AccessibleArchives' source code, run `build_docker_testing.sh` and then run `run_docker_testing.sh` to create a new docker container with the updated application.
- Every time you change the prerequisites of AccessibleArchives' source code, run `build_docker_prereqs.sh` then run `build_docker_testing.sh` and then run `run_docker_testing.sh` to create a new docker container with the updated application.
- To watch the AccessibleArchives logs, run:
```sh
docker exec -it $CONTAINER_ID /bin/journalctl -ef -u accessible_archives
```


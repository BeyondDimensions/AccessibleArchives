## Understanding Docker Volume Mounts
### Rationale
_why we use docker volume mounting_
This docker container works with various folders that contain large amounts of data or take a long time to generate
- IPFS: all files in a DocumentCollection are processed and stored under `~/.ipfs`
- Ollama: downloaded models are rather large!
  - Linux `/usr/share/ollama/.ollama/models`
  - MacOS `~/.ollama/models`
  - Windows `C:\Users%username%.ollama\models`
- Text Embeddings: Significant in data size, but above all costly to produce, as it can take several hours to generate the embeddings for LLMs from text.

To avoid downloading models, processing documents for IPFS and generating text embeddings every time a docker container is created, and to stop the docker container from using too much disk space, we can store these folders outside of the docker containers on our host machine and mount them into the docker container using volume mounts for the docker containers to access.

Likewise it is practical to store the DocumentCollections we want the AccessibleArchives docker container to process to be stored on our host machine.

### Implementation
_how we implement docker volume mounting_

In [run_docker_testing.sh](/release/docker/run_docker_testing.sh), when creating a docker container, we pass several arguments labelled `-v` which consist of two paths separated by a colon.
The path on the left specifies the path on the host machine that needs to be mounted in the docker container, and the path on the right of the colon specifies the mount-point inside the docker container.

```sh
  -v $CONTAINER_DATA_PATH/Ollama:/usr/share/ollama \
```

You can adjust the value of the path on your host machine in this definition:
```sh
CONTAINER_DATA_PATH=/opt/AccessibleArchives
```

Make sure that this path contains the subfolders which are mounted by [run_docker_testing.sh](/release/docker/run_docker_testing.sh), and place your DocumentCollections in the DocumentCollections subfolder.

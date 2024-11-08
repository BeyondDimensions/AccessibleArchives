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

Make sure that this path contains the subfolders which are mounted by [run_docker_testing.sh](/release/docker/run_docker_testing.sh), and place your DocumentCollections in the DocumentCollections subfolder, and the text-embeddings in the DocumentEmbeddings subfolder.
Also, put credentials.env in the Config subfolder with the OPENAI_API_KEY field set.

The folder should look something like this:
```
.
├── Config
│   └── credentials.env
├── DocumentCollections
│   ├── Demo
│   └── RAF
├── DocumentEmbeddings
│   ├── Demo
│   └── RAF
├── ipfs
└── Ollama
```

## Using for Development

If you want to use the docker container for development to avoid installing all the prerequisites on your main machine, mount this project's `/src` directory to `/opt/AccessibleArchives/src` in the docker container by adding the follwoing line to [run_docker_testing.sh](/release/docker/run_docker_testing.sh):

```sh
  -v path/to/src:/opt/AccessibleArchives/src \
```

Create a new docker container using that script, and now whenever you update the source code, the Streamlit WebUI should notify you and offer to rerun in the top right corner of is window.

## Logs

```sh
docker exec -it $CONTAINER_ID /bin/journalctl -ef -u accessible_archives
```

## Notes

- If you add documents to your DocumentCollections folder, you will have to manually get them processed by IPFS in the docker container:

```sh
docker exec -it $CONTAINER_ID /usr/local/bin/ipfs add -r /opt/AccessibleArchives/DocumentCollections
```

#/bin/bash

# path on the host machine were to store the Docker container's data
CONTAINER_DATA_PATH=/opt/AccessibleArchives

docker run -d --privileged \
  -p 8501:8501 \
  -v $CONTAINER_DATA_PATH/ipfs:/root/.ipfs \
  -v $CONTAINER_DATA_PATH/Ollama:/usr/share/ollama \
  -v $CONTAINER_DATA_PATH/ChromaDB:/opt/AccessibleArchives/ChromaDB \
  -v $CONTAINER_DATA_PATH/DocumentCollections:/opt/AccessibleArchives/DocumentCollections \
  -v $CONTAINER_DATA_PATH/Config:/opt/AccessibleArchives/Config \
  local/accessible_archives_testing


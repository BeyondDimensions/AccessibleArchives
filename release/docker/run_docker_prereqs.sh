#|/bin/bash
docker run -d --privileged \
  -p 8501:8501 \
  -v /opt/AccessibleArchives/ChromaDB:/opt/AccessibleArchives/ChromaDB \
  -v /opt/AccessibleArchives/DocumentCollections:/opt/AccessibleArchives/DocumentCollections \
  -v /opt/AccessibleArchives/Config:/opt/AccessibleArchives/Config \
  local/accessible_archives_prereqs


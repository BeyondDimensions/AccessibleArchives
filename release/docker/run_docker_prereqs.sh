docker run -d docker run --privileged \
  -p 8501:8501 \
  -v /opt/AccessibleArchives/ChromaDB:/opt/AccessibleArchives/ChromaDB \
  -v /opt/AccessibleArchives/.data:/opt/AccessibleArchives/DocumentCollection \
  -v /opt/AccessibleArchives/Config:/opt/AccessibleArchives/Config \
  local/accessible_archives


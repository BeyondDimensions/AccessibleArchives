docker run -it --privileged \
  -p 8501:8501 \
  -v /opt/AccessibleArchives/ChromaDB:/opt/AccessibleArchives/ChromaDB \
  -v /opt/AccessibleArchives/DocumentCollection:/opt/AccessibleArchives/DocumentCollection \
  -v /opt/AccessibleArchives/Config:/opt/AccessibleArchives/Config \
  local/accessible_archives_testing


docker run -d \
  -p 8501:8501 \
  -v /path/on/host/ChromaDB:/opt/AccessibleArchives/ChromaDB \
  -v /path/on/host/DocumentCollection:/opt/AccessibleArchives/DocumentCollection \
  -v /path/on/host/Configs:/opt/AccessibleArchives/Configs \
  local/accessible_archives


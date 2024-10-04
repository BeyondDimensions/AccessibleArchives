FROM local/accessible_archives_prereqs:latest
WORKDIR /opt/AccessibleArchives

COPY src /opt/AccessibleArchives/src
COPY release /opt/AccessibleArchives/release

COPY release/docker/docker_first_run_installation_config.sh /opt/AccessibleArchives/release/docker
COPY release/docker/docker_first_run_installations.sh /opt/AccessibleArchives/release/docker

RUN /opt/AccessibleArchives/release/docker/docker_first_run_installation_config.sh
# RUN /opt/AccessibleArchives/release/web/accessible_archives.service.sh

# run some installations we couldn't before
# CMD /opt/AccessibleArchives/release/web/run_webui.sh
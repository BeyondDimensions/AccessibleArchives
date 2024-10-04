FROM emendir/systemd-ipfs:latest
WORKDIR /opt/AccessibleArchives

COPY src /opt/AccessibleArchives/src
COPY release /opt/AccessibleArchives/release

RUN apt update
RUN apt install -y sudo
ENV DEBIAN_FRONTEND=noninteractive

# install some packages manually to avoid getting stuck in  install_webui.sh
RUN DEBIAN_FRONTEND=noninteractive apt-get update && \
    echo "tzdata tzdata/Areas select Etc" | debconf-set-selections && \
    echo "tzdata tzdata/Zones/Etc select UTC" | debconf-set-selections && \
    apt-get install -y tzdata
RUN touch /opt/AccessibleArchives/release/web/we_are_in_docker
RUN /opt/AccessibleArchives/release/web/install_webui.sh
RUN /opt/AccessibleArchives/release/web/ipfs/install_ipfs_monitor.sh
RUN ln -s /opt/AccessibleArchives/DocumentCollection /opt/AccessibleArchives/.data
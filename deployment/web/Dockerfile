FROM ubuntu:latest

ENV DEBIAN_FRONTEND=noninteractive

# Update package lists and install necessary packages

RUN apt-get update && \
    apt-get install -y \
        pandoc \
        texlive \
        texlive-xetex \
        texlive-fonts-recommended \
        ollama

# Clean up apt cache to reduce image size

RUN apt-get clean && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY . /app

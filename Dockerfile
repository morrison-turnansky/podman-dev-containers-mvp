# Set Fedora version
ARG FEDORA_VERSION=41

# Base image
FROM fedora:${FEDORA_VERSION}

# Run as root for now (Podman devcontainers are rootless by default, so this is okay)
USER root

# Install development tools and Python build essentials
RUN dnf upgrade --refresh -y && \
    dnf install -y \
        python3 \
        python3-devel \
        python3-pip \
        git \
        gcc \
        gcc-c++ \
        make \
        cmake \
        ninja-build \
        ccache \
        gdb \
        vim \
        curl \
        unzip \
        which \
        libffi-devel \
        openssl-devel \
        findutils && \
    dnf clean all

# Symlink `python` to `python3`
RUN ln -sf /usr/bin/python3 /usr/bin/python

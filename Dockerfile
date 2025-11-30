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

# Install Google Cloud CLI
RUN tee /etc/yum.repos.d/google-cloud-sdk.repo << EOM
[google-cloud-cli]
name=Google Cloud CLI
baseurl=https://packages.cloud.google.com/yum/repos/cloud-sdk-el9-x86_64
enabled=1
gpgcheck=1
repo_gpgcheck=0
gpgkey=https://packages.cloud.google.com/yum/doc/rpm-package-key.gpg
EOM

RUN dnf install -y google-cloud-cli && \
    dnf clean all

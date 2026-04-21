# syntax=docker/dockerfile:1

# SPDX-FileCopyrightText: 2025 Pierre-Noel Bouteville <pnb990@gmail.com>
# SPDX-License-Identifier: BSD-3-Clause

# ------------------------------------------------------------------------------
# Base image
# ------------------------------------------------------------------------------
FROM debian:trixie AS partkeepr-base

# -------------------------------------------------------------------
# Configuration and Environment Variables
# -------------------------------------------------------------------
ENV PYTHONUNBUFFERED 1

# -------------------------------------------------------------------
# Base Tool Install
# -------------------------------------------------------------------
RUN apt-get update && export DEBIAN_FRONTEND=noninteractive \
    && apt-get install -y --no-install-recommends \
    postgresql-client \
    libpq-dev \
    locales \
    ca-certificates \
    python3 \
    python3-dev \
    gcc \
    pipenv \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

FROM partkeepr-base AS partkeepr-dev

# -------------------------------------------------------------------
# Install Dev Tools and Debugging Utilities
# -------------------------------------------------------------------
RUN apt-get update && apt-get install -y --no-install-recommends \
    sudo \
    ssh \
    curl \
    git \
    acl \
    bash-completion \
    vim \
    iputils-ping

# -------------------------------------------------------------------
# Locale Setup
# -------------------------------------------------------------------
RUN sed -i '/en_US.UTF-8/s/^# //g' /etc/locale.gen && locale-gen

ENV LANG=en_US.UTF-8 \
    LANGUAGE=en_US:en \
    LC_ALL=en_US.UTF-8

# -------------------------------------------------------------------
# Add Dev User
# -------------------------------------------------------------------
ARG USERNAME=dev

RUN useradd -m $USERNAME \
    && echo "$USERNAME ALL=(root) NOPASSWD:ALL" > /etc/sudoers.d/$USERNAME \
    && chmod 0440 /etc/sudoers.d/$USERNAME

USER $USERNAME
ENV SHELL=/bin/bash

# -------------------------------------------------------------------
# Setup Workspace Directory
# -------------------------------------------------------------------
RUN mkdir -p /home/$USERNAME/project

# -------------------------------------------------------------------
# Metadata and Entrypoint
# -------------------------------------------------------------------
LABEL maintainer="Pierre-Noel Bouteville <pnb990@gmail.com>" \
    description="Devcontainer image for PyPnbPartKeepr Django project"

USER $USERNAME
CMD ["/bin/bash"]

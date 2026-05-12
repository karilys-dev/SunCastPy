ARG STAGE=base
# Use official slim Python image
FROM python:3.12-slim AS base

# Prevent Python from writing pyc files & enable stdout logging
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Install system dependencies (example: curl)
# Clean up apt cache to reduce vulnerabilities and image size (Trivy-friendly)
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        curl \
        git \
        locales \
    && sed -i 's/^# *en_US.UTF-8 UTF-8/en_US.UTF-8 UTF-8/' /etc/locale.gen \
    && locale-gen \
    && update-locale LANG=en_US.UTF-8 LC_ALL=en_US.UTF-8 \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

ENV LANG=en_US.UTF-8
ENV LC_ALL=en_US.UTF-8

# Create user
# Update pip and create virtual environment
# Ensure home + workspace are owned correctly
ARG USERNAME=devuser
ARG USER_UID=1000
ARG USER_GID=1000

RUN groupadd --gid $USER_GID $USERNAME \
    && useradd --uid $USER_UID --gid $USER_GID -m $USERNAME \
    && pip install --upgrade pip \
    && mkdir -p /workspace \
    && chown -R $USERNAME:$USERNAME /workspace

FROM base as robot-browser
ARG ROBOT=false

# This step only executes if ROBOT is explicitly set to 'true'
RUN if [ "$ROBOT" = "true" ] ; then \
        apt-get update \
        && apt-get install -y --no-install-recommends \
            nodejs \
            npm \
        && apt-get clean \
        && rm -rf /var/lib/apt/lists/* ; \
    fi

FROM ${STAGE} as final
# Switch to non-root user
USER $USERNAME
WORKDIR /workspace
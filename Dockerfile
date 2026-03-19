# Use official slim Python image
FROM python:3.12-slim

# Prevent Python from writing pyc files & enable stdout logging
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Install system dependencies (example: curl)
# Clean up apt cache to reduce vulnerabilities and image size (Trivy-friendly)
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        curl \
        git \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

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

# Switch to non-root user
USER $USERNAME
WORKDIR /workspace
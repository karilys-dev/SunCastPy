# Use official slim Python image
ARG PYTHON_VERSION

FROM python:${PYTHON_VERSION}-slim AS base

# Prevent Python from writing pyc files & enable stdout logging
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1
ARG ROBOT_FRAMEWORK=false
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
    && if [ "$ROBOT_FRAMEWORK" = "true" ]; then apt-get install -y chromium chromium-driver; fi \
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

# Switch to non-root user
USER $USERNAME
WORKDIR /workspace

COPY --chown=$USERNAME:$USERNAME SunCastPy/pyproject.toml README.md /workspace/
COPY --chown=$USERNAME:$USERNAME SunCastPy/src /workspace/src

RUN pip install --no-cache-dir .[aws]

# FastAPI port
EXPOSE 8000

ENTRYPOINT ["python", "-m", "uvicorn"]
CMD ["SunCastPy.api:app", "--host", "0.0.0.0", "--port", "8000"]
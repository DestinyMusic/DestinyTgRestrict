# ==============================================================================
# DestinyRestrict Dockerfile
# ==============================================================================

FROM python:3.11-slim

ENV PYTHONUNBUFFERED=1
ENV DEBIAN_FRONTEND=noninteractive

# Create non-root user
RUN useradd -m -u 1000 user

WORKDIR /app

# System packages
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    ffmpeg \
    sox \
    mediainfo \
    p7zip-full \
    coreutils \
    build-essential \
    gcc \
    g++ \
    python3-dev \
    git \
    curl \
    wget \
    mkvtoolnix \
    fonts-freefont-ttf && \
    rm -rf /var/lib/apt/lists/*

# Create virtualenv
RUN python -m venv /app/venv

ENV PATH="/app/venv/bin:$PATH"

# Install Python requirements
COPY requirements.txt .

# 🟢 FIX: This forces HuggingFace/Docker to completely wipe the cache from this step forward
ARG CACHE_BUSTER=1 

RUN pip install --upgrade pip setuptools wheel && \
    pip install --no-cache-dir -r requirements.txt

# Copy only the web deployment code paths.
# Android and iOS sources are intentionally excluded from the web runtime.
COPY main.py ./main.py
COPY config.py ./config.py
COPY config.env ./config.env
COPY bot ./bot
COPY core ./core
COPY database ./database
COPY media ./media
COPY streaming ./streaming
COPY web ./web

# Permissions
RUN chown -R user:user /app

USER user

# Web server port
ENV PORT=8080

EXPOSE 8080

# Start bot
CMD ["python", "main.py"]

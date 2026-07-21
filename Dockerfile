FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

ENV LANG=en_US.UTF-8
ENV LANGUAGE=en_US:en
ENV LC_ALL=en_US.UTF-8

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    gcc \
    locales \
    libgl1 \
    libglib2.0-0 \
    libgomp1 \
    poppler-utils \
    && sed -i '/en_US.UTF-8/s/^# //g' /etc/locale.gen \
    && locale-gen \
    && update-locale LANG=en_US.UTF-8 \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

RUN pip install --no-cache-dir --upgrade pip uv && \
    pip install --no-cache-dir \
        torch \
        torchvision \
        --index-url https://download.pytorch.org/whl/cpu && \
    uv pip install --system -r requirements.txt && \
    pip uninstall -y ninja django-ninja && \
    pip install --no-cache-dir django-ninja

COPY . .

EXPOSE 8000
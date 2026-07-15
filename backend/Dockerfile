# Use official Python 3.10 slim image
FROM python:3.10-slim AS base

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV DJANGO_SETTINGS_MODULE config.settings.production

# Set work directory
WORKDIR /app

# Install system dependencies
RUN apt-get update \
    && apt-get install -y --no-install-recommends gcc libpq-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt /app/
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Development stage (installs test/dev tools like pytest)
FROM base AS development
ENV DJANGO_SETTINGS_MODULE config.settings.development
COPY requirements-dev.txt /app/
RUN pip install -r requirements-dev.txt
COPY . /app/
EXPOSE 8000
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

# Production stage
FROM base AS production
COPY . /app/
EXPOSE 8000
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "config.wsgi:application"]

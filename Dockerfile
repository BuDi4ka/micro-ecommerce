FROM python:3.13

COPY ./src/ /app/
WORKDIR /app

# OS-level installs
RUN apt-get update && apt-get install -y --fix-missing \
    build-essential \
    python3-dev \
    python3-setuptools \
    libpq-dev \
    gcc \
    make

# Create and use virtual environment, install dependencies
RUN python3 -m venv /opt/venv && \
    /opt/venv/bin/python -m pip install --upgrade pip && \
    /opt/venv/bin/pip install -r /app/requirements.txt

# Purge build dependencies (optional but good for smaller image)
RUN apt-get remove -y --purge make gcc build-essential && \
    apt-get autoremove -y && \
    rm -rf /var/lib/apt/lists/*

# Collect static files (run with venv python)
RUN /opt/venv/bin/python manage.py collectstatic --noinput

# Make entrypoint executable
RUN chmod +x ./config/entrypoint.sh

# Set the entrypoint (start container with your script)
CMD ["./config/entrypoint.sh"]

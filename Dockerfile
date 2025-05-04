FROM python:3.12.6-slim-bookworm

# Python environment settings
ENV PYTHONFAULTHANDLER=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONHASHSEED=random \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100

# Poetry environment settings
ENV POETRY_NO_INTERACTION=1 \
    POETRY_CACHE_DIR='/var/cache/pypoetry' \
    POETRY_HOME='/usr/local' \
    POETRY_VERSION=2.1.2

# Install dependencies for Poetry
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*
RUN curl -sSL https://install.python-poetry.org | python3 -

# Set the working directory and copy the necessary files
WORKDIR /app
COPY pyproject.toml  /app/

# Install the dependencies in the global Python environment using Poetry
RUN poetry install --no-root  # This installs all dependencies in the containers Python environment

# Copy the remaining application files
COPY . /app

ENV PYTHONPATH="/app/src"
# Run the application using poetry
CMD ["poetry", "run", "python", "src/prospectgeo/main.py"]
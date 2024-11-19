# syntax=docker/dockerfile:1

# Comments are provided throughout this file to help you get started.
# If you need more help, visit the Dockerfile reference guide at
# https://docs.docker.com/go/dockerfile-reference/

# Want to help us make this template better? Share your feedback here: https://forms.gle/ybq9Krt8jtBL3iCk7

ARG PYTHON_VERSION=3.10.13
#ARG PYTHON_VERSION=3.11.8
FROM python:${PYTHON_VERSION}-slim AS base

# Prevents Python from writing pyc files.
ENV PYTHONDONTWRITEBYTECODE=1

# Keeps Python from buffering stdout and stderr to avoid situations where
# the application crashes without emitting any logs due to buffering.
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Create a non-privileged user that the app will run under.
# See https://docs.docker.com/go/dockerfile-user-best-practices/
#ARG UID=10001
#RUN adduser \
#    --disabled-password \
#    --gecos "" \
#    --home "/nonexistent" \
#    --shell "/sbin/nologin" \
#    --no-create-home \
#    --uid "${UID}" \
#   appuser

# Download dependencies as a separate step to take advantage of Docker's caching.
# Leverage a cache mount to /root/.cache/pip to speed up subsequent builds.
# Leverage a bind mount to requirements.txt to avoid having to copy them into
# into this layer.
COPY requirements.txt requirements.txt

#RUN python -m pip install -r requirements.txt
RUN pip install -r requirements.txt

# Switch to the non-privileged user to run the application.
#USER appuser
# Copy the source code into the container.
COPY . .

# Copy the .env.example file to .env
COPY wip/.env.example .env

# Expose the port that the application listens on.
EXPOSE 8000

# Run the application.
CMD ["python", "-m", "uvicorn", "main:app","--proxy-headers", "--host", "0.0.0.0", "--port", "8000"]
#CMD uvicorn src.app:app --proxy-headers --host 0.0.0.0 --port 8000
#CMD ["python3","./main.py"]
#CMD ["some-command", "--option", "value"]

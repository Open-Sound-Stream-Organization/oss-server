FROM python:3.7

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory
WORKDIR /oss_server

# Install dependencies
RUN pip install pipenv
COPY Pipfile Pipfile.lock README.md LICENSE /oss_server/
RUN pipenv install --system

# Copy project
COPY oss_server /oss_server/
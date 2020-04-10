FROM python:slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PYTHONUNBUFFERED 1

# Set work directory
WORKDIR /oss_server

#Install Pillow dependencie
RUN apt update
RUN apt install python-pillow -y
#Install Git
RUN apt install git -y
# Install dependencies
RUN pip install pipenv
COPY Pipfile Pipfile.lock README.md LICENSE start-server.sh /oss_server/
RUN pipenv install --system

# Copy project
COPY oss_server /oss_server/

EXPOSE 8000
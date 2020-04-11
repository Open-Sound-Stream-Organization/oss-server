FROM python:slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PYTHONUNBUFFERED 1

# Set work directory
WORKDIR /oss_server

EXPOSE 8000

# Copy project
COPY oss_server /oss_server/
#Install Pillow dependencie
RUN apt update
RUN apt install python-pillow -y
#Install Git
RUN apt install git -y
# Install dependencies
RUN pip install pipenv
COPY Pipfile Pipfile.lock README.md LICENSE start-server.sh /oss_server/
RUN pipenv install --system
RUN cd /oss_server/oss_server
RUN python manage.py makemigrations --noinput
RUN python manage.py collectstatic --noinput
CMD sh -c "python manage.py makemigrations && gunicorn --bind :8000 --workers 3 oss_server.wsgi"

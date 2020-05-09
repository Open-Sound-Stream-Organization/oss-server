FROM python:alpine as base

# Set work directory
WORKDIR /oss_server
FROM base as builder
# Copy Pipfile
COPY Pipfile /oss_server/
#Install dependencies
RUN apk update \
    && apk upgrade \
    && apk add postgresql-dev gcc python3-dev musl-dev jpeg-dev zlib-dev git \
    && pip install pipenv \
    && pipenv lock -r > requirements.txt \
    && pip install --prefix=/install -r ./requirements.txt
FROM base

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

EXPOSE 8000
# Copy project
COPY Pipfile Pipfile.lock README.md LICENSE start-server.sh oss_server /oss_server/
COPY --from=builder /install /usr/local

VOLUME /oss_server/db

RUN apk add libjpeg zlib ffmpeg \
    && apk --no-cache add --repository http://dl-cdn.alpinelinux.org/alpine/edge/community chromaprint \
    && pip install six certifi \
    && python manage.py collectstatic --noinput

CMD python manage.py migrate --noinput \
    && gunicorn --bind :8000 --workers 3 oss_server.wsgi

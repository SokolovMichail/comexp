FROM ubuntu:latest

WORKDIR /app
ARG DEBIAN_FRONTEND=noninteractive

RUN apt-get update -y && apt-get install -y python3-pip && \
    apt-get install -y ffmpeg libsm6

RUN pip3 install -U pipenv==2022.1.8
COPY Pipfile Pipfile
COPY Pipfile.lock Pipfile.lock
RUN pipenv install --deploy --system
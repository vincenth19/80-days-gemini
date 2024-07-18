FROM python:3.12-slim

RUN apt-get update && apt-get install -y apt-transport-https ca-certificates gnupg curl locales && \
    locale-gen en_US.UTF-8

RUN curl https://packages.cloud.google.com/apt/doc/apt-key.gpg | gpg --dearmor -o /usr/share/keyrings/cloud.google.gpg

RUN echo "deb [signed-by=/usr/share/keyrings/cloud.google.gpg] https://packages.cloud.google.com/apt cloud-sdk main" | tee -a /etc/apt/sources.list.d/google-cloud-sdk.list

USER root

RUN apt-get update && apt-get install -y git vim net-tools build-essential google-cloud-cli=473.0.0-0 \
    && useradd -u 1000 -m docker

ENV LANG=en_US.UTF-8
ENV LANGUAGE=en_US:en
ENV LC_ALL=en_US.UTF-8

WORKDIR /

ENV PYTHONPATH=/app

USER docker
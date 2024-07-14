FROM golang:1.21 AS git-leaks-builder

RUN git clone https://github.com/gitleaks/gitleaks.git && \
    cd gitleaks && \
    VERSION=$(git describe --tags --abbrev=0) && \
    CGO_ENABLED=0 go build -o bin/gitleaks -ldflags "-X="github.com/zricethezav/gitleaks/v8/cmd.Version=${VERSION}

FROM python:3.12-slim

COPY --from=git-leaks-builder /go/gitleaks/bin/* /usr/bin

RUN apt-get update && apt-get install -y apt-transport-https ca-certificates gnupg curl

RUN curl https://packages.cloud.google.com/apt/doc/apt-key.gpg | gpg --dearmor -o /usr/share/keyrings/cloud.google.gpg

RUN echo "deb [signed-by=/usr/share/keyrings/cloud.google.gpg] https://packages.cloud.google.com/apt cloud-sdk main" | tee -a /etc/apt/sources.list.d/google-cloud-sdk.list

USER root

RUN apt-get update && apt-get install -y git vim net-tools build-essential google-cloud-cli=473.0.0-0 \
    && pip install pre-commit \
    && useradd -u 1000 -m docker

WORKDIR /

ENV PYTHONPATH=/app

USER docker
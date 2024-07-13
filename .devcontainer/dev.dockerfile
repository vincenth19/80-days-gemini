FROM golang:1.21 AS git-leaks-builder

RUN git clone https://github.com/gitleaks/gitleaks.git && \
    cd gitleaks && \
    VERSION=$(git describe --tags --abbrev=0) && \
    CGO_ENABLED=0 go build -o bin/gitleaks -ldflags "-X="github.com/zricethezav/gitleaks/v8/cmd.Version=${VERSION}

FROM python:3.12-slim

COPY --from=git-leaks-builder /go/gitleaks/bin/* /usr/bin

USER root
RUN apt update && apt -y install git \
    && pip install pre-commit \
    && useradd -u 1000 -m docker

USER docker
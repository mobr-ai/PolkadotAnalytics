# using the jena-fuseki Docker image
#     Alpine Linux
#     OpenJDK
#     Apache Jena

FROM python:3.9.13-alpine3.16

# setting metadata mobr as maintainer
LABEL maintainer="contact@mobr.ai"

RUN set -eux; \
    apk add --update --no-cache bash python3 wget && ln -sf python3 /usr/bin/python; \
    python3 -m ensurepip; \
    pip3 install --no-cache --upgrade pip setuptools; \
    rm -rf /var/cache/apk/*

# addressing our platform dependencies
RUN mkdir -p /usr/src/pap/

WORKDIR /usr/src/pap/
ADD . .
RUN pip install -r requirements.txt && \
    wget https://raw.githubusercontent.com/mobr-ai/POnto/main/src/flat/POnto.ttl

EXPOSE 80

WORKDIR /usr/src/pap/src

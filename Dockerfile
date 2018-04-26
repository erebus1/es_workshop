FROM chinsky/apollo_base:2.7.14-alpine3.6

RUN apk update && \
    apk add --virtual .build-dependencies dpkg tar strace wget && \
    mkdir -p /var/lib/dpkg && \
    touch /var/lib/dpkg/status && \
    apk add gettext && \
    apk del .build-dependencies
ADD requirements.txt requirements.txt
RUN apk update && \
    apk add --virtual .build-dependencies gcc musl-dev && \
    pip install --no-cache-dir -r requirements.txt && \
    apk del .build-dependencies
WORKDIR /project


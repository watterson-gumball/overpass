FROM ubuntu:24.04

ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get upgrade -y
RUN apt-get install -y \
    wget \
    g++ \
    make \
    expat \
    libexpat1-dev \
    zlib1g-dev \
    liblz4-dev \
    apache2 \
    vim

COPY data.osm /data.osm

COPY build.sh /build.sh
RUN chmod +x /build.sh
RUN /build.sh

COPY 000-default.conf /etc/apache2/sites-available/000-default.conf

COPY run.sh /run.sh
RUN chmod +x /run.sh

EXPOSE 80

ENTRYPOINT [ "/run.sh" ]
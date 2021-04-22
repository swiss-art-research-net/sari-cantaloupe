FROM python:3.8

RUN apt-get -qq update && \
    apt-get -q -y upgrade && \
    apt-get install -y sudo curl wget locales && \
    rm -rf /var/lib/apt/lists/*
RUN locale-gen en_US.UTF-8

RUN apt update
RUN apt install -y default-jre
# Install Python packages
RUN pip install urllib3 requests tqdm

# Prepare directories and volumes
RUN mkdir /data
RUN mkdir /images
RUN mkdir /scripts
VOLUME /data
VOLUME /images
WORKDIR /scripts

# Start ssh service on entry
ENTRYPOINT tail -f /dev/null
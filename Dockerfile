FROM python:3.8-slim

RUN apt-get update && \
    apt-get install -y --no-install-recommends git && \
    apt-get purge -y --auto-remove && \
    rm -rf /var/lib/apt/lists/*

WORKDIR .

ENV PYTHONUNBUFFERED 1

# install required packages
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# clone the repo
RUN git clone https://github.com/Snaptraks/physbot.git
WORKDIR physbot

# give permission to execute start script
RUN chmod +x start.docker.sh

# copy config files
COPY config.py ./
COPY lexique_physique_filtre.txt ./

# start the Bot
CMD ["./start.docker.sh"]

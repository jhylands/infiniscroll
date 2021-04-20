FROM ubuntu:latest

RUN apt update
RUN DEBIAN_FRONTEND="noninteractive"  apt install -y \
    npm \
    python3 \
    python3-pip
RUN apt-get install -y libmysqlclient-dev

RUN mkdir -p /home/app/
WORKDIR /home/app

COPY package.json /home/app/
COPY requirements.txt /home/app

RUN pip3 install -r requirements.txt;
RUN npm install

COPY server /home/app/server
COPY templates /home/app/templates
COPY db /home/app/db
COPY worker /home/app/worker
COPY neo /home/app/neo
COPY scraper /home/app/scraper
COPY webpack.config.js /home/app/

RUN cd /home/app/;npx webpack
ENV code=thebestpasswordintheworld
ENV PYTHONPATH=/home/app
ENTRYPOINT ["python3", "/home/app/server/server.py"]


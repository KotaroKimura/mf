FROM ubuntu:18.04

RUN mkdir -p /app
WORKDIR /app

RUN apt-get update \
  && apt-get -y install curl \
  && apt-get -y install python3 \
  && apt-get -y install python3-dev \
  && apt-get -y install python3-pip \
  && apt-get -y install libmysqlclient-dev

COPY requirements.txt /app/
RUN pip3 install -r requirements.txt

CMD ["/bin/sh", "/app/run.sh"]

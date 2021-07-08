FROM ubuntu:18.04

RUN apt-get update \
  && apt-get -y install curl \
  && apt-get -y install firefox \
  && apt-get -y install python3 \
  && apt-get -y install python3-pip \
  && apt-get -y install python3-dev \
  && apt-get -y install libmysqlclient-dev \
  && apt-get -y install locales \
  && apt-get -y install fonts-migmix

RUN curl -L "https://github.com/mozilla/geckodriver/releases/download/v0.23.0/geckodriver-v0.23.0-arm7hf.tar.gz" |tar zx -C /bin/
RUN echo "ja_JP UTF-8" > /etc/locale.gen && locale-gen

ENV LANG ja_JP.UTF-8
#ENV TZ Asia/Tokyo

ADD . /src/
WORKDIR /src

RUN pip3 install -r requirements.txt

CMD ["python3", "cron.py"]

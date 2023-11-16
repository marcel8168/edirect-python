FROM python:3.8
WORKDIR /data
COPY . /data

RUN bash edirect_installation.sh

CMD tail -f /dev/null
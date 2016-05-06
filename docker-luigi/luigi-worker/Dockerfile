# originally...
FROM phusion/baseimage:0.9.16
# see https://github.com/phusion/baseimage-docker

# try a newer image from alpine...
#FROM trota/alpine-python3.5.1
# https://github.com/docker-library/python/blob/master/3.5/alpine/Dockerfile

# try the same base as luigid
#FROM python:3-slim
# slim=debian-based

ENV LUIGI_HOME /etc/luigi
ENV APP_HOME /usr/local/app1

# update OS packages
RUN apt-get update && apt-get upgrade -y -o \
  Dpkg::Options::="--force-confold"

RUN apt-get update && \
  apt-get install -y build-essential python python-dev python-pip

#RUN apt-get update && apt-get install -y build-essential

RUN apt-get update && apt-get install -y libpq-dev gcc
# need gcc to compile cffi for parqamiko

RUN apt-get update && apt-get install -y libffi-dev

RUN apt-get install -y python-pip

RUN pip install --upgrade pip

ADD requirements.txt /tmp/requirements.txt
RUN pip install -r /tmp/requirements.txt

VOLUME /var/log/luigi

RUN mkdir $LUIGI_HOME
RUN mkdir $APP_HOME
ADD client.cfg $LUIGI_HOME/client.cfg
#COPY scripts $APP_HOME/scripts
#COPY workflows $APP_HOME/workflows

# remove the compiler we used for crpto requirement of paramiko 
#RUN apt-get autoremove -y gcc

#ENTRYPOINT ["/bin/bash", "-c"]
#CMD ["$APP_HOME/scripts/run.sh"]

CMD ["python2.7"]

#RUN apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*
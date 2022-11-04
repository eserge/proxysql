FROM --platform=linux/amd64 python:3.9.1

RUN apt update

RUN apt -y install libdbd-mysql-perl
RUN apt install inetutils-ping

COPY ../mha4mysql-node_0.54-0_all.deb .

RUN dpkg -i mha4mysql-node_0.54-0_all.deb

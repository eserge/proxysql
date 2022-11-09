FROM --platform=linux/amd64 python:3.9.1

RUN apt update

RUN apt -y install libdbi-perl \
    libdbd-mysql-perl \
    libconfig-tiny-perl \
    liblog-dispatch-perl \
    libparallel-forkmanager-perl \
    libnet-amazon-ec2-perl \
    inetutils-ping

# COPY ./mha4mysql-manager_0.55-0_all.deb .
# COPY ./mha4mysql-node_0.54-0_all.deb .

# RUN dpkg -i mha4mysql-node_0.54-0_all.deb
# RUN dpkg -i mha4mysql-manager_0.55-0_all.deb

RUN mkdir -p /etc/mha/ /var/log/mha/

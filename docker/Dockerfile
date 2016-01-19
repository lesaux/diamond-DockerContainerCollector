# Docker image containing the Diamond collector
#
# VERSION               0.0.1
FROM      ubuntu:14.04
MAINTAINER Pierig Le Saux <lesaux@pythian.com>

# Install dependencies
ENV DEBIAN_FRONTEND noninteractive
ENV HANDLERS diamond.handler.graphite.GraphiteHandler
ENV GRAPHITE_HOST 127.0.0.1
ENV GRAPHITE_PORT 2003
ENV STATSD_HOST 127.0.0.1
ENV STATSD_PORT 8125
ENV DOCKER_HOSTNAME docker-hostname
ENV INTERVAL 5

RUN apt-get update && \
    apt-get install -y python-setuptools make pbuilder python-mock python-configobj python-support cdbs git python-psutil && \
    easy_install statsd && \
    git clone https://github.com/python-diamond/Diamond.git && \
    git clone https://github.com/docker/docker-py.git && \
    git clone https://github.com/lesaux/diamond-DockerContainerCollector.git && \
    cd /Diamond && \
    make builddeb && \
    sudo dpkg -i build/diamond_*_all.deb && \
    sudo mkdir /usr/share/diamond/collectors/dockercontainer && \
    find /usr/share/diamond/collectors/  -type f -name "*.py" -print0 | xargs -0 sed -i 's/\/proc/\/host_proc/g' && \
    cd /docker-py && \
    python setup.py install && \
    cd /diamond-DockerContainerCollector && \
    sudo cp dockercontainer.py /usr/share/diamond/collectors/dockercontainer/ && \
    apt-get autoremove -y git make pbuilder python-mock python-pip && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* && \
    rm -rf /Diamond /diamond-DockerContainerCollector /docker-py && \
    rm -rf /etc/diamond

#add diamond config dir
ADD diamond /etc/diamond/

#startup script
ADD config_diamond.sh /config_diamond.sh
RUN chmod +x /config_diamond.sh

ADD entrypoint.sh /


#start
ENTRYPOINT ["/entrypoint.sh"]

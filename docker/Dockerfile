# Docker image containing the Diamond collector
#
# VERSION               0.0.1
FROM      ubuntu:14.04
MAINTAINER Pierig Le Saux <lesaux@pythian.com>

# Install dependencies
ENV DEBIAN_FRONTEND noninteractive
RUN apt-get update && \
    apt-get install -y python-setuptools make pbuilder python-mock python-configobj python-support cdbs git python-psutil

#git clone diamond, docker-py and the collector
RUN git clone https://github.com/python-diamond/Diamond.git
RUN git clone https://github.com/docker/docker-py.git
RUN git clone https://github.com/lesaux/diamond-DockerContainerCollector.git

#compile and install diamond
WORKDIR /Diamond
RUN make builddeb
RUN sudo dpkg -i build/diamond_*_all.deb
RUN sudo mkdir /usr/share/diamond/collectors/dockercontainer
RUN find /usr/share/diamond/collectors/  -type f -name "*.py" -print0 | xargs -0 sed -i 's/\/proc/\/host_proc/g'

#install docker-py
WORKDIR /docker-py
RUN python setup.py install

#add diamond-dockercontainercollector
WORKDIR /diamond-DockerContainerCollector
RUN sudo cp dockercontainer.py /usr/share/diamond/collectors/dockercontainer/

#cleanup
RUN apt-get autoremove -y git python-setuptools make pbuilder python-mock && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* && \
    rm -rf /Diamond /diamond-DockerContainerCollector /docker-py

#add diamond config dir
ADD diamond /etc/diamond/

#startup script
ADD entrypoint.sh /

#enviroment
ENV GRAPHITE_HOST 127.0.0.1
ENV GRAPHITE_PORT 2003
ENV DOCKER_HOSTNAME docker-hostname
ENV INTERVAL 5

#configure diamond with env
ADD config_diamond.sh /config_diamond.sh
RUN chmod +x /config_diamond.sh

#start
ENTRYPOINT ["/entrypoint.sh"]

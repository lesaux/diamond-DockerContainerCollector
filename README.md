# diamond-DockerContainerCollector
A diamond collector for docker containers

A docker container that will ship the host and container metrics to graphite.

Diamond collectors are modified to read host stats from /host_proc instead of proc.
The DockerContainerCollector uses docker-py to gather container metrics.

If you wish you test it out, a container is available on the docker hub: https://registry.hub.docker.com/u/lesaux/diamond-containercollector/

The following environment variables are being used to launch the container:
```
HANDLERS=Handlers to use (e.g: diamond.handler.stats_d.StatsdHandler, defaults to diamond.handler.graphite.GraphiteHandler)
GRAPHITE_HOST=the ip address of your graphite container.
GRAPHITE_PORT=the port graphite listens on.
STATSD_HOST=the ip address of your StatsD daemon.
STATSD_PORT=the port StatsD listens on.
DOCKER_HOSTNAME=the name of the docker host as you wish to see it in graphite.
INTERVAL=the interval at which you wish to ship metrics.
```
The docker hosts metrics will be in the servers.hostname graphite path.
The container metrics will be in the docker.hostname.containers graphite path.

```
docker run -i -e GRAPHITE_HOST=192.168.0.78 -e GRAPHITE_PORT=2003 -e DOCKER_HOSTNAME=docker-node1 -e INTERVAL=5 -v /proc:/host_proc:ro -v /var/run/docker.sock:/var/run/docker.sock:ro lesaux/diamond-containercollector
```

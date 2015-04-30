#!/usr/bin/env python

import argparse
import re
import os
import docker
import pdb
import threading
import collections
import diamond.collector
try:
    import json
except ImportError:
    import simplejson as json


class DockerContainerCollector(diamond.collector.Collector):

    def get_default_config_help(self):
        config_help = super(DockerContainerCollector, self).get_default_config_help()
        config_help.update({
            'none': 'no options atm',
        })
        return config_help

    def get_default_config(self):
        """
        Returns the default collector settings
        """
        config = super(DockerContainerCollector, self).get_default_config()
        config.update({
            'path':     'containers',
        })
        return config

    def flatten_dict(self,d):
        def items():
            for key, value in d.items():
                if isinstance(value, dict):
                    for subkey, subvalue in self.flatten_dict(value).items():
                        yield key + "." + subkey, subvalue
                else:
                    yield key, value
        return dict(items())


    def collect(self):
        def print_metric(cc,name):
            data = cc.stats(name)
            metrics = json.loads(data.next())
            #memory metrics
            self.memory = self.flatten_dict (metrics['memory_stats'])
            for key, value in self.memory.items():
                metric_name = name+".memory."+key
                self.publish_counter(metric_name, value)
            #cpu metrics
            self.cpu = self.flatten_dict (metrics['cpu_stats'])
            for key, value in self.cpu.items():
                #percpu_usage is a list, we'll deal with it after
                if type(value) == int:
                    metric_name = name+".cpu."+key
                    self.publish_counter(metric_name, value)
                #dealing with percpu_usage
                if type(value) == list:
                    self.length = len(value)
                    for i in range(self.length):
                        self.value = value
                        self.metric_name = name+".cpu."+key+str(i)
                        self.publish_counter(self.metric_name, self.value[i])
            #network metrics
            self.network = self.flatten_dict (metrics['network'])
            for key, value in self.network.items():
                metric_name = name+".network."+key
                self.publish_counter(metric_name, value)
            #blkio metrics
            self.blkio = self.flatten_dict (metrics['blkio_stats'])
            for key, value in self.blkio.items():
                metric_name = name+".blkio."+key
                self.publish_counter(metric_name, value)

        cc = docker.Client(base_url='unix://var/run/docker.sock', version='auto')
        dockernames=[i['Names'] for i in cc.containers()]
        threads = []

        for dname in dockernames:
            t = threading.Thread(target=print_metric, args=(cc,dname[0][1:]))
            threads.append(t)
            t.start()

        for thread in threads:
            thread.join()

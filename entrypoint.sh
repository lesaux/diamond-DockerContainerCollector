#!/bin/bash

/config_diamond.sh
/usr/local/bin/diamond -f --skip-pidfile -l -c /etc/diamond/diamond.conf

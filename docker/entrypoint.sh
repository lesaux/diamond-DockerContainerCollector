#!/bin/bash

/config_diamond.sh
diamond -f --skip-pidfile -c /etc/diamond/diamond.conf

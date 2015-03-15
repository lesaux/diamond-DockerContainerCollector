#!/bin/bash

/config_diamond.sh
diamond -f -l --skip-pidfile -c /etc/diamond/diamond.conf

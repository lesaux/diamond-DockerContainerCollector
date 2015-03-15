#!/bin/bash
set -e


#if [ "${GRAPHITE_HOST}" = "**ChangeMe**" ]; then
#    echo "=> No address of InfluxDB is specified!"
#    echo "=> Program terminated!"
#    exit 1
#fi

echo "=> Configuring Diamond"
sed -i -e "s/<--GRAPHITE_HOST-->/${GRAPHITE_HOST}/g" \
    -e "s/<--GRAPHITE_PORT-->/${GRAPHITE_PORT}/g" \
    -e "s/<--INTERVAL-->/${INTERVAL}/g" \
    -e "s/<--DOCKER_HOSTNAME-->/${DOCKER_HOSTNAME}/g" /etc/diamond/diamond.conf


echo "=> Done!"

#!/bin/bash
#
# Run this to rebuild and relaunch the docker image in prod
# To see changes made in dev be pushed to prod, this must be run
# after teh changes are pushed to git
#

if [ $# -ne 1 ]
  then
    echo "please provide me with one and only one argument, the path to your key.pem"
    echo "usage: ./redeploy.sh /path/to/key.pem"
    exit 1
fi

if [ ! -f $1 ]
  then
    echo "the argument provided was not a file!"
    echo "usage: ./redeploy.sh /path/to/key.pem"
    exit 1
fi

ssh -i ${1} ec2-user@54.218.41.173 "docker rm -f \$(docker ps -aq); \
docker rmi \$(docker images | grep '<none>' | awk '{print \$3}'); \
docker rmi \$(docker images | grep 'latest' | awk '{print \$3}'); \
docker build -t sbc-compare . && \
docker run -d -p=80:8080 sbc-compare"


echo "----------------------------------------------------"
echo "Loadbalancer: Setting up initial config"
echo "----------------------------------------------------"

set -x

cp fresh-config.cfg haproxy.cfg

docker rm -f haproxy

docker network create --driver=bridge mldep_net

set +x

echo "----------------------------------------------------"
echo "Loadbalancer: Starting within container 'haproxy'"
echo "----------------------------------------------------"

docker run -d --name haproxy --net mldep_net -v $(pwd):/usr/local/etc/haproxy:ro -p 80:80 -p 8404:8404 -p 6000:6000 haproxytech/haproxy-alpine:2.4

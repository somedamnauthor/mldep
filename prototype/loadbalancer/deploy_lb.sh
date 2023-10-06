echo "----------------------------------------------------"
echo "Loadbalancer: Setting up initial config"
echo "----------------------------------------------------"

if [ ${1} = "true" ]; then
    lb_perm_string="sudo"
else
    lb_perm_string=""
fi

set -x

cp fresh-config.cfg haproxy.cfg

$lb_perm_string docker rm -f haproxy

$lb_perm_string docker network create --driver=bridge mldep_net

set +x

echo "----------------------------------------------------"
echo "Loadbalancer: Starting within container 'haproxy'"
echo "----------------------------------------------------"

$lb_perm_string docker run -d --name haproxy --net mldep_net -v $(pwd):/usr/local/etc/haproxy:ro -p 80:80 -p 8404:8404 -p 6000:6000 haproxytech/haproxy-alpine:2.4
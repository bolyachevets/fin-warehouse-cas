#! /bin/sh
cd /opt/app-root
echo 'run ora2pg on nettle'
cat cas-data-puller.py | ssh -i ~/.ssh/rsa/id_rsa "$NETTLE_IP" python - "$ORA_CONF"
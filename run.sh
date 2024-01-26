#! /bin/sh
cd /opt/app-root
echo 'run ora2pg on nettle'
cat cas-data-puller.py | ssh nettle.bcgov python - ora2pg/ora2pg.conf

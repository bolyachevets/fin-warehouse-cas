#! /bin/sh
cd /opt/app-root
echo 'run ora2pg on nettle'
if [ "$PATCH_CONFIG" == true ]; then
  cat cas-patch-config.py | ssh -v -i ~/.ssh/rsa/id_rsa "$NETTLE_IP" python - "$ORA_CONF_UPDATE"
fi
cat cas-data-puller.py | ssh -v -i ~/.ssh/rsa/id_rsa "$NETTLE_IP" python - "$ORA_CONF_UPDATE"
mkdir -p /data/update
scp -i ~/.ssh/rsa/id_rsa "$NETTLE_IP":/dsk01/warehouse/* /data/update
ssh -i ~/.ssh/rsa/id_rsa "$NETTLE_IP" 'rm /dsk01/warehouse/*'
python cas-upsert-formatter.py

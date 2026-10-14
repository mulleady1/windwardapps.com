#!/usr/bin/env bash
# Deploy master to production: push, then pull + migrate + collectstatic + reload on the server.
set -euo pipefail

git push origin master

ssh wwa 'bash -s' <<'REMOTE'
set -euo pipefail
cd /var/www/windwardapps.com
echo "[deploy] pulling"
git pull --ff-only
echo "[deploy] installing requirements"
env/bin/pip install -q -r requirements.txt
echo "[deploy] migrating"
env/bin/python manage.py migrate --noinput
echo "[deploy] collecting static"
env/bin/python manage.py collectstatic --noinput | tail -1
echo "[deploy] reloading gunicorn"
kill -HUP "$(systemctl show -p MainPID --value windwardapps.com.service)"
sleep 3
code=$(curl -s -o /dev/null -w '%{http_code}' -H 'Host: windwardapps.com' http://127.0.0.1:9100/)
echo "[deploy] local gunicorn answered $code"
[ "$code" = "200" ]
REMOTE

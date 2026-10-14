echo "[deploy.sh] rsyncing files..."
rsync -avz --exclude='*.pyc' --exclude='__pycache__/' manage.py requirements.txt static app blog shared project wwa:/var/www/windwardapps.com/
echo "[deploy.sh] rsyncing files... done"

echo "[deploy.sh] restarting..."
ssh wwa "cd /var/www/windwardapps.com && ./restart.sh"
echo "[deploy.sh] restarting... done"

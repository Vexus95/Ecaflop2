# Infra for hr db

This is used to deploy the web application on 26 URLs
(from a.hr.dmerej.info to z.hr.dmerej.info)

Steps:

 * Create a new droplet on Digital Ocean
   (2 GB Memory / 60 GB Disk / AMS3 - Debian 12 x64)
 * Add authentification with your public key
 * Add `A` record form hr.dmerej.info with the public IPv4 address of the droplet
 * Add the same `A` record for `<group>.hr.dmerej.info`


* Copy tmux config

```
scp ~/.tmux.conf root@hr.dmerej.info:
``

```bash
ssh root@hr.dmerej.info
# Deploy nginx *before* deploying anything, because
# we need certbot to work
apt install \
  certbot \
  kakoune \
  kitty-terminfo \
  nginx \
  python-is-python3 \
  python3-poetry \
  python3-venv \
  rsync \
  tmux \
  tree \
# Create hr system user in `/srv/hr`
addgroup --system hr
adduser --system --home /srv/hr hr --ingroup hr

mkdir /srv/hr/.ssh
cp .ssh/authorized_keys /srv/hr/.ssh/
chown -Rc hr:hr /srv/hr
chsh -s /bin/bash hr
```

Make sure `curl <group>hr.dmerej.info` and `curl a.<grup>.hr.dmerej.info` both work -
and then *stop* nginx so that certbot can run in "standalone" mode:

```
ssh root@hr.dmerej.info
systemctl stop nginx
# For the top-level:
certbot certonly -d hr.dmerej.info --standalone
# For the group:
certbot certonly -d <group>.hr.dmerej.info --standalone
# For all teams:
certbot certonly -d a.<group>.hr.dmerej.info --standalone
```

Create folders for the group:

```
ssh hr@hr.dmerej.info
group=<group>
mkdir -p /var/log/hr/$group
mkdir -p /srv/hr/src/$group
mkdir -p /srv/hr/data/$group
mkdir -p /srv/hr/run/$group
```

Deploy sources for the backend:

```
python automation.py --group <group> deploy-backend --no-restart
```

Create poetry virtual envs for the group:

```bash
scp ~/.tmux.conf hr@hr.dmerej.info:
cd /srv/hr/src/<group>
python -m venv .venv
source .venv/bin/activate
export PYTHON_KEYRING_BACKEND=keyring.backends.null.Keyring
poetry install --sync --only main
poetry install --sync --only main
deactivate
```

```bash
python automation.py --group <group> reset-dbs
python automation.py --group <group> deploy-systemd
python automation.py --group <group> deploy-nginx
python automation.py --group <group> restart-backend
```

#!/bin/bash
###############################################################################
# artemis dev environment installer
# --------------------------------
# This script installs a artemis stack suitable for development. DO NOT run this
# on a system that you use for other purposes as it might delete important
# files, truncate your databases, and otherwise do mean things to you.
#
# By default, this script will install the artemis code in the current user's
# home directory and all of its dependencies (including libraries and database
# servers) at the system level. The installed artemis will expect to be visited
# on the domain "artemis.local" unless specified otherwise.  Configuring name
# resolution for the domain is expected to be done outside the installed
# environment (e.g. in your host machine's /etc/hosts file) and is not
# something this script handles.
#
# Several configuration options (listed in the "Configuration" section below)
# are overridable with environment variables. e.g.
#
#    sudo ARTEMIS_DOMAIN=example.com ./install/artemis.sh
#
###############################################################################

# load configuration
RUNDIR=$(dirname $0)
source $RUNDIR/install.cfg


###############################################################################
# Sanity Checks
###############################################################################
if [[ $EUID -ne 0 ]]; then
    echo "ERROR: Must be run with root privileges."
    exit 1
fi

if [[ -z "$ARTEMIS_USER" ]]; then
    # in a production install, you'd want the code to be owned by root and run
    # by a less privileged user. this script is intended to build a development
    # install, so we expect the owner to run the app and not be root.
    cat <<END
ERROR: You have not specified a user. This usually means you're running this
script directly as root. It is not recommended to run artemis as the root user.

Please create a user to run artemis and set the ARTEMIS_USER variable
appropriately.
END
    exit 1
fi

if [[ "amd64" != $(dpkg --print-architecture) ]]; then
    cat <<END
ERROR: This host is running the $(dpkg --print-architecture) architecture!

Because of the pre-built dependencies in our PPA, and some extra picky things
like ID generation in liveupdate, installing artemis is only supported on amd64
architectures.
END
    exit 1
fi

# seriously! these checks are here for a reason. the packages from the
# artemis ppa aren't built for anything but trusty (14.04) right now, so
# if you try and use this install script on another release you're gonna
# have a bad time.
source /etc/lsb-release
if [ "$DISTRIB_ID" != "Ubuntu" -o "$DISTRIB_RELEASE" != "14.04" ]; then
    echo "ERROR: Only Ubuntu 14.04 is supported."
    exit 1
fi

if [[ "2000000" -gt $(awk '/MemTotal/{print $2}' /proc/meminfo) ]]; then
    LOW_MEM_PROMPT="artemis requires at least 2GB of memory to work properly, continue anyway? [y/n] "
    read -er -n1 -p "$LOW_MEM_PROMPT" response
    if [[ "$response" != "y" ]]; then
      echo "Quitting."
      exit 1
    fi
fi

ARTEMIS_AVAILABLE_PLUGINS=""
for plugin in $ARTEMIS_PLUGINS; do
    if [ -d $ARTEMIS_SRC/$plugin ]; then
        if [[ -z "$ARTEMIS_PLUGINS" ]]; then
            ARTEMIS_AVAILABLE_PLUGINS+="$plugin"
        else
            ARTEMIS_AVAILABLE_PLUGINS+=" $plugin"
        fi
        echo "plugin $plugin found"
    else
        echo "plugin $plugin not found"
    fi
done

###############################################################################
# Install prerequisites
###############################################################################

# install primary packages
$RUNDIR/install_apt.sh

# install cassandra from datastax
$RUNDIR/install_cassandra.sh

# install zookeeper
$RUNDIR/install_zookeeper.sh

# install services (rabbitmq, postgres, memcached, etc.)
$RUNDIR/install_services.sh

# install rust (needed for Lemmy backend)
$RUNDIR/install_rust.sh

###############################################################################
# Install the artemis source repositories
###############################################################################
if [ ! -d $ARTEMIS_SRC ]; then
    mkdir -p $ARTEMIS_SRC
    chown $ARTEMIS_USER $ARTEMIS_SRC
fi

function copy_upstart {
    if [ -d ${1}/upstart ]; then
        cp ${1}/upstart/* /etc/init/
    fi
}

function clone_artemis_repo {
    local destination=$ARTEMIS_SRC/${1}
    local repository_url=https://github.com/${2}.git

    if [ ! -d $destination ]; then
        sudo -u $ARTEMIS_USER -H git clone $repository_url $destination
    fi

    copy_upstart $destination
}

function clone_artemis_service_repo {
    clone_artemis_repo $1 artemis/artemis-service-$1
}

clone_artemis_repo artemis artemis/artemis
clone_artemis_repo i18n artemis/artemis-i18n
clone_artemis_service_repo websockets
clone_artemis_service_repo activity

# clone or link lemmy backend
if [ ! -d $ARTEMIS_SRC/artemis-lemmy ]; then
    if [ -d /var/home/guesty/Documents/Coding\ Projects/artemis/artemis-lemmy ]; then
        # link to the existing lemmy source
        sudo -u $ARTEMIS_USER ln -sf /var/home/guesty/Documents/Coding\ Projects/artemis/artemis-lemmy $ARTEMIS_SRC/artemis-lemmy
        echo "Linked existing Lemmy source"
    else
        # clone lemmy source
        sudo -u $ARTEMIS_USER git clone https://github.com/LemmyNet/lemmy.git $ARTEMIS_SRC/artemis-lemmy
        echo "Cloned Lemmy source"
    fi
fi

###############################################################################
# Configure Services
###############################################################################

# Configure Cassandra
$RUNDIR/setup_cassandra.sh

# Configure PostgreSQL
$RUNDIR/setup_postgres.sh

# Configure mcrouter
$RUNDIR/setup_mcrouter.sh

# Configure RabbitMQ
$RUNDIR/setup_rabbitmq.sh

# Setup Lemmy backend
$RUNDIR/setup_lemmy.sh

###############################################################################
# Install and configure the artemis code
###############################################################################
function install_artemis_repo {
    pushd $ARTEMIS_SRC/$1
    sudo -u $ARTEMIS_USER python setup.py build
    python setup.py develop --no-deps
    popd
}

install_artemis_repo artemis/r2
install_artemis_repo i18n
for plugin in $ARTEMIS_AVAILABLE_PLUGINS; do
    copy_upstart $ARTEMIS_SRC/$plugin
    install_artemis_repo $plugin
done
install_artemis_repo websockets
install_artemis_repo activity

# install lemmy backend
$RUNDIR/install_lemmy.sh

# generate binary translation files from source
sudo -u $ARTEMIS_USER make -C $ARTEMIS_SRC/i18n clean all

# this builds static files and should be run *after* languages are installed
# so that the proper language-specific static files can be generated and after
# plugins are installed so all the static files are available.
pushd $ARTEMIS_SRC/artemis/r2
sudo -u $ARTEMIS_USER make clean pyx

plugin_str=$(echo -n "$ARTEMIS_AVAILABLE_PLUGINS" | tr " " ,)
if [ ! -f development.update ]; then
    cat > development.update <<DEVELOPMENT
# after editing this file, run "make ini" to
# generate a new development.ini

[DEFAULT]
# global debug flag -- displays pylons stacktrace rather than 500 page on error when true
# WARNING: a pylons stacktrace allows remote code execution. Make sure this is false
# if your server is publicly accessible.
debug = true

disable_ads = true
disable_captcha = true
disable_ratelimit = true
disable_require_admin_otp = true

domain = $ARTEMIS_DOMAIN
oauth_domain = $ARTEMIS_DOMAIN

plugins = $plugin_str

media_provider = filesystem
media_fs_root = /srv/www/media
media_fs_base_url_http = http://%(domain)s/media/

[server:main]
port = 8001
DEVELOPMENT
    chown $ARTEMIS_USER development.update
else
    sed -i "s/^plugins = .*$/plugins = $plugin_str/" $ARTEMIS_SRC/artemis/r2/development.update
    sed -i "s/^domain = .*$/domain = $ARTEMIS_DOMAIN/" $ARTEMIS_SRC/artemis/r2/development.update
    sed -i "s/^oauth_domain = .*$/oauth_domain = $ARTEMIS_DOMAIN/" $ARTEMIS_SRC/artemis/r2/development.update
fi

sudo -u $ARTEMIS_USER make ini

if [ ! -L run.ini ]; then
    sudo -u $ARTEMIS_USER ln -nsf development.ini run.ini
fi

popd

###############################################################################
# some useful helper scripts
###############################################################################
function helper-script() {
    cat > $1
    chmod 755 $1
}

helper-script /usr/local/bin/artemis-run <<ARTEMISRUN
#!/bin/bash
exec paster --plugin=r2 run $ARTEMIS_SRC/artemis/r2/run.ini "\$@"
ARTEMISRUN

helper-script /usr/local/bin/artemis-shell <<ARTEMISSHELL
#!/bin/bash
exec paster --plugin=r2 shell $ARTEMIS_SRC/artemis/r2/run.ini
ARTEMISSHELL

helper-script /usr/local/bin/artemis-start <<ARTEMISSTART
#!/bin/bash
initctl emit artemis-start
ARTEMISSTART

helper-script /usr/local/bin/artemis-stop <<ARTEMISSTOP
#!/bin/bash
initctl emit artemis-stop
ARTEMISSTOP

helper-script /usr/local/bin/artemis-restart <<ARTEMISRESTART
#!/bin/bash
initctl emit artemis-restart TARGET=${1:-all}
ARTEMISRESTART

helper-script /usr/local/bin/lemmy-start <<LEMMYSTART
#!/bin/bash
initctl emit artemis-lemmy-start
LEMMYSTART

helper-script /usr/local/bin/lemmy-stop <<LEMMYSTOP
#!/bin/bash
initctl emit artemis-lemmy-stop
LEMMYSTOP

helper-script /usr/local/bin/lemmy-restart <<LEMMYRESTART
#!/bin/bash
initctl emit artemis-restart TARGET=lemmy
LEMMYRESTART

helper-script /usr/local/bin/artemis-flush <<ARTEMISFLUSH
#!/bin/bash
echo flush_all | nc localhost 11211
ARTEMISFLUSH

helper-script /usr/local/bin/artemis-serve <<ARTEMISSERVE
#!/bin/bash
exec paster serve --reload $ARTEMIS_SRC/artemis/r2/run.ini
ARTEMISSERVE

###############################################################################
# pixel and click server
###############################################################################
mkdir -p /var/opt/artemis/
chown $ARTEMIS_USER:$ARTEMIS_GROUP /var/opt/artemis/

mkdir -p /srv/www/pixel
chown $ARTEMIS_USER:$ARTEMIS_GROUP /srv/www/pixel
cp $ARTEMIS_SRC/artemis/r2/r2/public/static/pixel.png /srv/www/pixel

if [ ! -f /etc/gunicorn.d/click.conf ]; then
    cat > /etc/gunicorn.d/click.conf <<CLICK
CONFIG = {
    "mode": "wsgi",
    "working_dir": "$ARTEMIS_SRC/artemis/scripts",
    "user": "$ARTEMIS_USER",
    "group": "$ARTEMIS_USER",
    "args": (
        "--bind=unix:/var/opt/artemis/click.sock",
        "--workers=1",
        "tracker:application",
    ),
}
CLICK
fi

service gunicorn start

###############################################################################
# nginx
###############################################################################

mkdir -p /srv/www/media
chown $ARTEMIS_USER:$ARTEMIS_GROUP /srv/www/media

cat > /etc/nginx/sites-available/artemis-media <<MEDIA
server {
    listen 9000;

    expires max;

    location /media/ {
        alias /srv/www/media/;
    }
}
MEDIA

cat > /etc/nginx/sites-available/artemis-pixel <<PIXEL
upstream click_server {
  server unix:/var/opt/artemis/click.sock fail_timeout=0;
}

server {
  listen 8082;

  log_format directlog '\$remote_addr - \$remote_user [\$time_local] '
                      '"\$request_method \$request_uri \$server_protocol" \$status \$body_bytes_sent '
                      '"\$http_referer" "\$http_user_agent"';
  access_log      /var/log/nginx/traffic/traffic.log directlog;

  location / {

    rewrite ^/pixel/of_ /pixel.png;

    add_header Last-Modified "";
    add_header Pragma "no-cache";

    expires -1;
    root /srv/www/pixel/;
  }

  location /click {
    proxy_pass http://click_server;
  }
}
PIXEL

cat > /etc/nginx/sites-available/artemis-ssl <<SSL
map \$http_upgrade \$connection_upgrade {
  default upgrade;
  ''      close;
}

server {
    listen 443;

    ssl on;
    ssl_certificate /etc/ssl/certs/ssl-cert-snakeoil.pem;
    ssl_certificate_key /etc/ssl/private/ssl-cert-snakeoil.key;

    ssl_protocols TLSv1 TLSv1.1 TLSv1.2;
    ssl_ciphers EECDH+AES128:RSA+AES128:EECDH+AES256:RSA+AES256:EECDH+3DES:RSA+3DES:!MD5;
    ssl_prefer_server_ciphers on;

    ssl_session_cache shared:SSL:1m;

    location / {
        proxy_pass http://127.0.0.1:8080;
        proxy_set_header Host \$http_host;
        proxy_http_version 1.1;
        proxy_set_header X-Forwarded-For \$remote_addr;
        proxy_pass_header Server;

        # allow websockets through if desired
        proxy_set_header Upgrade \$http_upgrade;
        proxy_set_header Connection \$connection_upgrade;
    }
}
SSL

# remove the default nginx site that may conflict with haproxy
rm -rf /etc/nginx/sites-enabled/default
# put our config in place
ln -nsf /etc/nginx/sites-available/artemis-media /etc/nginx/sites-enabled/
ln -nsf /etc/nginx/sites-available/artemis-pixel /etc/nginx/sites-enabled/
ln -nsf /etc/nginx/sites-available/artemis-ssl /etc/nginx/sites-enabled/

# make the pixel log directory
mkdir -p /var/log/nginx/traffic

# link the ini file for the Flask click tracker
ln -nsf $ARTEMIS_SRC/artemis/r2/development.ini $ARTEMIS_SRC/artemis/scripts/production.ini

service nginx restart

###############################################################################
# haproxy
###############################################################################
if [ -e /etc/haproxy/haproxy.cfg ]; then
    BACKUP_HAPROXY=$(mktemp /etc/haproxy/haproxy.cfg.XXX)
    echo "Backing up /etc/haproxy/haproxy.cfg to $BACKUP_HAPROXY"
    cat /etc/haproxy/haproxy.cfg > $BACKUP_HAPROXY
fi

# make sure haproxy is enabled
cat > /etc/default/haproxy <<DEFAULT
ENABLED=1
DEFAULT

# configure haproxy
cat > /etc/haproxy/haproxy.cfg <<HAPROXY
global
    maxconn 350

frontend frontend
    mode http

    bind 0.0.0.0:80
    bind 127.0.0.1:8080

    timeout client 24h
    option forwardfor except 127.0.0.1
    option httpclose

    # make sure that requests have x-forwarded-proto: https iff tls
    reqidel ^X-Forwarded-Proto:.*
    acl is-ssl dst_port 8080
    reqadd X-Forwarded-Proto:\ https if is-ssl

    # send websockets to the websocket service
    acl is-websocket hdr(Upgrade) -i WebSocket
    use_backend websockets if is-websocket

    # send media stuff to the local nginx
    acl is-media path_beg /media/
    use_backend media if is-media

    # send pixel stuff to local nginx
    acl is-pixel path_beg /pixel/
    acl is-click path_beg /click
    use_backend pixel if is-pixel || is-click

    # send lemmy api requests to lemmy backend
    acl is-lemmy-api path_beg /api/ v3/
    acl is-lemmy-api path_beg /lemmy/
    use_backend lemmy if is-lemmy-api

    default_backend artemis

backend artemis
    mode http
    timeout connect 4000
    timeout server 30000
    timeout queue 60000
    balance roundrobin

    server app01-8001 localhost:8001 maxconn 30

backend websockets
    mode http
    timeout connect 4s
    timeout server 24h
    balance roundrobin

    server websockets localhost:9001 maxconn 250

backend media
    mode http
    timeout connect 4000
    timeout server 30000
    timeout queue 60000
    balance roundrobin

    server nginx localhost:9000 maxconn 20

backend pixel
    mode http
    timeout connect 4000
    timeout server 30000
    timeout queue 60000
    balance roundrobin

    server nginx localhost:8082 maxconn 20

backend lemmy
    mode http
    timeout connect 4000
    timeout server 30000
    timeout queue 60000
    balance roundrobin

    server lemmy localhost:8536 maxconn 30
HAPROXY

# this will start it even if currently stopped
service haproxy restart

###############################################################################
# websocket service
###############################################################################

if [ ! -f /etc/init/artemis-websockets.conf ]; then
    cat > /etc/init/artemis-websockets.conf << UPSTART_WEBSOCKETS
description "websockets service"

stop on runlevel [!2345] or artemis-restart all or artemis-restart websockets
start on runlevel [2345] or artemis-restart all or artemis-restart websockets

respawn
respawn limit 10 5
kill timeout 15

limit nofile 65535 65535

exec baseplate-serve2 --bind localhost:9001 $ARTEMIS_SRC/websockets/example.ini
UPSTART_WEBSOCKETS
fi

service artemis-websockets restart

###############################################################################
# activity service
###############################################################################

if [ ! -f /etc/init/artemis-activity.conf ]; then
    cat > /etc/init/artemis-activity.conf << UPSTART_ACTIVITY
description "activity service"

stop on runlevel [!2345] or artemis-restart all or artemis-restart activity
start on runlevel [2345] or artemis-restart all or artemis-restart activity

respawn
respawn limit 10 5
kill timeout 15

exec baseplate-serve2 --bind localhost:9002 $ARTEMIS_SRC/activity/example.ini
UPSTART_ACTIVITY
fi

service artemis-activity restart

###############################################################################
# lemmy backend service
###############################################################################

if [ ! -f /etc/init/artemis-lemmy.conf ]; then
    cat > /etc/init/artemis-lemmy.conf << UPSTART_LEMMY
description "lemmy backend service"

stop on runlevel [!2345] or artemis-restart all or artemis-restart lemmy
start on runlevel [2345] or artemis-restart all or artemis-restart lemmy

respawn
respawn limit 10 5
kill timeout 15

env LEMMY_CONFIG=/etc/lemmy/config.hjson

exec /usr/local/bin/lemmy-server -c \$LEMMY_CONFIG
UPSTART_LEMMY
fi

# create lemmy config if it doesn't exist
if [ ! -f /etc/lemmy/config.hjson ]; then
    mkdir -p /etc/lemmy
    cat > /etc/lemmy/config.hjson <<LEMMY_CONFIG
{
  database: {
    uri: "postgres://lemmy:password@localhost:5432/lemmy"
  }
  hostname: "localhost"
  bind: "127.0.0.1:8536"
  tls: {
    enabled: false
  }
  setup: {
    admin_username: "admin"
    admin_password: "password"
    admin_email: "admin@example.com"
    site_name: "Artemis Lemmy"
  }
}
LEMMY_CONFIG
    chown -R $ARTEMIS_USER:$ARTEMIS_GROUP /etc/lemmy
fi

service artemis-lemmy restart

###############################################################################
# geoip service
###############################################################################
if [ ! -f /etc/gunicorn.d/geoip.conf ]; then
    cat > /etc/gunicorn.d/geoip.conf <<GEOIP
CONFIG = {
    "mode": "wsgi",
    "working_dir": "$ARTEMIS_SRC/artemis/scripts",
    "user": "$ARTEMIS_USER",
    "group": "$ARTEMIS_USER",
    "args": (
        "--bind=127.0.0.1:5000",
        "--workers=1",
         "--limit-request-line=8190",
         "geoip_service:application",
    ),
}
GEOIP
fi

service gunicorn start

###############################################################################
# Job Environment
###############################################################################
CONSUMER_CONFIG_ROOT=$ARTEMIS_HOME/consumer-count.d

if [ ! -f /etc/default/artemis ]; then
    cat > /etc/default/artemis <<DEFAULT
export ARTEMIS_ROOT=$ARTEMIS_SRC/artemis/r2
export ARTEMIS_INI=$ARTEMIS_SRC/artemis/r2/run.ini
export ARTEMIS_USER=$ARTEMIS_USER
export ARTEMIS_GROUP=$ARTEMIS_GROUP
export ARTEMIS_CONSUMER_CONFIG=$CONSUMER_CONFIG_ROOT
alias wrap-job=$ARTEMIS_SRC/artemis/scripts/wrap-job
alias manage-consumers=$ARTEMIS_SRC/artemis/scripts/manage-consumers
DEFAULT
fi

###############################################################################
# Queue Processors
###############################################################################
mkdir -p $CONSUMER_CONFIG_ROOT

function set_consumer_count {
    if [ ! -f $CONSUMER_CONFIG_ROOT/$1 ]; then
        echo $2 > $CONSUMER_CONFIG_ROOT/$1
    fi
}

set_consumer_count search_q 0
set_consumer_count del_account_q 1
set_consumer_count scraper_q 1
set_consumer_count markread_q 1
set_consumer_count commentstree_q 1
set_consumer_count newcomments_q 1
set_consumer_count vote_link_q 1
set_consumer_count vote_comment_q 1
set_consumer_count automoderator_q 0
set_consumer_count butler_q 1
set_consumer_count author_query_q 1
set_consumer_count branch_query_q 1
set_consumer_count domain_query_q 1

chown -R $ARTEMIS_USER:$ARTEMIS_GROUP $CONSUMER_CONFIG_ROOT/

###############################################################################
# Complete plugin setup, if setup.sh exists
###############################################################################
for plugin in $ARTEMIS_AVAILABLE_PLUGINS; do
    if [ -x $ARTEMIS_SRC/$plugin/setup.sh ]; then
        echo "Found setup.sh for $plugin; running setup script"
        $ARTEMIS_SRC/$plugin/setup.sh $ARTEMIS_SRC $ARTEMIS_USER
    fi
done

###############################################################################
# Start everything up
###############################################################################

# the initial database setup should be done by one process rather than a bunch
# vying with eachother to get there first
artemis-run -c 'print "ok done"'

# ok, now start everything else up
initctl emit artemis-stop
initctl emit artemis-start

###############################################################################
# Cron Jobs
###############################################################################
if [ ! -f /etc/cron.d/artemis ]; then
    cat > /etc/cron.d/artemis <<CRON
0    3 * * * root /sbin/start --quiet artemis-job-update_sr_names
30  16 * * * root /sbin/start --quiet artemis-job-update_branches
0    * * * * root /sbin/start --quiet artemis-job-update_promos
*/5  * * * * root /sbin/start --quiet artemis-job-clean_up_hardcache
*/2  * * * * root /sbin/start --quiet artemis-job-broken_things
*/2  * * * * root /sbin/start --quiet artemis-job-rising
0    * * * * root /sbin/start --quiet artemis-job-trylater

# liveupdate
*    * * * * root /sbin/start --quiet artemis-job-liveupdate_activity

# jobs that recalculate time-limited listings (e.g. top this year)
PGPASSWORD=password
*/15 * * * * $ARTEMIS_USER $ARTEMIS_SRC/artemis/scripts/compute_time_listings link year "['hour', 'day', 'week', 'month', 'year']"
*/15 * * * * $ARTEMIS_USER $ARTEMIS_SRC/artemis/scripts/compute_time_listings comment year "['hour', 'day', 'week', 'month', 'year']"

# disabled by default, uncomment if you need these jobs
#*    * * * * root /sbin/start --quiet artemis-job-email
#0    0 * * * root /sbin/start --quiet artemis-job-update_gold_users
CRON
fi

###############################################################################
# Finished with install script
###############################################################################
# print this out here. if vagrant's involved, it's gonna do more steps
# afterwards and then re-run this script but that's ok.
$RUNDIR/done.sh

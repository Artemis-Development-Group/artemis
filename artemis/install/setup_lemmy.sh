#!/bin/bash
###############################################################################
# Lemmy backend setup script
# Ensures Rust 1.75 is used for Ubuntu 14.04 compatibility
###############################################################################

# load configuration
RUNDIR=$(dirname $0)
source $RUNDIR/install.cfg

echo "Setting up Lemmy backend..."

# source cargo environment
if [ -f /home/$ARTEMIS_USER/.cargo/env ]; then
    source /home/$ARTEMIS_USER/.cargo/env
fi

# ensure rust 1.75 is being used
if command -v rustc &> /dev/null; then
    CURRENT_VERSION=$(rustc --version | grep -oP 'rustc \K[0-9.]+')
    if [[ "$CURRENT_VERSION" != "1.75.0" ]]; then
        echo "Switching to Rust 1.75.0 (current: $CURRENT_VERSION)"
        sudo -u $ARTEMIS_USER bash -c "source /home/$ARTEMIS_USER/.cargo/env && rustup default 1.75.0"
    fi
else
    echo "ERROR: Rust not found. Please run install_rust.sh first."
    exit 1
fi

# verify rust version
RUST_VERSION=$(sudo -u $ARTEMIS_USER bash -c "source /home/$ARTEMIS_USER/.cargo/env && rustc --version")
echo "Using: $RUST_VERSION"

# build lemmy backend if not already built
if [ ! -d $ARTEMIS_SRC/artemis-lemmy ]; then
    echo "Lemmy source not found at $ARTEMIS_SRC/artemis-lemmy"
    exit 1
fi

# create lemmy configuration directory
mkdir -p /etc/lemmy
chown $ARTEMIS_USER:$ARTEMIS_GROUP /etc/lemmy

# create lemmy database
SQL="SELECT COUNT(1) FROM pg_catalog.pg_database WHERE datname = 'lemmy';"
IS_DATABASE_CREATED=$(sudo -u postgres psql -t -c "$SQL")

if [ $IS_DATABASE_CREATED -ne 1 ]; then
    sudo -u postgres psql <<LEMMYDB
CREATE DATABASE lemmy WITH ENCODING = 'utf8' TEMPLATE template0 LC_COLLATE='en_US.utf8' LC_CTYPE='en_US.utf8';
CREATE USER lemmy WITH PASSWORD 'password';
GRANT ALL PRIVILEGES ON DATABASE lemmy TO lemmy;
LEMMYDB
    echo "Lemmy database created"
else
    echo "Lemmy database already exists"
fi

# run lemmy database migrations
cd $ARTEMIS_SRC/artemis-lemmy
sudo -u $ARTEMIS_USER bash -c "source /home/$ARTEMIS_USER/.cargo/env && cargo install diesel_cli --no-default-features --features postgres"
sudo -u $ARTEMIS_USER bash -c "source /home/$ARTEMIS_USER/.cargo/env && cd $ARTEMIS_SRC/artemis-lemmy && diesel migration run --database-url postgres://lemmy:password@localhost/lemmy"

echo "Lemmy backend setup complete"

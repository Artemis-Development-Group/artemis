#!/bin/bash
###############################################################################
# Lemmy backend installation script
# Uses Rust 1.75 for Ubuntu 14.04 compatibility
###############################################################################

# load configuration
RUNDIR=$(dirname $0)
source $RUNDIR/install.cfg

echo "Installing Lemmy backend with Rust 1.75 for Ubuntu 14.04..."

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
echo "Building with: $RUST_VERSION"

# check if lemmy source exists
if [ ! -d $ARTEMIS_SRC/artemis-lemmy ]; then
    echo "Lemmy source not found at $ARTEMIS_SRC/artemis-lemmy"
    echo "Please ensure Lemmy source is available before running this script"
    exit 1
fi

# build lemmy backend with rust 1.75
cd $ARTEMIS_SRC/artemis-lemmy
sudo -u $ARTEMIS_USER bash -c "source /home/$ARTEMIS_USER/.cargo/env && cargo build --release"

# create symlink for lemmy binary
if [ -f $ARTEMIS_SRC/artemis-lemmy/target/release/lemmy_server ]; then
    ln -sf $ARTEMIS_SRC/artemis-lemmy/target/release/lemmy_server /usr/local/bin/lemmy-server
    chmod +x /usr/local/bin/lemmy-server
    echo "Lemmy server binary installed"
else
    echo "ERROR: lemmy_server binary not found after build"
    exit 1
fi

echo "Lemmy backend installation complete"

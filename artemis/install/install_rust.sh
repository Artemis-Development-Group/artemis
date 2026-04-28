#!/bin/bash
###############################################################################
# Rust installation script for Lemmy backend
# Installs Rust 1.75 specifically for Ubuntu 14.04 compatibility
###############################################################################

# load configuration
RUNDIR=$(dirname $0)
source $RUNDIR/install.cfg

echo "Installing Rust 1.75 for Lemmy backend..."

# install rust 1.75 using rustup
if ! command -v rustc &> /dev/null; then
    sudo -u $ARTEMIS_USER curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sudo -u $ARTEMIS_USER sh -s -- -y --default-toolchain 1.75.0
    # source cargo environment
    source /home/$ARTEMIS_USER/.cargo/env
    # verify version
    sudo -u $ARTEMIS_USER bash -c "source /home/$ARTEMIS_USER/.cargo/env && rustc --version"
    echo "Rust 1.75 installed successfully"
else
    # check if correct version is installed
    CURRENT_VERSION=$(rustc --version | grep -oP 'rustc \K[0-9.]+')
    if [[ "$CURRENT_VERSION" != "1.75.0" ]]; then
        echo "Installing Rust 1.75.0 (current: $CURRENT_VERSION)"
        sudo -u $ARTEMIS_USER bash -c "source /home/$ARTEMIS_USER/.cargo/env && rustup install 1.75.0 && rustup default 1.75.0"
    else
        echo "Rust 1.75 already installed"
    fi
fi

# source cargo environment
if [ -f /home/$ARTEMIS_USER/.cargo/env ]; then
    source /home/$ARTEMIS_USER/.cargo/env
fi

# install additional tools needed for Lemmy
apt-get install -y protobuf-compiler libssl-dev pkg-config

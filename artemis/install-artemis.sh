#!/bin/bash
###############################################################################
# Artemis dev environment installer (light wrapper)
# -----------------------------------------------
# Minimal wrapper around install/artemis.sh
###############################################################################

set -e

echo "#######################################################################"
echo "# Artemis Installer by OmegaAOL - WARNING"
echo "#######################################################################"
echo
echo "This script will run install/artemis.sh with your current config."
echo "It assumes:"
echo "  - install/install.cfg exists and is correct"
echo "  - all required install scripts are present"
echo "  - system layout (paths, users, services) is already valid"
echo
echo "DO NOT run this on a system you care about without understanding the potential repercussions."
echo

read -rp "Proceed? [Y/n]: " response
if [[ "$response" =~ ^[Nn]$ ]]; then
    echo "Aborted."
    exit 1
fi

echo
echo "Loading configuration..."
source install/install.cfg

echo "Running Artemis installer..."
bash install/artemis.sh

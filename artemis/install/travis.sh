#!/bin/bash
# The contents of this file are subject to the Common Public Attribution
# License Version 1.0. (the "License"); you may not use this file except in
# compliance with the License. You may obtain a copy of the License at
# http://code.reddit.com/LICENSE. The License is based on the Mozilla Public
# License Version 1.1, but Sections 14 and 15 have been added to cover use of
# software over a computer network and provide for limited attribution for the
# Original Developer. In addition, Exhibit A has been modified to be consistent
# with Exhibit B.
#
# Software distributed under the License is distributed on an "AS IS" basis,
# WITHOUT WARRANTY OF ANY KIND, either express or implied. See the License for
# the specific language governing rights and limitations under the License.
#
# The Original Code is artemis.
#
# The Original Developer is the Initial Developer.  The Initial Developer of
# the Original Code is artemis Inc.
#
# All portions of the code written by artemis are Copyright (c) 2006-2015 artemis
# Inc. All Rights Reserved.
###############################################################################

###############################################################################
# artemis travis environment installer
# -----------------------------------
# This script installs a artemis stack suitable for running on travis-ci.
# As such, this is a minimal build to allow for running "nosetests"
# and not much more.
###############################################################################

# load configuration
RUNDIR=$(dirname $0)
source $RUNDIR/install.cfg

# who is running me (expects "travis" or "vagrant")
ENVIRONMENT=${1:-travis}

# the root directory to base the install in. must exist already
ARTEMIS_CODE=${2:-$ARTEMIS_SRC/artemis}

if [ ! -e $ARTEMIS_CODE ]; then
    echo "Couldn't find source $ARTEMIS_CODE. Aborting"
    exit 1
fi

###############################################################################
# Sanity Checks
###############################################################################
if [[ $EUID -ne 0 ]]; then
    echo "ERROR: Must be run with root privileges."
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

###############################################################################
# Install prerequisites
###############################################################################
$RUNDIR/install_apt.sh

$RUNDIR/install_cassandra.sh
$RUNDIR/install_zookeeper.sh

###############################################################################
# Install and configure the artemis code
###############################################################################

[ -x "$(which pip)" ] || easy_install pip
pip install -U pip wheel setuptools coverage
pushd $ARTEMIS_CODE/r2
sudo python setup.py build
python setup.py develop
make
ln -sf example.ini test.ini
popd

###############################################################################
# Install services (for local testing only!)
# NB: this is otherwise handled in the .travis.yml in before_script
###############################################################################
if [ "$ENVIRONMENT" == "vagrant" ]; then
    # install services (cassandra, postgres, etc.)
    $RUNDIR/install_services.sh
    # travis doesn't have mcrouter as a possible service, so we need to
    # be able to test without that running
    service mcrouter stop
    # Configure PostgreSQL
    $RUNDIR/setup_postgres.sh
    # Configure Cassandra
    $RUNDIR/setup_cassandra.sh
    # Configure RabbitMQ
    $RUNDIR/setup_rabbitmq.sh
fi

###############################################################################
# All done!
###############################################################################
cat <<CONCLUSION

Congratulations! A base version of artemis is now installed.  To run the
unit tests:

    cd src/artemis/r2
    nosetests

CONCLUSION

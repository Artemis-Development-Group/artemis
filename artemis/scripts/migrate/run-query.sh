#!/bin/bash

set -x
psql -h ${DB_HOST:-localhost} \
     -d ${DB_NAME:-artemis} \
     -U ${DB_USER:-artemis} \
     -p ${DB_PORT:-5432} \
     -F"\t" -A -t

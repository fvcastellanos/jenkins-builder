#!/bin/bash

set -eu

# configuring slave node [REQUIRED]
python -u /var/lib/jenkins/configure_jenkins_slave_node.py

exec "$@"

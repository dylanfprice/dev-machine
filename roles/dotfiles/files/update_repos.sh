#!/bin/bash 

. $HOME/.es_bashrc

cd $ENERGYSAVVY_DIR/deployment
hg pull -u

cd $ENERGYSAVVY_DIR/release
hg pull -u

cd $ENERGYSAVVY_DIR/ansible
hg pull -u

cd $ENERGYSAVVY_DIR/mainrepo
hg pull -u


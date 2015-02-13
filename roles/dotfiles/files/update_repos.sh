#!/bin/bash 

. $HOME/.es_bashrc

cd $ENERGYSAVVY_DIR/deployment
hg fetch

cd $ENERGYSAVVY_DIR/provisioning
hg fetch


#!/bin/bash 

. $HOME/.es_bashrc

ctags -f $ENERGYSAVVY_DIR/package-tags -R $ENERGYSAVVY_DIR/energysavvy_venv/lib/python2.7/ 2>/dev/null 
ctags --exclude='node_modules' --exclude='migrations' -f $ENERGYSAVVY_DIR/optix-tags -R $ENERGYSAVVY_DIR/mainrepo/ 2>/dev/null 

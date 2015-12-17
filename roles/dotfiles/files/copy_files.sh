#!/bin/bash 

. $HOME/.es_bashrc

mkdir -p $ENERGYSAVVY_DIR/config_files/

devstack cp /etc/pip.conf /vagrant/config_files/
devstack cp /home/django/.config/flake8 /vagrant/config_files/

cp $ENERGYSAVVY_DIR/config_files/pip.conf ${ENERGYSAVVY_VENV}/pip.conf
cp $ENERGYSAVVY_DIR/config_files/flake8 $HOME/.config/flake8

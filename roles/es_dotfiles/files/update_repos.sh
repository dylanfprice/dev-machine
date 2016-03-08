#!/bin/bash 

. $HOME/.es_bashrc

cd $ENERGYSAVVY_DIR
repos=$(ag --hidden -g '.hg/hgrc')

for repo in $repos; do
  cd ${repo%.hg/hgrc} && hg pull -u
  cd $ENERGYSAVVY_DIR
done

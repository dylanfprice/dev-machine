#!/bin/bash 

echo 'installing ansible'
sudo apt-add-repository ppa:ansible/ansible
sudo apt-get update
sudo apt-get install ansible

echo '\nmake sure you have an ssh key, and pushed it to github and bitbucket' 
read

echo 'create a new gnome terminal profile with the name "Default"'
read

echo 'log in to chromium account and sync add-ons'
read

echo 'energysavvy: you will need to copy pip.conf file to host machine'
read

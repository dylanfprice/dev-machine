#!/bin/bash

echo 'installing ansible'
sudo apt-add-repository ppa:ansible/ansible
sudo apt-get update
sudo apt-get install ansible
sudo ansible-galaxy install -r requirements.yml

echo '\nmake sure you have an ssh key, and pushed it to github and bitbucket'

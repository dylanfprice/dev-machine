#!/bin/bash

echo 'installing ansible'
sudo apt-get install software-properties-common
sudo apt-add-repository ppa:ansible/ansible
sudo apt-get update
sudo apt-get install ansible

echo '\nmake sure you have an ssh key, and pushed it to github and bitbucket'

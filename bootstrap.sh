#!/bin/bash 

echo 'disabling graphical boot'
sudo systemctl disable display-manager.service
sudo systemctl set-default multi-user.target

echo 'installing ansible'
sudo apt update
sudo apt install ansible

echo '\nmake sure you have an ssh key, and pushed it to github and bitbucket' 
read

echo 'log in to firefox account and sync add-ons'
read

echo '*after* running the playbook, run `dropbox status`'

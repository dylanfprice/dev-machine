#!/bin/bash 

echo 'disabling graphical boot'
sudo systemctl disable display-manager.service
sudo systemctl set-default multi-user.target

echo 'get an internet connection!'
echo '(might need to plug in to ethernet and set up systemd-networkd)'
read

echo 'installing sudo'
sudo apt update
sudo apt install sudo
echo '\nadd me to sudoers group'
read

echo 'installing ansible'
sudo apt install ansible

echo '\nmake sure you have an ssh key, and pushed it to github' 
read

echo 'log in to firefox account and sync add-ons'
read

#!/bin/bash 

echo 'installing ansible'
sudo apt-add-repository ppa:ansible/ansible
sudo apt-get update
sudo apt-get install ansible

echo '\nmake sure you have an ssh key, and pushed it to github and bitbucket' 
read

echo 'install the following firefox add-ons:'
echo 'https://addons.mozilla.org/en-US/firefox/addon/vimperator/'
echo 'https://addons.mozilla.org/en-US/firefox/addon/tree-style-tab/'
echo 'https://addons.mozilla.org/en-US/firefox/addon/session-manager/'
echo 'https://addons.mozilla.org/en-US/firefox/addon/privacy-badger-firefox/'
echo 'https://addons.mozilla.org/en-US/firefox/addon/lastpass-password-manager/'
echo 'https://addons.mozilla.org/en-US/firefox/addon/ublock-origin/'
echo 'https://addons.mozilla.org/en-US/firefox/addon/decentraleyes/'
read

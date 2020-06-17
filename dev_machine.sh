#!/bin/bash

ansible-playbook \
    -i "localhost," \
    -e 'ansible_python_interpreter=/usr/bin/python3' \
    --private-key=~/.ssh/id_rsa \
    --ask-become-pass \
    -c local \
    dev_machine.yml \
    $*

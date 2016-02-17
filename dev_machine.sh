#!/bin/bash

ansible-playbook -i "localhost," --private-key=~/.ssh/id_rsa --ask-become-pass -c local dev_machine.yml $*

#!/bin/bash

ansible-playbook -i "localhost," -c local -K dev_machine.yml $*

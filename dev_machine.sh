#!/bin/bash

ansible-playbook -i "localhost," -c local dev_machine.yml $*

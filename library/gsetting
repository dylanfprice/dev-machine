#!/usr/bin/env python2

DOCUMENTATION = '''
---
module: gsettings
short_description: Manage GNOME settings
'''

EXAMPLES = '''
- gsettings: schema=org.gnome.software key=download-updates value=false
'''

import json
import re
import subprocess

from ansible.module_utils.basic import *


def get_dbus_launch_call():
    if 'DBUS_SESSION_BUS_ADDRESS' in os.environ:
        return []
    else:
        return ['dbus-launch', '--exit-with-session', '--']

def gsettings_get(schema, key):
    result = subprocess.check_output(get_dbus_launch_call() + [
        'gsettings', 'get', schema, key])
    assert result.endswith('\n')
    return result[:-1]

def gsettings_set(schema, key, value):
    subprocess.check_output(get_dbus_launch_call() + [
        'gsettings', 'set', schema, key, value])


def main():

    module = AnsibleModule(
        argument_spec = {
            'state': { 'choices': ['present'], 'default': 'present' },
            'schema': { 'required': True },
            'key': { 'required': True },
            'value': { 'required': True },
        },
        supports_check_mode = True,
    )

    params = module.params
    state = module.params['state']
    schema = module.params['schema']
    key = module.params['key']
    value = module.params['value']

    current_value = gsettings_get(schema, key)
    changed = current_value != value

    if changed and not module.check_mode:
        gsettings_set(schema, key, value)

    module.exit_json(changed=changed)


if __name__ == '__main__':
    main()

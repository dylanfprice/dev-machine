#!/usr/bin/env python

import os
from os.path import basename, dirname
from subprocess import check_output, CalledProcessError


ISORT_CFG_TEMPLATE = '''
[settings]
line_length=100
# Use hanging-indent for multi-line imports
multi_line_output=2
default_section=THIRDPARTY
known_first_party={known_first_party}
not_skip=__init__.py
lines_after_imports=2
'''


def _ag_setup_pys(repo):
    try:
        return check_output(['ag', '-g', '/setup.py$', repo]).split('\n')
    except CalledProcessError:
        return ()


def get_top_level_python_packages(energysavvy_dir):
    repos = filter(
        bool,
        (
            check_output([
                'bash',
                '-c',
                'dirname $(dirname $(ls {}/*/.hg/hgrc))'.format(energysavvy_dir)
            ])
            .split('\n')
        )
    )

    setup_pys = (
        setup_py
        for repo in repos
        for setup_py in _ag_setup_pys(repo)
        if setup_py
    )

    pip_packages = (
        dirname(setup_py) for setup_py in setup_pys
    )

    top_level_init_pys = (
        top_level_init_py
        for pip_package in pip_packages
        for top_level_init_py in (
            check_output(['ag', '-g', '{}/[^/]+/__init__.py$'.format(pip_package), pip_package])
            .split('\n')
        )
        if top_level_init_py
    )
    top_level_python_packages = {
        basename(dirname(top_level_init_py)) for top_level_init_py in top_level_init_pys
    }
    return top_level_python_packages

energysavvy_dir = os.environ['ENERGYSAVVY_DIR']
print(ISORT_CFG_TEMPLATE.format(
    known_first_party=','.join(get_top_level_python_packages(energysavvy_dir))
))

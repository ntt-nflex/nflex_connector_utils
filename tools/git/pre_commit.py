#!/usr/bin/env python

import sys
import os
from flake8.hooks import git_hook
import pep8
import pyflakes
import mccabe

PEP_VERSION = '1.7.0'
PYFLAKES_VERSION = '1.0.0'
MCCABE_VERSION = '0.4.0'

# Check versions
if pep8.__version__ != PEP_VERSION:
    print('The git hooks require pep8 version %s' % PEP_VERSION)

if pyflakes.__version__ != PYFLAKES_VERSION:
    print('The git hooks require pyflakes version %s' % PYFLAKES_VERSION)

if mccabe.__version__ != MCCABE_VERSION:
    print('The git hooks require mccabe version %s' % MCCABE_VERSION)


STRICT = os.getenv('FLAKE8_STRICT', True)
IGNORE = os.getenv('FLAKE8_IGNORE')
LAZY = os.getenv('FLAKE8_LAZY', False)


if __name__ == '__main__':
    sys.exit(git_hook(
        strict=STRICT,
        ignore=IGNORE,
        lazy=LAZY,
    ))

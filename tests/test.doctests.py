#!/usr/bin/env python
# Run doctests

from __future__ import division, print_function
import sys
import doctest
from nonstdlib.io import color
import nonstdlib.classes as classes
import nonstdlib.debug as debug
import nonstdlib.execute as execute
import nonstdlib.io as io
import nonstdlib.meta as meta
import nonstdlib.misc as misc
import nonstdlib.text as text

class Test(object):
    def __init__(self, name, module):
        self.name = name
        self.module = module

testcases = [
    Test('classes', classes),
    #Test('debug', debug),
    Test('execute', execute),
    Test('io', io),
    Test('meta', meta),
    Test('misc', misc),
    Test('text', text),
]

failures = False
for case in testcases:
    (fails, tests) = doctest.testmod(case.module)
    if fails:
        failures = True
    print(
        color(
            '%s %s: %s tests run, %s failures detected.' % (
                case.name, 'FAILS' if fails else 'Passes', tests, fails
            ), 'red' if fails else 'green'
        )
    )

sys.exit(bool(failures))

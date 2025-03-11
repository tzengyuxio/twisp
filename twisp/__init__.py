#!/usr/bin/env python

"""twisp: TaiWan Individual e-Statement Parser"""

__version__ = '0.1.0'

import sys
from .tsib import CreditCardParser

SOME_WORD = 'hello sekai'


def add_one(n):
    return n + 1


def _real_main():
    print("hello sekai")
    p = CreditCardParser()
    p.extract(sys.argv[1])


def main():
    _real_main()

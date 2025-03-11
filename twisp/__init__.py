#!/usr/bin/env python

"""twisp: TaiWan Individual e-Statement Parser"""

__version__ = '0.1.0'

import sys

import click

from .tsib import CreditCardParser

SOME_WORD = 'hello sekai'


def add_one(n):
    return n + 1


@click.command()
@click.argument('filename', type=click.Path(exists=True))
@click.option('--password', help='The password for opening the PDF file.')
def main(filename, password):
    p = CreditCardParser()
    p.extract(filename)

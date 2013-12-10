"""Module to load flags."""
import sys

from optparse import OptionParser


PARSER = OptionParser()
OPTIONS = None


def init():
    """init flag parsing.
    Args:
      argv: list of string, which should be the same as sys.argv.

    Return:
      no return
    """
    (options, argv) = PARSER.parse_args()
    sys.argv = [sys.argv[0]] + argv
    global OPTIONS
    OPTIONS = options


def add(flagname, **kwargs):
    """add a flag name and its setting."""
    PARSER.add_option('--%s' % flagname, dest=flagname, **kwargs)


def add_bool(flagname, default=True, **kwargs):
    """add a bool flag name and its setting."""
    PARSER.add_option('--%s' % flagname,
                      dest=flagname, default=default,
                      action="store_true", **kwargs)
    PARSER.add_option('--no%s' % flagname,
                      dest=flagname,
                      action="store_false", **kwargs)

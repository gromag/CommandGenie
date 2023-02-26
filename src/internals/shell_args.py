import sys
import argparse
from .version import __version__


class VersionAction(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        print(__version__)
        sys.exit(0)


def get_shell_args(args=None):
    parser = argparse.ArgumentParser(
        description=f"""
    CommandGenie Utility (version: {__version__}).
     CommandGenie is a Python-based command-line tool that uses the power of
     artificial intelligence to generate commands and automate common tasks."""
    )

    parser.add_argument(
        "-v",
        "--version",
        action=VersionAction,
        nargs=0,
        help="Prints the CommandGenie version.",
    )

    shellargs = parser.parse_args(args)

    return shellargs

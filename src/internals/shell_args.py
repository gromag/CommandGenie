import sys
import argparse
from internals.provider_log_path import LogPathProvider
from .version import __version__


class CliArgs:
    VERBOSE = False
    START_DAEMON = False
    COMMAND = ""


class VersionAction(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        print(__version__)
        sys.exit(0)


class VerboseAction(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        CliArgs.VERBOSE = True


class StartAction(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        CliArgs.START_DAEMON = True


class CommandAction(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        CliArgs.COMMAND = values


def _inject_and_get_args():
    # Get the command-line arguments
    args = sys.argv[1:]

    if len(args) and args[0][0] != "-":
        command = " ".join(args).strip()
        args = ["-c", command]

    return args


def _get_shell_args(args):
    parser = argparse.ArgumentParser(
        description=f"""
    CommandGenie Utility (version: {__version__}).
     CommandGenie is a Python-based command-line tool that uses the power of
     artificial intelligence to generate commands and automate common tasks.
     Please start the daemon `genie -s` on a separate shell window before 
     starting the client.
     Example usage:
     `genie delete all __pycache__ folders`
     """
    )

    parser.add_argument(
        "-v",
        "--version",
        action=VersionAction,
        nargs=0,
        help="Prints the CommandGenie version",
    )

    parser.add_argument(
        "-V",
        "--verbose",
        action=VerboseAction,
        nargs=0,
        help=f"Sets high verbosity (DEBUG). To view the file logs see: {LogPathProvider().get_path()}",
    )
    
    parser.add_argument("-s", "--start", action=StartAction, nargs=0, help="Starts the CommandGenie daemon")

    parser.add_argument(
        "-c",
        "--command",
        action=CommandAction,
        help="Takes an English instruction which will be converted into a shell command",
    )


    shellargs = parser.parse_args(args)

    return shellargs


injected_args = _inject_and_get_args()
_get_shell_args(injected_args)

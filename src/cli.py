from daemon.server import start_daemon
from internals.shell_args import CliArgs
from genie.genie import GenieClient
from internals.ui_interaction import UIInteraction


def start():
    # Get the command-line arguments
    if CliArgs.COMMAND:
        genie = GenieClient(UIInteraction())
        genie.run(CliArgs.COMMAND)
    elif CliArgs.START_DAEMON:
        start_daemon()


if __name__ == "__main__":
    start()
